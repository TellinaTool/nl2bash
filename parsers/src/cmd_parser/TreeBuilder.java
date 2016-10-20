package cmd_parser;

import org.antlr.v4.runtime.Parser;
import org.antlr.v4.runtime.tree.*;
import org.antlr.v4.tool.Rule;


/**
 * Created by clwang on 10/19/16.
 */
public class TreeBuilder extends AbstractParseTreeVisitor {

    Parser parser;

    public TreeBuilder(Parser p) {this.parser = p;}

    public String tryVisit(Object obj) {
        if (obj instanceof ParseTree) {
            return visit((ParseTree)obj);
        }
        else if (obj instanceof RuleNode) {
            return visitChildren((RuleNode) obj);
        } else if (obj instanceof TerminalNode) {
            return visitTerminal((TerminalNode) obj);
        }
        return "";
    }

    public void printParseTree(ParseTree node, int indent) {
        String ld = "";
        for (int i = 0; i < indent; i ++)
            ld += "  ";
        String str = "## " + node.getText();
        if (node.getChildCount() != 0)
            str = "NT: " + node.toStringTree(parser).split(" ")[0].substring(1);

        System.out.println(ld + str);

        for (int i = 0; i < node.getChildCount(); i ++) {
            printParseTree(node.getChild(i), indent + 1);
        }
    }

    public CmdTreeNode buildCmdTree(ParseTree node) {

        CmdTreeNode cmdNode = new CmdTreeNode();

        if (node.getChildCount() != 0)
            cmdNode.setContent(node.toStringTree(parser).split(" ")[0].substring(1));
        else
            cmdNode.setContent(node.getText());

        for (int i = 0; i < node.getChildCount(); i ++) {
            cmdNode.addChild(buildCmdTree(node.getChild(i)));
        }

        if (cmdNode.getContent().equals("find_primitive_exp"))
            return cmdNode.getChildren().get(0);

        return cmdNode;
    }

    public String getType(Object obj) {

        if (obj instanceof ParseTree) {
            return "ParseTree";
        }
        else if (obj instanceof RuleNode) {
            return "Rule";
        } else if (obj instanceof TerminalNode) {
            return "Terminal";
        }
        return "Other";
    }

    @Override
    public String visit(ParseTree parseTree) {
        printParseTree(parseTree, 0);
        String s = "";
        for (int i = 0; i < parseTree.getChildCount(); i ++) {
            s += " \n\t## "  + getType(parseTree.getChild(i)) + tryVisit(parseTree.getChild(i));
        }
        return "";
    }

    @Override
    public String visitChildren(RuleNode ruleNode) {
        String s = "~~~~";
        for (int i = 0; i < ruleNode.getChildCount(); i ++) {
            s += " \n\t\t&& " + tryVisit(ruleNode.getChild(i));
        }
        return ruleNode.getText() + " && " + s;
    }

    @Override
    public String visitTerminal(TerminalNode terminalNode) {
        return terminalNode.getText();
    }

    @Override
    public String visitErrorNode(ErrorNode errorNode) {
        return "NULL";
    }
}
