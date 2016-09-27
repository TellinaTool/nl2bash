package man_parser.cmd;

import javafx.util.Pair;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by clwang on 2/14/16.
 */
public class Cmd {

    public static class ManPage {
        String type = "man_parser";
        public List<String> aliases = new ArrayList<>();
        public String description = "";
        // one option may have more than once synopsis
        public List<CmdOp> optionLists = new ArrayList<>();
        public List<DescriptionPair> optionDesc = new ArrayList<>();

        public void setName(List<String> aliases, String description) {
            this.aliases = aliases;
            this.description = description;
        }

        public String getName() { return this.aliases.get(0); }

        public String toString() {
            String s = "  " + aliases.stream().reduce("", String::concat) + "\r\n";
            s+="Synopsis\r\n";
            for (CmdOp op : optionLists) {
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
                    || this.arg_name.equalsIgnoreCase("source_file")
                    || this.arg_name.equalsIgnoreCase("target_file")
                    || this.arg_name.equalsIgnoreCase("xfile")
                    || this.arg_name.equalsIgnoreCase("file1")
                    || this.arg_name.equalsIgnoreCase("file2")
                    || this.arg_name.equalsIgnoreCase("filename")
                    || this.arg_name.equalsIgnoreCase("directory")
                    || this.arg_name.equalsIgnoreCase("exdir")
                    || this.arg_name.equalsIgnoreCase("path")
                    || this.arg_name.equalsIgnoreCase("progfile")) {
                arg_type = "File";
            } else if (this.arg_name.equalsIgnoreCase("number")
                    || this.arg_name.equalsIgnoreCase("n")
                    || this.arg_name.equalsIgnoreCase("replacements")
                    || this.arg_name.equalsIgnoreCase("maxprocs")
                    || this.arg_name.equalsIgnoreCase("incr")
                    || this.arg_name.equalsIgnoreCase("bytes")
                    || this.arg_name.equalsIgnoreCase("mask")
                    || this.arg_name.equalsIgnoreCase("num")
                    || this.arg_name.equalsIgnoreCase("depth")
                    || this.arg_name.equalsIgnoreCase("MINUSa")
                    || this.arg_name.equalsIgnoreCase("PLUSa")
                    || this.arg_name.equalsIgnoreCase("EQUALa")
                    || this.arg_name.equalsIgnoreCase("count")
                    || this.arg_name.equalsIgnoreCase("nmin")) {
                arg_type = "Number";
            } else if (this.arg_name.equalsIgnoreCase("permmode")
                    || this.arg_name.equalsIgnoreCase("MINUSpermmode")
                    || this.arg_name.equalsIgnoreCase("PLUSpermmode")) {
                arg_type = "Permission";
            } else if (this.arg_name.equalsIgnoreCase("uname")
                    || this.arg_name.equalsIgnoreCase("gname")
                    || this.arg_name.equalsIgnoreCase("eofstr")
                    || this.arg_name.equalsIgnoreCase("replstr")
                    || this.arg_name.equalsIgnoreCase("string")
                    || this.arg_name.equalsIgnoreCase("command")
                    || this.arg_name.equalsIgnoreCase("extension")
                    || this.arg_name.equalsIgnoreCase("option")
                    || this.arg_name.equalsIgnoreCase("name")) {
                arg_type = "String";
            } else if (this.arg_name.equalsIgnoreCase("pattern")
                    || this.arg_name.equalsIgnoreCase("fs")) {
                arg_type = "Pattern";
            } else if (this.arg_name.equalsIgnoreCase("time")
                    || this.arg_name.equalsIgnoreCase("date")) {
                arg_type = "Time";
            } else if (this.arg_name.equalsIgnoreCase("size")
                    || this.arg_name.equalsIgnoreCase("blocksize")) {
                arg_type = "Size";
            } else if (this.arg_name.equalsIgnoreCase("utility")) {
                arg_type = "Utility";
            } else if (this.arg_name.equalsIgnoreCase("argument")) {
                arg_type = "Argument";
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
        String type = "option_description_pair";
        public String name;
        public CmdOp option;
        public String description;

        public DescriptionPair(Pair<CmdOp, String> p) {
            this(p.getKey(), p.getValue());
        }

        public DescriptionPair(CmdOp fst, String desc) {
            this.name = fst.toString();
            this.option = fst;
            this.description = desc;
        }

        public String toString() {
            return  option.toString() + " :: " + description;
        }
    }
}
