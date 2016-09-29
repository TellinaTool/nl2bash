package main;

import cmd_parser.CmdGrammarGenerator;
import cmd_parser.CmdParserInterface;
import man_parser.cmd.Cmd;
import man_parser.parser.ParseException;
import man_parser.ManParserInterface;

import java.io.IOException;
import java.util.List;

public class Main {

    public static void main(String[] args) throws IOException, ParseException {
        //ManParserInterface.parseGrammarFile(Config.SynopsisGrammar);
        //genG4FromSynopsis();
        testParseCmd();
    }

    public static void genG4FromSynopsis() {
        ManParserInterface.GrammarFile gf = null;
        try {
            gf = ManParserInterface.parseGrammarFile(Config.SynopsisGrammar);
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ParseException e) {
            e.printStackTrace();
        }
        System.out.println(CmdGrammarGenerator.genG4(gf.commandsGrammar, gf.nonTerminals, null));
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
