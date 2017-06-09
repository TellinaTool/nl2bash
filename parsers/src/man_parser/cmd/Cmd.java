package man_parser.cmd;

import javafx.util.Pair;
import man_parser.ManParserInterface;
import man_parser.parser.ParseException;
import man_parser.parser.SynopParser;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by clwang on 2/14/16.
 */
public class Cmd {

    public static Map<String, String> ConstantArgDict = new HashMap<>();
    public static Map<String, String> NameToTypeDict = new HashMap<>();

    public static class ManPage {
        public List<String> aliases = new ArrayList<>();
        public String description = "";
        public String rawSynopsis = "";

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
        public Command(String name, CmdOp op) {
            this.name = name;
            this.option = op;
        }
        public String toString() {
            return name + " " + option.toString();
        }
    }

    public interface CmdOp {
        String getType();
    }
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
        public String toString() {
            String flag = "-" + flag_name;
            return flag;
        }
        @Override
        public String getType() {
            return type;
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
        @Override
        public String getType() {
            return type;
        }
    }
    public static class Opt implements CmdOp {
        public String type = "optional_option";
        public CmdOp cmd;
        public Opt(CmdOp cmd) { this.cmd = cmd; }
        public String toString() {
            return "[" + cmd.toString() + "]";
        }
        @Override
        public String getType() {
            return type;
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
        @Override
        public String getType() {
            return type;
        }
    }
    public static class NonTerminal implements CmdOp {
        public String type = "argument_option";
        public String name;
        public boolean isList = false;
        public NonTerminal(String s) {
            name = s;
        }
        public String toString() {
            if (isList) return ":" + name + ": " + "...";
            else return ":" + name + ":";
        }
        @Override
        public String getType() {
            return type;
        }
    }
    public static class Compound implements CmdOp {
        public String type = "compound_options";
        public List<CmdOp> commands = new ArrayList<>();
        public Compound(List<CmdOp> cmds) { this.commands = cmds; }
        public String toString() {
            return commands.stream().map(cmd -> cmd.toString()).reduce(" ", (x,y) -> x + " " + y);
        }
        @Override
        public String getType() {
            return type;
        }
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
        @Override
        public String getType() {
            return type;
        }
    }

    public static class DescriptionPair {
        String type = "option_description_pair";
        public String name;
        public CmdOp option;
        public List<CmdOp> allOptions = new ArrayList<>();
        public String description;

        public DescriptionPair(CmdOp fst, String wholeOpPart, String desc) {
            this.name = fst.toString().trim();
            this.option = fst;
            this.description = desc;
            this.addAllOptions(wholeOpPart);
        }

        public void addAllOptions(String allOptions) {
            for (String s : allOptions.split(",")) {
                try {
                    this.allOptions.add(new SynopParser(new java.io.StringReader(s)).compoundOp());
                } catch (ParseException e) {
                    e.printStackTrace();
                }
            }
        }
        public String toString() {
            return  option.toString() + " :: " + description;
        }

        public String pureOptions() {
            String synOp = "[";
            for (int i = 0; i < allOptions.size(); i ++) {
                if (i != 0)
                    synOp += "|";
                synOp += " " + allOptions.get(i).toString() + " ";

            }
            synOp += "]";
            return synOp;
        }
    }

    private static Pair<String, String> normalizeArgNameType(String argName) {

        if (NameToTypeDict.containsKey(argName)) {
            return new Pair<>(argName, NameToTypeDict.get(argName));
        } else if (ConstantArgDict.containsKey(argName)) {
            return new Pair<>(ConstantArgDict.get(argName), "Constant");
        } else {
            return new Pair<>(argName, "Unknown");
        }

    }
}
