package main;

import cmd_parser.CmdGrammarGenerator;
import cmd_parser.CmdParserInterface;
import man_parser.parser.ParseException;
import man_parser.ManParserInterface;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class Main {

    public static void main(String[] args) throws IOException, ParseException {
        if (args.length < 2) {
            System.out.println("usage: java -jar command_parser -parse command");
            System.out.println("       java -jar command_parser -parse_file filename");
            // System.out.println("       java -jar command_parser -make_grammar grammar_file");
            return;
        }

        if (args[0].equals("-make_grammar")) {
            Config.SynopsisGrammar = args[1];
            String g4 = genG4FromSynopsis();
            System.out.println(g4);
        } else if (args[0].equals("-parse")) {
            System.out.println(CmdParserInterface.parse(args[1]));
        } else if (args[0].equals("-parse_file")) {
            Files.lines(Paths.get(args[0])).forEach(x -> System.out.println(CmdParserInterface.parse(x)));
        }

        //ManParserInterface.parseGrammarFile(Config.SynopsisGrammar);
        //genG4FromSynopsis();
        //testParseCmd();
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

    public static void testParseCmd() {
        String[] cmds = {
            "mv -f -v ./src/file.text ./src/file.text2 ../../dst",
            "find . -name '*~' -print0",
            "find . -exec util {} -name \"*java*\" ",
            "find xargstest/ -name 'file??'"
        };

        for (String cmd : cmds) {
            System.out.println(CmdParserInterface.parse(cmd));
        }
    }
}
