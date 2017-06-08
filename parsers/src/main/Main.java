package main;

import cmd_parser.CmdGrammarGenerator;
import cmd_parser.CmdParserInterface;
import javafx.util.Pair;
import man_parser.parser.ParseException;
import man_parser.ManParserInterface;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;

public class Main {

    public static void main(String[] args) throws IOException, ParseException {

        if (args.length < 1) {
            Main.printRunningInstruction();
            return;
        }

        if (args[0].equals("-make_grammar")) {
            String g4 = genG4FromSynopsis();

            if (args.length == 1) {
                System.out.println(g4);
                //Config.SynopsisGrammar = args[1];
            } else {
                String targetFile = args[1];
                //a typical location "src/cmd_parser/parser/Commands.g4";
                Files.write(Paths.get(targetFile), g4.getBytes());
            }
        } else if (args[0].equals("-parse")) {
            Pair<String, String> p = CmdParserInterface.parse(args[1]);
            System.out.println(p.getKey() + "\n" + p.getValue());
        } else if (args[0].equals("-parse_file")) {
            Files.lines(Paths.get(args[0])).forEach(x -> {
                Pair<String, String> p = CmdParserInterface.parse(x);
                System.out.println(p.getKey() + "\n" + p.getValue());
            });
        } else if (args[0].equals("-test")) {
            if (args.length >= 2 && args[1].equals("-print-fail"))
                testParseCmd(true);
            else
                testParseCmd(false);
        } else if (args[0].equals("-gen-primitive-cmd-json")) {
            if (args.length < 3)
                Main.printRunningInstruction();
            Config.OptionWordDictionary = args[2];
            Config.SynopsisGrammar = args[1];
            System.out.println(ManParserInterface.parseSynopsisBNF());
        } else if (args[0].equals("-parse_manpage")) {
            ManParserInterface.parseManPage(true);
        }

        //ManParserInterface.parseGrammarFile(Config.SynopsisGrammar);
        //testParseCmd();
    }

    private static void printRunningInstruction() {
        System.out.println("Usages: java -jar command_parser -parse command");
        System.out.println("    [1] Parse a command:");
        System.out.println("        java -jar command_parser -parse command");
        System.out.println("    [2] Parse all commands in a file, each command in a line.");
        System.out.println("        java -jar command_parser -parse_file filename");
        System.out.println("    [3] Test the parse result on the default given file.");
        System.out.println("        java -jar command_parser -test [-print-fail]");
        System.out.println("    [4] Build the json representation of the command grammar, with the help of optionword.");
        System.out.println("        java -jar command_parser -gen-primitive-cmd-json grammar_file optionword");
        System.out.println("    [5] Generate g4 grammar file: (you may want to generate to \"src/cmd_parser/parser/Commands.g4\")");
        System.out.println("        java -jar command_parser -make-grammar [target_file]");
        System.out.println("    [6] Parse plain text manpages into a json file, which is used in explaining commands.");
        System.out.println("        java -jar command_parser -parse_manpage");

    }

    public static String genG4FromSynopsis() {
        ManParserInterface.GrammarFile gf = null;
        try {
            gf = ManParserInterface.parseGrammarFile(Config.SynopsisGrammar);
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return CmdGrammarGenerator.genG4(gf.commandsGrammar, gf.nonTerminals, null);
    }

    public static void testParseCmd(boolean printFail) throws IOException {
        String[] cmds = {
                "find -E -L /home/peter -name *~ -print0 | xargs -0 rm {}",
                "find -L -E /home/peter -name *~ -print0 | xargs -0 rm {}",
                "find -L -E /home/peter -print0 -name *~ | xargs -0 rm {}",
                "find / -nouser -ok rm {} ;",
                "find . -ctime -22",
                "find -L /home/peter -name *~ -print0 | xargs -0 -r rm {}",
                "find . -name \"*.svg.png\" -print0 | sed 's/.svg.png//g' | xargs -0 -I namePrefix mv namePrefix.svg.png namePrefix.png",
                "find . -name '*[+{;\"\\\\=?~()<>&*|$ ]*' -exec rm -f {} ;",
                "grep -A3 -B 3 -C434",
                "find  /home/mine -iname \"*.png\" -printf \"%P\\n \" | xargs  -I % -n1 cp %  /home/mine/pngcoppies/copy%",
                "find / -xdev -name document -print"
        };

        for (String cmd : cmds) {
           // System.out.println(cmd);
            //System.out.println(CmdParserInterface.parse(cmd));
        }

       //if (cmds.length > 0)
         //   return;

        String testDataPath = "test_data/train.correct.cm";

        //System.err
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        System.setErr(new PrintStream(baos));

        Files.lines(Paths.get(testDataPath)).forEach(
            x -> {
                String s = x.replace("\\)", ")").replace("\\(", "(").replace("\\;", ";");
                Pair<String, String> cmdParsedPair = CmdParserInterface.parse(s);
                String parseLog = new String( baos.toByteArray(), Charset.defaultCharset() );
                if (! parseLog.trim().equals("")) {
                    //print unparsed commands
                    if (printFail)
                        System.out.println("[Failed to parse] " + s);
                } else {
                    // print parsed commands
                    if (!printFail) {
                        System.out.println(s);
                        System.out.println(cmdParsedPair.getKey() + "\n" + cmdParsedPair.getValue());
                    }
                }
                baos.reset();
            }
        );
    }
}
