package man_parser;

import main.Main;
import man_parser.cmd.Cmd;
import man_parser.parser.ParseException;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.stream.Collectors;

import static org.junit.Assert.*;

/**
 * Created by clwang on 12/11/16.
 */
public class ManParserInterfaceTest {

    @Test
    public void test() {
        try {
            ManParserInterface.parseManPage(true);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Test
    public void fastMakeGrammar() throws IOException, ParseException {
        String[] args = {"-gen-primitive-cmd-json", "../grammar/grammar.2.txt", "../grammar/optionwords.txt"};
        Main.main(args);
    }

    @Test
    public void fastTestGrammar() throws IOException, ParseException {
        String[] args = {"-gen-primitive-cmd-json", "./testdata/test_grammar.txt", "../grammar/optionwords.txt"};
        Main.main(args);
    }

    @Test
    public void fastGenG4Grammar() throws IOException, ParseException {
        String[] args = {"-make_grammar"};
        Main.main(args);
    }

    @Test
    public void fastParseManPage() throws IOException {
        String manPage = "../data/gnu-man/man1/split.txt";
        Cmd.ManPage mp = ManParserInterface.parseFile(new File(manPage));
        System.out.println(mp.rawSynopsis);

        String options = mp.optionDesc.stream().map(od -> od.pureOptions()).reduce("", (x,y)->(x + " " + y));

        System.out.println(options);
        System.out.println();

        System.out.println("\n" + mp.rawSynopsis.replaceAll("\\[OPTION\\]...", options));
        System.out.println("\n" + mp.rawSynopsis.replaceAll("\\[OPTION...\\]", options));
    }

}