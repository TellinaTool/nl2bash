package man_parser;

import man_parser.parser.ParseException;
import org.junit.Test;

import java.io.IOException;

import static org.junit.Assert.*;

/**
 * Created by clwang on 12/11/16.
 */
public class ManParserInterfaceTest {

    @Test
    public void test() {
        try {
            ManParserInterface.parseSynopsisBNF("../grammar/grammar.2.txt");
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ParseException e) {
            e.printStackTrace();
        }
    }
}