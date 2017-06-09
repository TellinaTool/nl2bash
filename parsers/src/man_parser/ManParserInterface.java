package man_parser;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.PropertyAccessor;
import com.fasterxml.jackson.core.sym.Name;
import com.fasterxml.jackson.databind.ObjectMapper;
import main.Config;
import man_parser.cmd.Cmd;
import javafx.util.Pair;
import man_parser.parser.*;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class ManParserInterface {

    public static String parseSynopsisBNF() throws IOException, ParseException {

        // summarizing options of the file tar.1.txt

        List<Cmd.Command> commands = ManParserInterface.parseGrammarFile(Config.SynopsisGrammar).commandsGrammar;

        ObjectMapper mapper = new ObjectMapper();
        mapper.setVisibility(PropertyAccessor.FIELD, JsonAutoDetect.Visibility.ANY);
        return mapper.writeValueAsString(commands);
    }

    public static void parseManPage(boolean testSmallExamples) throws IOException {
        String PREFIX = Config.ProjectFolder;

        if (testSmallExamples) {
            String[] targetFiles = {
                    PREFIX + "data/plain-man/find.1.txt",
                    PREFIX + "data/plain-man/mv.1.txt",
                    PREFIX + "data/plain-man/sort.1.txt",
                    PREFIX + "data/plain-man/grep.1.txt",
                    PREFIX + "data/plain-man/egrep.1.txt",
                    PREFIX + "data/plain-man/cp.1.txt",
                    PREFIX + "data/plain-man/ls.1.txt",
                    PREFIX + "data/plain-man/tar.1.txt",
                    PREFIX + "data/plain-man/xargs.1.txt",
                    PREFIX + "data/plain-man/sed.1.txt",
                    PREFIX + "data/plain-man/awk.1.txt",
                    PREFIX + "data/plain-man/rm.1.txt",
                    PREFIX + "data/plain-man/cd.1.txt",
                    PREFIX + "data/plain-man/wc.1.txt",
                    PREFIX + "data/plain-man/chmod.1.txt",
                    PREFIX + "data/plain-man/chgrp.1.txt",
                    PREFIX + "data/plain-man/head.1.txt",
                    PREFIX + "data/plain-man/tail.1.txt",
                    PREFIX + "data/plain-man/seq.1.txt",
                    PREFIX + "data/plain-man/unlink.1.txt",
                    PREFIX + "data/plain-man/cat.1.txt",
                    PREFIX + "data/plain-man/zip.1.txt",
                    PREFIX + "data/plain-man/unzip.1.txt",
                    PREFIX + "data/plain-man/du.1.txt",
                    PREFIX + "data/plain-man/echo.1.txt",
                    PREFIX + "data/plain-man/diff.1.txt",
                    PREFIX + "data/plain-man/comm.1.txt",
                    PREFIX + "data/plain-man/sh.1.txt"
            };

            List<Cmd.ManPage> manPages = new ArrayList<>();
            for (String f : targetFiles) {
                //System.out.println(f);
                Cmd.ManPage mp = ManParserInterface.parseFile(new File(f));
                if (mp.aliases.isEmpty())
                    System.out.println("???" + f);
                manPages.add(mp);

            }
            ObjectMapper mapper = new ObjectMapper();
            mapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
            String jsonInString = mapper.writeValueAsString(manPages);
            System.out.println(jsonInString);
        } else {
            File[] files = new File(PREFIX +  "data/plain-man").listFiles();

            for (File f : files) {
                if (! f.getName().matches("\\w*\\.\\d\\.txt"))
                    continue;
                ManParserInterface.parseFile(f);
            }
        }
    }

    public static class GrammarFile {
        public List<Cmd.Command> commandsGrammar = new ArrayList<>();
        public Map<String, String> nameToTypeDict = new HashMap<>();
        public Map<String, String> constantNameToSymbol = new HashMap<>();
        public Map<String, List<Cmd.CmdOp>> nonTerminals = new HashMap<>();

        public GrammarFile(List<Cmd.Command> commandsGrammar, Map<String, List<Cmd.CmdOp>> nonTerminals,
                           Map<String, String> nameToTypeDict, Map<String, String> constantNameToSymbol) {
            this.commandsGrammar = commandsGrammar;
            this.nameToTypeDict = nameToTypeDict;
            this.constantNameToSymbol = constantNameToSymbol;
            this.nonTerminals = nonTerminals;
        }
    }

    // parse the grammar file
    public static GrammarFile parseGrammarFile(String path) throws IOException, ParseException {
        List<String> lines = Files.readAllLines(Paths.get(path));

        List<Cmd.Command> commands = new ArrayList<>();
        Map<String, String> nameToTypeDict = new HashMap<>();
        Map<String, String> constantNameToSymbol = new HashMap<>();
        Map<String, List<Cmd.CmdOp>> nonTerminals = new HashMap<>();

        List<String> rawCommands = new ArrayList<>();
        List<String> rawNameToTypes = new ArrayList<>();
        List<String> rawConstantToType = new ArrayList<>();
        Map<String, List<String>> rawNonTerminals = new HashMap<>();

        int i = 0;
        while (i < lines.size()) {
            if (lines.get(i).startsWith("PrimitiveCmd")) {
                i ++;
                int l = i;
                while (i < lines.size()) {
                    if (indentCount(lines.get(i)) == 0 && !lines.get(i).trim().equals(""))
                        break;
                    i ++;
                }

                rawCommands = lines.subList(l, i)
                        .stream().filter(s -> !s.trim().equals("")).map(s -> s.trim()).collect(Collectors.toList());

            } else if (lines.get(i).startsWith("type")) {
                i++;
                int l = i;
                while (i < lines.size()) {
                    if (indentCount(lines.get(i)) == 0 && !lines.get(i).trim().equals(""))
                        break;
                    i++;
                }
                rawNameToTypes = lines.subList(l, i)
                        .stream().filter(s -> !s.trim().equals("")).map(s -> s.trim()).collect(Collectors.toList());

            } else if (lines.get(i).startsWith("constant")) {
                i++;
                int l = i;
                while (i < lines.size()) {
                    if (indentCount(lines.get(i)) == 0 && !lines.get(i).trim().equals(""))
                        break;
                    i++;
                }

                rawConstantToType = lines.subList(l, i)
                        .stream().filter(s -> !s.trim().equals("")).map(s -> s.trim()).collect(Collectors.toList());

            } else {

                if (! lines.get(i).contains(":=")) {
                    i ++;
                    continue;
                }

                String ntName = lines.get(i).substring(0, lines.get(i).indexOf(":=")).trim();

                i ++;
                int l = i;
                while (i < lines.size()) {
                    if (indentCount(lines.get(i)) == 0 && !lines.get(i).trim().equals(""))
                        break;
                    i ++;
                }

                List<String> nonTerminalContents = lines.subList(l, i)
                        .stream().filter(s -> !s.trim().equals("")).map(s -> s.trim()).collect(Collectors.toList());

                rawNonTerminals.put(ntName, nonTerminalContents);
            }
        }

        for (String s : rawConstantToType) {
            String[] p = s.split("\\s+");
            constantNameToSymbol.put(p[0], p[1]);
        }

        for (String s : rawNameToTypes) {
            String typeName = s.substring(0, s.indexOf("(")).trim();
            String[] argnames = s.substring(s.indexOf("(") + 1, s.indexOf(")")).split(",");
            for (String a : argnames) {
                nameToTypeDict.put(a.trim(), typeName);
            }
        }

        Cmd.ConstantArgDict = constantNameToSymbol;
        Cmd.NameToTypeDict = nameToTypeDict;

        commands = parsePrimitiveGrammar(rawCommands);


        for (Map.Entry<String, List<String>> e : rawNonTerminals.entrySet()) {
            nonTerminals.put(e.getKey(), parseNonTerminalContent(e.getValue()));
        }

        return new GrammarFile(commands, nonTerminals, nameToTypeDict, constantNameToSymbol);

    }

    public static List<Cmd.Command> parsePrimitiveGrammar(List<String> rawCommands) throws ParseException {
        List<Cmd.Command> commands = new ArrayList<>();
        for (String s : rawCommands) {
            String name = s.trim().split("\\s+")[0];
            String raw = s.substring(s.indexOf(name) + name.length()).trim();
            commands.add(new Cmd.Command(name, parseSynopsisInstance(raw)));
        }
        return commands;
    }

    public static List<Cmd.CmdOp> parseNonTerminalContent(List<String> cmdOpContents) throws ParseException {
        List<Cmd.CmdOp> options = new ArrayList<>();
        for (String s : cmdOpContents) {
            String raw = s.trim();
            options.add(parseSynopsisInstance(raw));
        }
        return options;
    }

    public static Cmd.ManPage parseFile(File file) throws IOException {
        // read the file
        List<String> lines = Files.readAllLines(file.toPath());
        Cmd.ManPage manpage = new Cmd.ManPage();

        int i = 0;
        while (i < lines.size()) {
            if (lines.get(i).startsWith("NAME")) {
                // segmenting the name section
                int l = i + 1;
                i ++;
                while (i < lines.size() && indentCount(lines.get(i)) != 0) {
                    i ++;
                }
                Pair<List<String>, String> name = parseName(lines.subList(l, i));
                manpage.setName(name.getKey(), name.getKey().get(0) + ": " + name.getValue() + "\n");
            } else if (i < lines.size() && lines.get(i).startsWith("SYNOPSIS")) {
                // segmenting the synopsis section
                int l = i + 1;
                i ++;
                while (indentCount(lines.get(i)) != 0) {
                    i ++;
                }
                manpage.rawSynopsis =lines.subList(l,i).stream().reduce("", (x,y)->(x.trim() + "\n" + y.trim())).trim();
                List<Pair<String, Cmd.CmdOp>> options = parseSynopsis(manpage.getName(), lines.subList(l,i));
                for (Pair<String, Cmd.CmdOp> pair : options) {
                    manpage.optionLists.add(pair.getValue());
                }
            } else if (i < lines.size() && (lines.get(i).startsWith("DESCRIPTION"))) {
                // segmenting the description section
                int l = i + 1;
                i ++;
                while(indentCount(lines.get(i)) != 0 || lines.get(i).equals("")) {
                    i ++;
                }
                Pair<String, List<Pair<String, String>>> descSec = parseDescription(lines.subList(l, i));
                manpage.description += descSec.getKey() + "\n";
                for (Pair<String, String> desc : descSec.getValue()) {
                    String optionPart = desc.getKey();
                    int inOuterLevel = 0;
                    boolean added = false;
                    for (int k = 0; k < optionPart.length(); k ++) {
                        if (optionPart.charAt(k) == ',' && inOuterLevel == 0) {

                            try {
                                Cmd.DescriptionPair d = new Cmd.DescriptionPair(parseSynopsisInstance(optionPart.substring(0, k)), optionPart, desc.getValue());
                                manpage.optionDesc.add(d);

                                added = true;
                            } catch (ParseException e) {
                                continue;
                            }
                        } else if (optionPart.charAt(k) == '[') {
                            inOuterLevel ++;
                        } else if (optionPart.charAt(k) == '[') {
                            inOuterLevel --;
                        }
                    }
                    if (! added) {
                        try {
                            manpage.optionDesc.add(
                                    new Cmd.DescriptionPair(parseSynopsisInstance(optionPart), optionPart, desc.getValue()));
                        } catch (ParseException e) {
                            continue;
                        }
                    }
                }
                i --;
            } else if (i < lines.size() && (lines.get(i).startsWith("PRIMARIES")
                            || lines.get(i).startsWith("USE")
                            || lines.get(i).startsWith("OPTIONS"))) {

                // segmenting the PRIMARIES section, specially for the find command
                int l = i + 1;
                i ++;

                while(indentCount(lines.get(i)) != 0 || lines.get(i).equals("")) {
                    i ++;
                }
                Pair<String, List<Pair<String, String>>> descSec = parseDescription(lines.subList(l, i));
                for (Pair<String, String> desc : descSec.getValue()) {
                    String optionPart = desc.getKey();
                    int inOuterLevel = 0;
                    boolean added = false;
                    for (int k = 0; k < optionPart.length(); k ++) {
                        if (optionPart.charAt(k) == ',' && inOuterLevel == 0) {
                            try {
                                manpage.optionDesc.add(
                                        new Cmd.DescriptionPair(parseSynopsisInstance(optionPart.substring(0, k)), optionPart, desc.getValue()));
                                added = true;
                            } catch (ParseException e) {
                                continue;
                            }
                        } else if (optionPart.charAt(k) == '[') {
                            inOuterLevel ++;
                        } else if (optionPart.charAt(k) == '[') {
                            inOuterLevel --;
                        }
                    }
                    if (! added) {
                        try {
                            manpage.optionDesc.add(
                                    new Cmd.DescriptionPair(parseSynopsisInstance(optionPart), optionPart, desc.getValue()));
                        } catch (ParseException e) {
                            continue;
                        }
                    }
                }
                i --;
            } else if (i < lines.size() && lines.get(i).startsWith("EXAMPLES")) {
                int l = i + 1;
                i ++;
                while (indentCount(lines.get(i)) != 0 || lines.get(i).equals("")) {
                    i ++;
                }
                parseExample(lines.subList(l, i));
            }

            i ++;
        }

        return manpage;
    }

    // return value: key is the list of parsed aliases, value is the cmd description
    private static Pair<List<String>, String> parseName(List<String> secContent) {
        String content = secContent.stream().reduce("", String::concat).replaceAll("\\s+", " ");

        List<String>  aliases = new ArrayList<>();
        String description = "";

        String rawName = content.trim();

        if (content.contains(" -- ")) {
            rawName = content.substring(0, content.indexOf(" -- ")).trim();
            description = content.substring(content.indexOf(" -- ") + 4).trim();
        } else if (content.contains(" - ")) {
            rawName = content.substring(0, content.indexOf(" - ")).trim();
            description = content.substring(content.indexOf(" - ") + 3).trim();
        }

        String[] splits = rawName.split(",");
        for (String s : splits) {
            if (s.trim().equals("")) continue;
            aliases.add(s.trim());
        }
        return new Pair<>(aliases, description);
    }

    // return value: extract the value
    private static List<Pair<String, Cmd.CmdOp>> parseSynopsis(String name, List<String> secContent) {
        List<Pair<String, Cmd.CmdOp>> result = new ArrayList<>();
        int i = 0;
        while (i < secContent.size()) {
            // dealing with the first indent
            int l = i;
            i ++;
            while (i < secContent.size() && !secContent.get(i).trim().startsWith(name + " ")) {
                i ++;
            }
            List<String> subContent = secContent.subList(l, i);

            if (subContent.size() == 0)
                System.err.println("[Error@ParseSynopsis] An empty synopsis.");

            String cmdRaw = subContent.stream().reduce(" ", String::concat).replaceAll("\\s+", " ").trim();
            String cmdName = cmdRaw.split("\\s+")[0];
            cmdRaw = cmdRaw.substring(cmdRaw.indexOf(cmdName) + cmdName.length()).trim();
            try {
                result.add(new Pair(cmdName, parseSynopsisInstance(cmdRaw)));
            } catch (ParseException e) {
                continue;
            }
        }
        return result;
    }

    private static Cmd.CmdOp parseSynopsisInstance(String line) throws ParseException {
        Cmd.CmdOp op = new SynopParser(new java.io.StringReader(line)).compoundOp();
        return op;

    }

    /**
     * Parse descriptions in the
     * @param lines representing the body of descriptions of a file
     * @return a Pair:
     *      the key of the pair is an overview of the description,
     *      the value is a list of pairs, (optionName, optionDescription)
     */
    private static Pair<String, List<Pair<String, String>>> parseDescription(List<String> lines) {
        // parse descriptions
        int i = 0, l = i;
        String instrdesc = "";

        int baseIndention = indentCount(lines.get(0));

        while (i < lines.size()) {
            if ((indentCount(lines.get(i)) == baseIndention) && lines.get(i).trim().startsWith("-"))
                break;
            else
                i ++;
        }

        if (i != 0)
            instrdesc = lines.subList(l, i-2).stream().reduce("", (x,y) -> x + "\n" + y).replaceFirst("\\s+$", "");

        // start parsing options
        List<Pair<String, String>> optionList = new ArrayList<>();

        while (i < lines.size()) {
            if (!(indentCount(lines.get(i)) == baseIndention && lines.get(i).trim().startsWith("-")))
                break;
            String optionName = lines.get(i).trim().split("  ")[0];
            //System.out.println(optionName);
            l = i;
            i ++;
            while (i < lines.size() && !(indentCount(lines.get(i)) == baseIndention)) {
                i ++;
            }
            String optionDesc = lines.subList(l, i).stream().reduce("", (x,y) -> x + "\n" + y);
            //System.out.println(optionDesc);
            optionList.add(new Pair(optionName, optionDesc));
        }
        return new Pair(instrdesc, optionList);
    }

    private static List<Pair<String, String>> parseExample(List<String> lines) {
        // TODO
        return new ArrayList<>();
    }

    private static int indentCount(String s) { return s.indexOf(s.trim()); }

}
