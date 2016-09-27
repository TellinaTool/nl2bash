package main;

import cmd_parser.CmdParserInterface;
import cmd_parser.parser.CommandsParser;
import man_parser.cmd.Cmd;
import man_parser.parser.ParseException;
import man_parser.ManParserInterface;
import org.antlr.v4.runtime.tree.ParseTree;

import java.io.IOException;
import java.util.List;

public class Main {

    public static void main(String[] args) throws IOException, ParseException {
        //ManParserInterface.parseSynopsisBNF();

        List<Cmd.Command> commands = ManParserInterface.parsePrimitiveGrammar(Config.SynopsisGrammar);

        String cmd = "mv -f -v ./src/file.text ./src/file.text2 ../../dst";

        System.out.println(CmdParserInterface.parse(cmd));
        CmdParserInterface.genG4(commands);
    }
}
