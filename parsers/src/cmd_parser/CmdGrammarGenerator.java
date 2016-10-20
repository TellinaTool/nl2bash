package cmd_parser;

import man_parser.cmd.Cmd;
import org.antlr.v4.runtime.misc.IntegerList;
import org.antlr.v4.runtime.misc.Pair;

import java.util.*;
import java.util.stream.Collectors;

/**
 * Created by clwang on 9/27/16.
 */
public class CmdGrammarGenerator {

    static Set<String> argTypeCollector = new HashSet<>();

    /**
     * Generate g4 grammar for given commands
     * @param commands The list of commands to be processed
     * @param whitelist An optional list: if target is empty, we will emit grammar for all commands in the list,
     *                otherwise we will only generate commands in the targets list.
     * @return A string representing the g4 grammar for all of these commands.
     */
    public static String genG4(List<Cmd.Command> commands, Map<String, List<Cmd.CmdOp>> cmdNonTerminals, List<String> whitelist) {

        // grammar declaration
        String prologue = "grammar Commands;";

        String content = "";

        content += "command : primitive_command \n" +
                "           | primitive_command ('|' primitive_command)*; \n\n";

        List<String> commandDef = new ArrayList<>();
        Set<String> nonTerminals = new HashSet<>();

        for (Cmd.Command cmd : commands) {
            if (whitelist != null && whitelist.size() != 0) {
                if (! whitelist.contains(cmd.name))
                    continue;
            }
            Pair<String, List<String>> p = emitGrammar(cmd);
            commandDef.add(p.a);
            nonTerminals.addAll(p.b);
        }

        content += "primitive_command : ";

        // generating command non-terminals
        List<String> commandNonTerminal = new ArrayList<>();

        // use the nameAssigner to avoid duplicate names
        Map<String, Integer> nameAssigner = new HashMap<>();
        for (String t : commandDef) {
            String hd = t.split("\\s+")[0];
            String name = hd.substring(1, hd.length()-1);
            if (! nameAssigner.containsKey(name)) {
                nameAssigner.put(name, 0);
            }
            nameAssigner.put(name, nameAssigner.get(name) + 1);
            name = name + nameAssigner.get(name);
            content += name + "\n\t    | ";

            commandNonTerminal.add(name + " : " + aggregateOptionalOps(t));
        }

        // remove the last "|"
        content = content.substring(0, content.length()-2) + ";\n\n";

        for (String t : commandNonTerminal) {
            content += t + ";\n";
        }

        content += "\n";

        for (Map.Entry<String, List<Cmd.CmdOp>> e : cmdNonTerminals.entrySet()) {
            content += e.getKey() + " : ";
            int indent = e.getKey().length() + 1;
            boolean first = true;
            for (Cmd.CmdOp op : e.getValue()) {
                Pair<String, List<String>> p = emitNonTerminalGrammar(e.getKey(), op);
                nonTerminals.addAll(p.b);
                if (! first) {
                    for (int i = 0; i < indent; i ++)
                        content += " ";
                    content += "| ";
                } else {
                    first = false;
                }
                content += p.a + "\n";
            }
            for (int i = 0; i < indent; i ++)
                content += " ";
            content += "; ";
            content += "\n\n";
        }

        content += "\n\n";

        for (String t : nonTerminals.stream().sorted().collect(Collectors.toList())) {
            content += t + ";" + "\n";
        }


        String typeDef = "";
        for (String s : argTypeCollector) {
            typeDef += s + " : STRING \n    | '$(' command ')'; \n\n";
        }

        String epilogue =
                typeDef +
                "//arg : ( 'a' .. 'z' | 'A' .. 'Z' | '0' .. '9' | '.' | '_' | '/' ) + ; \n\n" +
                "arg : STRING \n" +
                "    | '$(' command ')'; \n\n" +
                "STRING : (~(' ' | '-'))+ \n" +
                "       | '\"' (~'\"')+ '\"'\n" +
                "       |  '\\'' (~'\\'')+ '\\''\n" +
                "       ;\n" +
                "WS : [ \\t\\n\\r] + -> skip;";

        return prologue + "\n\n" + content + "\n" + epilogue;
    }

    /**
     * Given a string representing command top-level grammar,
     * aggregate optional options like "(op1)? (op2)" ==> (op1 | op2)*
     * @param cmdDef the string representation of top-level command BNF
     * @return transformed grammar string
     */
    private static String aggregateOptionalOps(String cmdDef) {
        String[] segments = cmdDef.split("\\s+");

        List<String> result = new ArrayList<>();
        int i = 0;

        while (i < segments.length) {

            List<String> aggrStrings = new ArrayList<>();
            while (i < segments.length && segments[i].matches("\\(.+\\)\\?")) {
                aggrStrings.add(segments[i]);
                i ++;
            }

            if (aggrStrings.isEmpty()) {
                result.add(segments[i]);
                i ++;
            } else {
                String str = "("
                        + aggrStrings.stream()
                            .map(x -> "(" + x.substring(1, x.length()-2) + ")")
                            .reduce((x,y)-> x + " | " + y).get()
                        + ")*";
                result.add(str);
            }
        }

        return result.stream().reduce((x, y) -> (x + " " + y)).get();
    }

    public static Pair<String, List<String>> emitGrammar(Cmd.Command command) {
        Pair<String, List<String>> p = new CmdGrammarGenerator(command.name).emitGrammar(command.option, command.type);
        return new Pair<>("'"+ command.name + "' " + p.a, p.b);
    }

    public static Pair<String, List<String>> emitNonTerminalGrammar(String ntName, Cmd.CmdOp nonTerminalContent) {
        Pair<String, List<String>> p = new CmdGrammarGenerator(ntName).emitGrammar(nonTerminalContent, nonTerminalContent.getType());
        return new Pair<>(p.a, p.b);
    }

    String cmdName;

    private CmdGrammarGenerator(String cmdName) {
        this.cmdName = cmdName;
    }

    private static Map<String, Integer> optionCountPerCommand = new HashMap<>();
    private static Map<Pair<String, String>, String> nonTerminalDict = new HashMap<>();

    private static String getNoneTerminalName(String command, String nonTerminal) {

        if (! nonTerminalDict.containsKey(new Pair<>(command, nonTerminal))) {
            if (! optionCountPerCommand.containsKey(command)) {
                optionCountPerCommand.put(command, 0);
            }

            String name = command + "_op" + optionCountPerCommand.get(command);
            optionCountPerCommand.put(command, optionCountPerCommand.get(command) + 1);

            nonTerminalDict.put(new Pair<>(command, nonTerminal), name);
        }

        return nonTerminalDict.get(new Pair<>(command, nonTerminal));
    }

    private Pair<String, List<String>> emitGrammar(Cmd.CmdOp option, String lastLevelType) {

        if (option instanceof Cmd.Compound) {
            String result = "";
            List<String> emitted = new ArrayList<>();
            for (Cmd.CmdOp op : ((Cmd.Compound) option).commands) {
                Pair<String, List<String>> grammarString = emitGrammar(op, ((Cmd.Compound) option).type);
                emitted.addAll(grammarString.b);
                result += grammarString.a + " ";
            }

            return new Pair<>(result, emitted);

        } else if (option instanceof Cmd.Ar) {

            String argTok;
            String enhancedType =  "arg_" + ((Cmd.Ar) option).arg_type;

            argTypeCollector.add(enhancedType);

            if (((Cmd.Ar) option).arg_type.equals("Constant"))
                argTok = "'" + ((Cmd.Ar) option).arg_name + "'";
            else {
                String argPrefix = "";
                if (((Cmd.Ar) option).arg_name.startsWith("MINUS"))
                    argPrefix = "'-'";
                if (((Cmd.Ar) option).arg_name.startsWith("PLUS"))
                    argPrefix = "'+'";
                if (((Cmd.Ar) option).arg_name.startsWith("EQUAL"))
                    argPrefix = "'='";

                argTok = argPrefix + enhancedType;
            }

            if (((Cmd.Ar) option).isList)
                return new Pair<>("(" + argTok+ ")+", new ArrayList<>());
            else
                return new Pair<>(argTok, new ArrayList<>());

        } else if (option instanceof Cmd.Exclusive) {
            String result = "";

            List<String> emitted = new ArrayList<>();
            boolean first = true;
            for (Cmd.CmdOp op : ((Cmd.Exclusive) option).commands) {
                Pair<String, List<String>> grammarString = emitGrammar(op, ((Cmd.Exclusive) option).type);
                emitted.addAll(grammarString.b);
                if (! first) {
                    result += " | " + grammarString.a;
                } else {
                    first = false;
                    result += grammarString.a;
                }
            }
            return new Pair<>(result, emitted);

        } else if (option instanceof Cmd.Fl) {

            return new Pair<>("'-" + ((Cmd.Fl) option).flag_name + "'", new ArrayList<>());

        } else if (option instanceof Cmd.Flv2) {

            String flagPart = "'--" + ((Cmd.Flv2) option).flag_name;

            if (! ((Cmd.Flv2) option).arg_exists) {
                return new Pair<>(flagPart + "'", new ArrayList<>());
            } else {

                Pair<String, List<String>> arp = emitGrammar(((Cmd.Flv2) option).argument, ((Cmd.Flv2) option).type);

                if (! ((Cmd.Flv2) option).arg_optional) {
                    return new Pair<>(flagPart + "=' " + arp.a, new ArrayList<>());
                } else {
                    return new Pair<>(flagPart + "=' " + "(" + arp.a + ")*", new ArrayList<>());
                }
            }

        } else if (option instanceof Cmd.Opt) {

            List<String> emitted  = new ArrayList<>();

            Pair<String, List<String>> p = emitGrammar(((Cmd.Opt) option).cmd, ((Cmd.Opt) option).type);
            emitted.addAll(p.b);

            String intermediate = getNoneTerminalName(this.cmdName, ((Cmd.Opt) option).cmd.toString());

            emitted.add(intermediate + " : " + p.a);

            if (!lastLevelType.equals("exclusive_options"))
                return new Pair<>("(" + intermediate + ")?", emitted);
            else
                return new Pair<>(intermediate, emitted);

        } else if (option instanceof Cmd.NonTerminal) {
            if (((Cmd.NonTerminal) option).isList)
                return new Pair<>("(" + ((Cmd.NonTerminal) option).name+ ")*", new ArrayList<>());
            else
                return new Pair<>(((Cmd.NonTerminal) option).name, new ArrayList<>());
        }

        return null;
    }
}