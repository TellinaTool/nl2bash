package cmd_parser;

import man_parser.cmd.Cmd;
import org.antlr.v4.runtime.misc.Pair;

import java.util.*;

/**
 * Created by clwang on 9/27/16.
 */
public class CmdGrammarGenerator {

    public static String genG4(List<Cmd.Command> commands, List<String> targets) {

        String prologue = "grammar Commands;";

        String content = "";

        List<String> commandDef = new ArrayList<>();
        Set<String> nonTerminals = new HashSet<>();

        for (Cmd.Command cmd : commands) {
            if (targets != null && targets.size() != 0) {
                if (! targets.contains(cmd.name))
                    continue;
            }
            Pair<String, List<String>> p = emitGrammar(cmd);
            commandDef.add(p.a);
            nonTerminals.addAll(p.b);
        }

        content += "command : " + commandDef.get(0) + "\n";
        for (int i = 1; i < commandDef.size(); i ++) {
            content += "\t    | " + commandDef.get(i) + "\n";
        }
        content += "\t    ;" + "\n\n";
        for (String t : nonTerminals) {
            content += t + ";" + "\n";
        }

        String epilogue = "/*File : STRING; \nPermission: STRING; \nSize: STRING; \nTime: STRING; \nArgument: STRING; \nUtility: STRING; \nNumber: STRING; \nPattern: STRING; \nString : STRING;*/ \n//STRING : ( 'a' .. 'z' | 'A' .. 'Z' | '0' .. '9' | '.' | '_' | '/' ) + ; \nSTRING : ( ~' ' ) + ; \nWS : [ \\t\\n\\r] + -> skip;";

        return prologue + "\n\n" + content + "\n" + epilogue;

    }

    public static Pair<String, List<String>> emitGrammar(Cmd.Command command) {
        Pair<String, List<String>> p = new CmdGrammarGenerator(command.name).emitGrammar(command.option);
        return new Pair<>("'"+ command.name + "' " + p.a, p.b);
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

    private Pair<String, List<String>> emitGrammar(Cmd.CmdOp option) {

        if (option instanceof Cmd.Compound) {
            String result = "";
            List<String> emitted = new ArrayList<>();
            for (Cmd.CmdOp op : ((Cmd.Compound) option).commands) {
                Pair<String, List<String>> grammarString = emitGrammar(op);
                emitted.addAll(grammarString.b);
                result += grammarString.a + " ";
            }
            return new Pair<>(result, emitted);

        } else if (option instanceof Cmd.Ar) {

            String argTok;
            String enhancedType =  ((Cmd.Ar) option).arg_type + "=STRING";


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
                Pair<String, List<String>> grammarString = emitGrammar(op);
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

                Pair<String, List<String>> arp = emitGrammar(((Cmd.Flv2) option).argument);

                if (! ((Cmd.Flv2) option).arg_optional) {
                    return new Pair<>(flagPart + "=' " + arp.a, new ArrayList<>());
                } else {
                    return new Pair<>(flagPart + "=' " + "(" + arp.a + ")*", new ArrayList<>());
                }
            }

        } else if (option instanceof Cmd.Opt) {
            List<String> emitted  = new ArrayList<>();

            Pair<String, List<String>> p = emitGrammar(((Cmd.Opt) option).cmd);
            emitted.addAll(p.b);

            String intermediate = getNoneTerminalName(this.cmdName, ((Cmd.Opt) option).cmd.toString());

            emitted.add(intermediate + " : " + p.a);

            return new Pair<>("(" + intermediate + ")?", emitted);
        }

        return null;
    }
}