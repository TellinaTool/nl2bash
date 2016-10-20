package cmd_parser;

import javafx.util.Pair;

import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by clwang on 10/19/16.
 */
public class CmdTreeNode {


    Set<String> shouldNotReorder = new HashSet<String>(Arrays.asList("-print0", "-print", "-exec", "-prune")) ;

    public enum NodeType {
        notyetset, command, argument, option
    };

    String content;
    NodeType type = NodeType.notyetset;
    List<CmdTreeNode> children = new ArrayList<>();

    public String getContent() { return content;}
    public void setContent(String content) {this.content = content;}
    public NodeType getType() {return type;}
    public void setType(NodeType type) {this.type = type;}
    public List<CmdTreeNode> getChildren() {return children;}
    public void addChild(CmdTreeNode child) {this.children.add(child);}

    public CmdTreeNode() {}

    public void sortChildren() {

        for (CmdTreeNode t : children)
            t.sortChildren();

        List<CmdTreeNode> tempList = new ArrayList<>();
        for (CmdTreeNode n : this.children) {
            // sort option nodes
            if (isOption(n.getContent())) {

                String hd = getOpId(n.getContent()).getKey();
                int val = getOpId(n.getContent()).getValue();
                int i = tempList.size();

                while (i - 1 >= 0
                        && isOption(tempList.get(i-1).getContent())
                        && (! notReorder(tempList.get(i-1).toCommand().trim()))
                        && (! notReorder(n.toCommand().trim()))
                        && getOpId(tempList.get(i-1).getContent()).getKey().equals(hd)
                        && getOpId(tempList.get(i-1).getContent()).getValue() > val) {
                    i --;
                }
                tempList.add(i, n);
            } else {
                tempList.add(n);
            }
        }
        this.children = tempList;
    }

    public void prettyPrint(int indent) {
        String ld = "";
        for (int i = 0; i < indent; i ++)
            ld += "  ";
        String str = "### " + this.getContent();
        if (this.children.size() != 0)
            str = "NT: " + this.getContent()  + " ~~ " + isOption(this.getContent());

        System.out.println(ld + str);

        for (int i = 0; i < this.children.size(); i ++) {
            this.children.get(i).prettyPrint(indent + 1);
        }
    }

    public static boolean isOption(String content) {
        Pattern p = Pattern.compile("^.*_op(\\d)+$");
        Matcher m = p.matcher(content);
        return m.matches();
    }

    public static Pair<String, Integer> getOpId(String op)  {
        if (!isOption(op))
            return new Pair<>(op, 99999);
        return new Pair<>(op.substring(0, op.lastIndexOf("_op") + 3),
                Integer.parseInt(op.substring(op.lastIndexOf("_op") + 3)));
    }

    public String toCommand() {
        if (this.children.size() == 0)
            return this.getContent();

        if (this.getContent().startsWith("arg_"))
            return this.getContent();

        String s = "";
        for (int i = 0; i < this.children.size(); i ++) {
            s += " " + this.children.get(i).toCommand();
        }
        return s;
    }

    public boolean notReorder(String s) {
        for (String t : shouldNotReorder) {
            if (s.startsWith(t)) return true;
        }
        return false;
    }
}
