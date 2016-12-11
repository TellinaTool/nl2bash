package main;

import cmd_parser.CmdGrammarGenerator;
import cmd_parser.CmdParserInterface;
import man_parser.parser.ParseException;
import man_parser.ManParserInterface;
import org.antlr.v4.runtime.RecognitionException;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintStream;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;

public class Main {

    public static void main(String[] args) throws IOException, ParseException {

        if (args.length < 1) {
            System.out.println("usage: java -jar command_parser -parse command");
            System.out.println("       java -jar command_parser -parse_file filename");
            //System.out.println("       java -jar command_parser -make_grammar grammar_file");
            return;
        }

        args[0] = "-test";

        if (args[0].equals("-make_grammar")) {
            //Config.SynopsisGrammar = args[1];
            String g4 = genG4FromSynopsis();
            Files.write(Paths.get("src/cmd_parser/parser/Commands.g4"), g4.getBytes());
        } else if (args[0].equals("-parse")) {
            System.out.println(CmdParserInterface.parse(args[1]));
        } else if (args[0].equals("-parse_file")) {
            Files.lines(Paths.get(args[0])).forEach(x -> System.out.println(CmdParserInterface.parse(x)));
        } else if (args[0].equals("-test")) {
            testParseCmd();
        }

        //ManParserInterface.parseGrammarFile(Config.SynopsisGrammar);
        //testParseCmd();
    }

    public static String genG4FromSynopsis() {
        ManParserInterface.GrammarFile gf = null;
        try {
            gf = ManParserInterface.parseGrammarFile(Config.SynopsisGrammar);
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return CmdGrammarGenerator.genG4(gf.commandsGrammar, gf.nonTerminals, null);
    }

    public static void testParseCmd() throws IOException {
        String[] cmds = {
                "find -E -L /home/peter -name *~ -print0 | xargs -0 rm {}",
                "find -L -E /home/peter -name *~ -print0 | xargs -0 rm {}",
                "find -L -E /home/peter -print0 -name *~ | xargs -0 rm {}",
                "find / -nouser -ok rm {} ;",
                "find . -ctime -22",
                "find -L /home/peter -name *~ -print0 | xargs -0 -r rm {}",
                "find . -name \"*.svg.png\" -print0 | sed 's/.svg.png//g' | xargs -0 -I namePrefix mv namePrefix.svg.png namePrefix.png",
                "find . -name '*[+{;\"\\\\=?~()<>&*|$ ]*' -exec rm -f {} ;",
                "grep -A3 -B 3 -C434",
                "find  /home/mine -iname \"*.png\" -printf \"%P\\n \" | xargs  -I % -n1 cp %  /home/mine/pngcoppies/copy%",
                "find / -xdev -name document -print"
        };

        for (String cmd : cmds) {
           // System.out.println(cmd);
            //System.out.println(CmdParserInterface.parse(cmd));
        }

       //if (cmds.length > 0)
         //   return;

        String testDataPath = "test_data/train.correct.cm";

        int u = 0;

        //System.err
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        System.setErr(new PrintStream(baos));

        Files.lines(Paths.get(testDataPath)).forEach(
            x -> {
                String s = x.replace("\\)", ")").replace("\\(", "(").replace("\\;", ";");
                String cmdParsedPair = CmdParserInterface.parse(s);
                String parseLog = new String( baos.toByteArray(), Charset.defaultCharset() );
                if (! parseLog.trim().equals("")) {
                    //print unparsed commands
                  //  System.out.println(s);
                } else {
                    // print parsed commands
                    System.out.println(s);
                    System.out.println(cmdParsedPair);
                }

                baos.reset();
            }
        );
    }
}
