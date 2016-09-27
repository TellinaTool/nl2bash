package man_parser.cmd;

import javafx.util.Pair;
import org.antlr.v4.runtime.tree.ParseTree;

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
            if (this.flag_name.equals("ONE")) this.flag_name = "1";
            if (this.flag_name.equals("TWO")) this.flag_name = "2";
            if (this.flag_name.equals("THREE")) this.flag_name = "3";
            if (this.flag_name.equals("EXCLAMATION")) this.flag_name = "!";
            if (this.flag_name.equals("DOLLAR")) this.flag_name = "$";
            if (this.flag_name.equals("AT")) this.flag_name = "@";

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
        public Ar() {}
        public Ar(String s) {
            Pair<String, String> p = normalizeArgNameType(s);
            this.arg_name  = p.getKey();
            this.arg_type = p.getValue();
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

    private static Pair<String, String> normalizeArgNameType(String argName) {
        String arg_name = argName;
        String arg_type = "Unknown";

        if (arg_name.equalsIgnoreCase("file")
                || arg_name.equalsIgnoreCase("f")
                || arg_name.equalsIgnoreCase("source_file")
                || arg_name.equalsIgnoreCase("target_file")
                || arg_name.equalsIgnoreCase("xfile")
                || arg_name.equalsIgnoreCase("file1")
                || arg_name.equalsIgnoreCase("file2")
                || arg_name.equalsIgnoreCase("filename")
                || arg_name.equalsIgnoreCase("directory")
                || arg_name.equalsIgnoreCase("exdir")
                || arg_name.equalsIgnoreCase("dir")
                || arg_name.equalsIgnoreCase("path")
                || arg_name.equalsIgnoreCase("progfile")
                || arg_name.equalsIgnoreCase("command_file")
                || arg_name.equalsIgnoreCase("zipfile")
                || arg_name.equalsIgnoreCase("archive-file")) {
            arg_type = "File";
        } else if (arg_name.equalsIgnoreCase("number")
                || arg_name.equalsIgnoreCase("n")
                || arg_name.equalsIgnoreCase("replacements")
                || arg_name.equalsIgnoreCase("maxprocs")
                || arg_name.equalsIgnoreCase("incr")
                || arg_name.equalsIgnoreCase("bytes")
                || arg_name.equalsIgnoreCase("mask")
                || arg_name.equalsIgnoreCase("num")
                || arg_name.equalsIgnoreCase("depth")
                || arg_name.equalsIgnoreCase("MINUSa")
                || arg_name.equalsIgnoreCase("PLUSa")
                || arg_name.equalsIgnoreCase("EQUALa")
                || arg_name.equalsIgnoreCase("count")
                || arg_name.equalsIgnoreCase("nmin")
                || arg_name.equalsIgnoreCase("a")) {
            arg_type = "Number";
        } else if (arg_name.equalsIgnoreCase("permmode")
                || arg_name.equalsIgnoreCase("MINUSpermmode")
                || arg_name.equalsIgnoreCase("PLUSpermmode")) {
            arg_type = "Permission";
        } else if (arg_name.equalsIgnoreCase("uname")
                || arg_name.equalsIgnoreCase("gname")
                || arg_name.equalsIgnoreCase("eofstr")
                || arg_name.equalsIgnoreCase("replstr")
                || arg_name.equalsIgnoreCase("string")
                || arg_name.equalsIgnoreCase("command")
                || arg_name.equalsIgnoreCase("extension")
                || arg_name.equalsIgnoreCase("option")
                || arg_name.equalsIgnoreCase("name")
                || arg_name.equalsIgnoreCase("MINUSflags")
                || arg_name.equalsIgnoreCase("PLUSflags")
                || arg_name.equalsIgnoreCase("flags")
                || arg_name.equalsIgnoreCase("type")
                || arg_name.equalsIgnoreCase("t")
                || arg_name.equalsIgnoreCase("findexp")
                || arg_name.equalsIgnoreCase("tar_format")
                || arg_name.equalsIgnoreCase("options")
                || arg_name.equalsIgnoreCase("program")
                || arg_name.equalsIgnoreCase("format")
                || arg_name.equalsIgnoreCase("varEQvalue")
                || arg_name.equalsIgnoreCase("prog")
                || arg_name.equalsIgnoreCase("owner")
                || arg_name.equalsIgnoreCase("first")
                || arg_name.equalsIgnoreCase("last")
                || arg_name.equalsIgnoreCase("suffixes")
                || arg_name.equalsIgnoreCase("list")) {
            arg_type = "String";
        } else if (arg_name.equalsIgnoreCase("pattern")
                || arg_name.equalsIgnoreCase("fs")) {
            arg_type = "Pattern";
        } else if (arg_name.equalsIgnoreCase("time")
                || arg_name.equalsIgnoreCase("date")) {
            arg_type = "Time";
        } else if (arg_name.equalsIgnoreCase("size")
                || arg_name.equalsIgnoreCase("blocksize")) {
            arg_type = "Size";
        } else if (arg_name.equalsIgnoreCase("utility")) {
            arg_type = "Utility";
        } else if (arg_name.equalsIgnoreCase("argument")) {
            arg_type = "Argument";
        } else if (arg_name.equalsIgnoreCase("SEMICOLON"))  {
            arg_type = "Constant";
            arg_name = ";";
        } else if (arg_name.equalsIgnoreCase("PLUS"))  {
            arg_type = "Constant";
            arg_name = "+";
        } else if (arg_name.equalsIgnoreCase("EXCLAMATION"))  {
            arg_type = "Constant";
            arg_name = "!";
        } else if (arg_name.equalsIgnoreCase("BRACKETS")
                || arg_name.equals("{}"))  {
            arg_type = "Constant";
            arg_name = "{}";
        }  else if (arg_name.equalsIgnoreCase("ACE"))  {
            arg_type = "Constant";
        } else {
            arg_type = "Unknown";
        }

        return new Pair<>(arg_name, arg_type);
    }
}
