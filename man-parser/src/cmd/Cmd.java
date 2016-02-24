package cmd;

import javafx.util.Pair;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 * Created by clwang on 2/14/16.
 */
public class Cmd {

    public static class ManPage {
        public List<String> aliases = new ArrayList<>();
        public String description = "";
        // one option may have more than once synopsis
        public List<Cmd.CmdOp> optionLists = new ArrayList<>();
        public List<DescriptionPair> optionDesc = new ArrayList<>();

        public void setName(List<String> aliases, String description) {
            this.aliases = aliases;
            this.description = description;
        }

        public String getName() { return this.aliases.get(0); }

        public String toString() {
            String s = "  " + aliases.stream().reduce("", String::concat) + "\r\n";
            s+="Synopsis\r\n";
            for (Cmd.CmdOp op : optionLists) {
                    s += op.toString() + "  ";
                s += "\r\n";
            }
            s += "Description\r\n";
            for (DescriptionPair p : optionDesc) {
                s += p.toString();
            }
            return s;
        }
    }

    public interface CmdOp { }
    // flag of form -flagname
    public static class Fl implements CmdOp {
        public String flagName;
        public Fl(String s) {
            this.flagName = s;
            if (this.flagName.startsWith("-")) {
                this.flagName = this.flagName.substring(1);
            }
        }
        public Fl() {}
        public String toString() {
            String flag = "-" + flagName;
            return flag;
        }
    }
    // another type of flag, with --flagname=arg
    public static class Flv2 implements CmdOp {
        public String flagName;
        // whether there exists arg
        boolean existArg = false;
        // whether the arg is of the form [=XXX] or =XXX
        boolean isOptionalArg = false;
        String arg = "";
        public Flv2(String flagname) {
            this.flagName = flagname;
        }
        public void setName(String arg, boolean isOptionalArg) {
            this.existArg = true;
            this.arg = arg;
            this.isOptionalArg = isOptionalArg;
        }
        public String toString() {
            String result = "--" + flagName.toString();
            if (existArg) {
                if (isOptionalArg)
                    result += "[=" + arg.toString() + "]";
                else
                    result += "=" + arg.toString();
            }
            return result;
        }
    }
    public static class Opt implements CmdOp {
        public String type = "optional";
        public CmdOp cmd;
        public Opt(CmdOp cmd) { this.cmd = cmd; }
        public Opt() {}
        public String toString() {
            return "[" + cmd.toString() + "]";
        }
    }
    public static class Ar implements CmdOp {
        public String type = "argument";
        public String argname;
        public boolean isList = false;
        public Ar() {};
        public Ar(String s) { this.argname = s; }
        public String toString() {
            if (isList) return argname + "...";
            else return argname;
        }
    }
    public static class Compound implements CmdOp {
        public String type = "compound";
        public List<CmdOp> cmds = new ArrayList<>();
        public Compound(List<CmdOp> cmds) { this.cmds = cmds; }
        public String toString() { return cmds.stream().map(cmd -> cmd.toString()).reduce(" ", (x,y) -> x + " " + y); }
    }
    public static class Exclusive implements CmdOp {
        public String type = "eclusive";
        public List<CmdOp> cmds = new ArrayList<>();
        public Exclusive(List<CmdOp> cmds) { this.cmds = cmds; }
        public String toString() {
            String s = "";
            for (CmdOp flg : cmds) {
                s += flg + " | ";
            }
            return s;
        }
    }

    public static class DescriptionPair {
        public String name;
        public Cmd.CmdOp option;
        public String description;

        public DescriptionPair(Pair<Cmd.CmdOp, String> p) {
            this(p.getKey(), p.getValue());
        }

        public DescriptionPair(Cmd.CmdOp fst, String desc) {
            this.name = fst.toString();
            this.option = fst;
            this.description = desc;
        }

        public String toString() {
            return  option.toString() + " :: " + description;
        }
    }
}
