import cmd.Cmd;
import com.sun.org.apache.bcel.internal.ExceptionConstants;
import com.sun.org.apache.xerces.internal.util.SynchronizedSymbolTable;
import javafx.util.Pair;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;
import parser.*;

public class Main {

    static boolean trySmallExample = true;

    public static void main(String[] args) throws IOException {

        File[] files = new File("../data/plain-man").listFiles();

        if (trySmallExample) {
            parseFile(new File("../data/plain-man/grep.1.txt"));
            return;
        }

        for (File f : files) {
            if (! f.getName().matches("\\w*\\.\\d\\.txt"))
                continue;
            parseFile(f);
        }
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
                                    new Pair(parseSynopsisInstance(optionPart.substring(0, k)), desc.getValue()));
                                added = true;
                            } catch (Exception e) {
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
                                    new Pair(parseSynopsisInstance(optionPart), desc.getValue()));
                        } catch (Exception e) {
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
            result.add(new Pair(cmdName, parseSynopsisInstance(cmdRaw)));
        }
        return result;
    }

    private static Cmd.CmdOp parseSynopsisInstance(String line) {
        String name = "";
        try {
            Cmd.CmdOp op = new SynopParser(new java.io.StringReader(line)).compoundOp();
            return op;
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return null;
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
        while (i < lines.size()) {
            if ((indentCount(lines.get(i)) == 5) && lines.get(i).trim().startsWith("-"))
                break;
            else
                i ++;
        }
        instrdesc = lines.subList(l, i-2).stream().reduce("", (x,y) -> x + "\n" + y).replaceFirst("\\s+$", "");

        // start parsing options
        List<Pair<String, String>> optionList = new ArrayList<>();

        while (i < lines.size()) {
            if (!(indentCount(lines.get(i)) == 5 && lines.get(i).trim().startsWith("-")))
                break;
            String optionName = lines.get(i).trim().split("  ")[0];
            //System.out.println(optionName);
            l = i;
            i ++;
            while (i < lines.size() && !(indentCount(lines.get(i)) == 5)) {
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
