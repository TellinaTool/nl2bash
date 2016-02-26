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

    public static class Command {
        public String type = "command";
        public String name = "";
        public CmdOp option;
        public Command() {};
        public Command(String name, CmdOp op) {
            this.name = name;
            this.option = op;
        }
        public String toString() {
            return name + " " + option.toString();
        }
    }

    public interface CmdOp { }
    // flag of form -flagname
    public static class Fl implements CmdOp {
        public String type = "flag_option";
        public String flag_name;
        public Fl(String s) {
            this.flag_name = s;
            if (this.flag_name.startsWith("-")) {
                this.flag_name = this.flag_name.substring(1);
            }
        }
        public Fl() {}
        public String toString() {
            String flag = "-" + flag_name;
            return flag;
        }
    }
    // another type of flag, with --flagname=arg
    public static class Flv2 implements CmdOp {
        public String type = "long_flag_option";
        public String flag_name;
        // whether there exists arg
        public boolean arg_exists = false;
        // whether the arg is of the form [=XXX] or =XXX
        public boolean arg_optional = false;
        public Ar argument = new Ar();
        public Flv2(String flagname) {
            this.flag_name = flagname;
        }
        public void setName(String arg, boolean arg_optional) {
            this.arg_exists = true;
            this.argument = new Ar(arg);
            this.arg_optional = arg_optional;
        }
        public String toString() {
            String result = "--" + flag_name.toString();
            if (arg_exists) {
                if (arg_exists)
                    result += "[=" + argument.toString() + "]";
                else
                    result += "=" + argument.toString();
            }
            return result;
        }
    }
    public static class Opt implements CmdOp {
        public String type = "optional_option";
        public CmdOp cmd;
        public Opt(CmdOp cmd) { this.cmd = cmd; }
        public Opt() {}
        public String toString() {
            return "[" + cmd.toString() + "]";
        }
    }
    public static class Ar implements CmdOp {
        public String type = "argument_option";
        public String arg_name;
        public String arg_type;
        public boolean isList = false;
        public Ar() {};
        public Ar(String s) {
            this.arg_name = s;
            if (this.arg_name.equalsIgnoreCase("file")
                    || this.arg_name.equalsIgnoreCase("f")
                    || this.arg_name.equalsIgnoreCase("source")
                    || this.arg_name.equalsIgnoreCase("target")) {
                arg_type = "File";
            } else if (this.arg_name.equalsIgnoreCase("number")
                    || this.arg_name.equalsIgnoreCase("n")
                    || this.arg_name.equalsIgnoreCase("num")) {
                arg_type = "Number";
            } else if (this.arg_name.equalsIgnoreCase("mode")) {
                arg_type = "PermissionMode";
            } else if (this.arg_name.equalsIgnoreCase("uname")) {
                arg_type = "Username";
            } else if (this.arg_name.equalsIgnoreCase("gname")) {
                arg_type = "Groupname";
            } else if (this.arg_name.equalsIgnoreCase("pattern")) {
                arg_type = "Pattern";
            } else if (this.arg_name.equalsIgnoreCase("time")) {
                arg_type = "Time";
            } else if (this.arg_name.equalsIgnoreCase("size")) {
                arg_type = "Size";
            } else {
                arg_type = "Unknown";
            }
        }
        public String toString() {
            if (isList) return arg_name + "...";
            else return arg_name;
        }
    }
    public static class Compound implements CmdOp {
        public String type = "compound_options";
        public List<CmdOp> commands = new ArrayList<>();
        public Compound(List<CmdOp> cmds) { this.commands = cmds; }
        public String toString() { return commands.stream().map(cmd -> cmd.toString()).reduce(" ", (x,y) -> x + " " + y); }
    }
    public static class Exclusive implements CmdOp {
        public String type = "exclusive_options";
        public List<CmdOp> commands = new ArrayList<>();
        public Exclusive(List<CmdOp> cmds) { this.commands = cmds; }
        public String toString() {
            String s = "";
            for (CmdOp flg : commands) {
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
