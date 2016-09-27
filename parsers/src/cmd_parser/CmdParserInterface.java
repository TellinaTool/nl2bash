package cmd_parser;

import man_parser.cmd.Cmd;
import org.antlr.v4.runtime.ANTLRInputStream;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;

import cmd_parser.parser.*;

import java.util.List;


/**
 * Created by clwang on 9/26/16.
 */
public class CmdParserInterface {

    public static String parse(String command) {
        CommandsLexer lexer = new CommandsLexer(new ANTLRInputStream(command));
        CommonTokenStream tokens = new CommonTokenStream( lexer );

        CommandsParser parser = new CommandsParser(tokens);
        ParseTree tree = parser.command();
        return tree.toStringTree(parser);
    }

    public static void genG4(List<Cmd.Command> commands) {
        for (Cmd.Command cmd : commands)
            System.out.println(cmd);
    }
}
