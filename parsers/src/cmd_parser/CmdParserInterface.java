package cmd_parser;

import org.antlr.v4.runtime.ANTLRInputStream;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;

import cmd_parser.parser.*;

/**
 * Created by clwang on 9/26/16.
 */
public class CmdParserInterface {

    public static String parse(String command) {
        CommandsLexer lexer = new CommandsLexer(new ANTLRInputStream(command));
        CommonTokenStream tokens = new CommonTokenStream( lexer );

        CommandsParser parser = new CommandsParser(tokens);
        ParseTree tree = parser.command();
        //printParseTree(tree, 0);



        CmdTreeNode cmdTree = new TreeBuilder(parser).buildCmdTree(tree);

        String s = cmdTree.toCommand();
        //System.out.println(cmdTree.toCommand());
        cmdTree.sortChildren();
        //System.out.println(cmdTree.toCommand());
        //cmdTree.prettyPrint(0);
        //System.out.println("=================================");


        //return tree.toStringTree(parser);
        return s + "\n" + cmdTree.toCommand() + "\n";
    }

    public static void printParseTree(ParseTree t, int indent) {

        String space = "";
        for (int i = 0; i < indent; i ++)
            space += "\t";

        System.out.println(space + "[[" + t.getText() + "]]");
        for (int i = 0; i < t.getChildCount(); i ++) {
            printParseTree(t.getChild(i), indent + 1);
        }
    }

}
