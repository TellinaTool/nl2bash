import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

/**
 * Created by clwang on 2/24/16.
 */
public class SmallTask {

    public static String processWierdThing(String path) throws IOException {
        List<String> allLines = Files.readAllLines(Paths.get(path));
        String output = "";
        for (String s : allLines) {
            output += "[ " + s + " ]" + " ";
            //output += "[ " + " -not " + s + " ]";
        }

        for (int i = 0; i < allLines.size(); i ++) {
            for (int j = i + 1; j < allLines.size(); j ++) {
                //output += "[ " + allLines.get(i) + " -and " + allLines.get(j) + "] ";
                //output += "[ " + allLines.get(i) + " -or " + allLines.get(j) + "] ";
            }
        }

        return output;
    }

}
