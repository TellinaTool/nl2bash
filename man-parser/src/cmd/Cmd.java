package cmd;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 * Created by clwang on 2/14/16.
 */
public class Cmd {

    public static class ManPage {
        List<String> aliases = new ArrayList<>();
        String description = "";
        // one option may have more than once synopsis
        List<List<Cmd.CmdOp>> optionLists = new ArrayList<>();

        public void setName(List<String> aliases, String description) {
            this.aliases = aliases;
            this.description = description;
        }

        public String getName() { return this.aliases.get(0); }

        public String toString() {
            String s = aliases.stream().reduce("", String::concat) + "\r\n";
            for (List<Cmd.CmdOp> list : optionLists) {
                for (Cmd.CmdOp op : list)
                    s += op.toString() + "  ";
                s += "\r\n";
            }
            return s;
        }
    }

    public interface CmdOp { }
    // flag of form -flagname
    public static class Fl implements CmdOp {
        public String flagName;
        public Fl(String s) { this.flagName = s; }
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
        public CmdOp cmd;
        public Opt(CmdOp cmd) { this.cmd = cmd; }
        public Opt() {}
        public String toString() {
            return "[" + cmd.toString() + "]";
        }
    }
    public static class Ar implements CmdOp {
        public String name;
        public boolean isList = false;
        public Ar() {};
        public Ar(String s) { this.name = s; }
        public String toString() {
            if (isList) return name + "...";
            else return name;
        }
    }
    public static class Compound implements CmdOp {
        public List<CmdOp> cmds = new ArrayList<>();
        public Compound(List<CmdOp> cmds) { this.cmds = cmds; }
        public String toString() { return cmds.stream().map(cmd -> cmd.toString()).reduce(" ", (x,y) -> x + " " + y); }
    }
    public static class Exclusive implements CmdOp {
        public List<CmdOp> args = new ArrayList<>();
        public Exclusive(List<CmdOp> cmds) { this.args = cmds; }
        public String toString() {
            String s = "";
            for (CmdOp flg : args) {
                s += flg + " | ";
            }
            return s;
        }
    }
}
