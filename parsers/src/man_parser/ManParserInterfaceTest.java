package man_parser;

import man_parser.parser.ParseException;
import org.junit.jupiter.api.Test;

import java.io.IOException;

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
}