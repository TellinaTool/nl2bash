import cmd.Cmd;
import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.PropertyAccessor;
import javafx.util.Pair;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import parser.*;
import com.fasterxml.jackson.core.*;
import com.fasterxml.jackson.databind.*;

public class Main {

    static boolean trySmallExample = true;

    static final String PREFIX = "../../";

    public static void main(String[] args) throws IOException, ParseException {

        // // summarizing options of the file tar.1.txt
        // SmallTask.extractOptionsFrom("../data/plain-man/tar.1.txt");

        //jsonPrimitiveGrammar("../grammar.txt");

        /*String s = SmallTask.processWierdThing("wierddata");
        System.out.println(s);*/

        File[] files = new File(PREFIX +  "data/plain-man").listFiles();

        if (trySmallExample) {
            String[] targetFiles = {
                    PREFIX + "data/plain-man/grep.1.txt",
                    PREFIX + "data/plain-man/find_cheat.1.txt",
                    PREFIX + "data/plain-man/xargs.1.txt",
                    PREFIX + "data/plain-man/sort.1.txt",
                    PREFIX + "data/plain-man/cp.1.txt",
                    PREFIX + "data/plain-man/ls.1.txt",
                    PREFIX + "data/plain-man/tar.1.txt"
            };
            List<Cmd.ManPage> manPages = new ArrayList<>();
            for (String f : targetFiles) {
                manPages.add(parseFile(new File(f)));
            }
            ObjectMapper mapper = new ObjectMapper();
            String jsonInString = mapper.writeValueAsString(manPages);
            System.out.println(jsonInString);
            return;
        }

        for (File f : files) {
            if (! f.getName().matches("\\w*\\.\\d\\.txt"))
                continue;
            parseFile(f);
        }
    }

    public static String jsonPrimitiveGrammar(String path) throws IOException, ParseException {
        List<String> lines = Files.readAllLines(Paths.get(path));
        int i = 0;
        List<Cmd.Command> commands = new ArrayList<>();
        while (i < lines.size()) {
            if (lines.get(i).startsWith("PrimitiveCmd")) {
                i ++;
                int l = i;
                while (i < lines.size()) {
                    if (indentCount(lines.get(i)) == 0 && !lines.get(i).trim().equals(""))
                        break;
                    i ++;
                }
                System.out.println(+ l + " " + i);

                List<String> primitives = lines.subList(l, i)
                        .stream().filter(s -> !s.trim().equals("")).map(s -> s.trim()).collect(Collectors.toList());

                for (String s : primitives)
                    System.out.println("> " + s);

                for (String s : primitives) {
                    System.out.println(s);
                    String name = s.trim().split("\\s+")[0];
                    String raw = s.substring(s.indexOf(name) + name.length()).trim();
                    commands.add(new Cmd.Command(name, parseSynopsisInstance(raw)));
                }
            }
            i ++;
        }
        for (Cmd.Command cmd : commands) {
            System.out.println("=== \n" + cmd.toString());
        }


        ObjectMapper mapper = new ObjectMapper();
        mapper.setVisibility(PropertyAccessor.FIELD, JsonAutoDetect.Visibility.ANY);
        String jsonInString = mapper.writeValueAsString(commands);
        System.out.println(jsonInString);
        return "";
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
                manpage.setName(name.getKey(), name.getValue());
                continue;
            } else if (i < lines.size() && lines.get(i).startsWith("SYNOPSIS")) {
                // segmenting the synopsis section
                int l = i + 1;
                i ++;
                while (indentCount(lines.get(i)) != 0) {
                    i ++;
                }
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
                manpage.description += descSec.getKey();
                for (Pair<String, String> desc : descSec.getValue()) {
                    String optionPart = desc.getKey();
                    int inOuterLevel = 0;
                    boolean added = false;
                    for (int k = 0; k < optionPart.length(); k ++) {
                        if (optionPart.charAt(k) == ',' && inOuterLevel == 0) {
                            try {
                                manpage.optionDesc.add(
                                    new Cmd.DescriptionPair(parseSynopsisInstance(optionPart.substring(0, k)), desc.getValue()));
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
                                    new Cmd.DescriptionPair(parseSynopsisInstance(optionPart), desc.getValue()));
                        } catch (ParseException e) {
                            continue;
                        }
                    }
                }
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

        System.out.println(manpage.toString());
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
        String name = "";
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
