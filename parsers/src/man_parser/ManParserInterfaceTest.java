package man_parser;

import main.Main;
import man_parser.parser.ParseException;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.util.Arrays;

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

}