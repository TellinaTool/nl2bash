import javafx.util.Pair;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
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

    public static void extractOptionsFrom(String path) throws IOException {
        List<String> lines = Files.readAllLines(Paths.get(path));
        for (int i = 0; i < lines.size(); i ++) {
            if (lines.get(i).startsWith("OPTIONS")) {
                System.out.println(lines.get(i));
                i ++;
                int l = i;
                while (i < lines.size() && (lines.get(i).indexOf(lines.get(i).trim()) != 0 || lines.get(i).equalsIgnoreCase(""))) {
                    System.out.println(lines.get(i));
                    i ++;
                }
                List<String> subLst = lines.subList(l, i);
                parseOption(subLst);
                break;
            }
        }
    }

    private static void parseOption(List<String> lines) {
        int i = 0;
        int basicIndent = -1;
        // c,r,t,u,x respectly
        List<List<String>> modes = new ArrayList<>();
        for (int j = 0; j < 5; j ++) {
            modes.add(new ArrayList<>());
        }
        while (i < lines.size()) {
            if (lines.get(i).trim().startsWith("-")) {
                String title = lines.get(i).trim();
                System.out.println("> " + title);
                if (basicIndent == -1) {
                    basicIndent = lines.get(i).indexOf(lines.get(i).trim());
                }
                i ++;
                int l = i;
                while (i < lines.size() && !lines.get(i).trim().startsWith("-")) {
                    i ++;
                }
                i --;
                String body = lines.subList(l, i).stream().reduce(" ", (x,y) -> x  + " " + y);
                if (body.trim().startsWith("(")) {
                    String mode = body.trim().substring(1, body.trim().indexOf(")"));
                    //System.out.println(mode);
                    List<String> tokenList = new ArrayList<>();
                    String[] tokens = mode.split(",");
                    for (String token : tokens) {
                        String[] ts = token.split("\\s+");
                        for (String t : ts)
                            tokenList.add(t.trim());
                    }
                    for (String t : tokenList) {
                        System.out.println(t);
                    }
                    if (contains("c", tokenList)) {
                        modes.get(0).add(title);
                    }
                    if (contains("r", tokenList)) {
                        modes.get(1).add(title);
                    }
                    if (contains("t", tokenList)) {
                        modes.get(2).add(title);
                    }
                    if (contains("u", tokenList)) {
                        modes.get(3).add(title);
                    }
                    if (contains("x", tokenList)) {
                        modes.get(4).add(title);
                    }
                } else {
                    for (int k = 0; k < 5; k ++) {
                        modes.get(k).add(title);
                    }
                }
                System.out.println("  " + body);
            }
            i ++;
        }

        for (List<String> ls : modes) {
            String s = "";
            for (String temps: ls) {
                s += "[ " + temps + "] ";
            }
            System.out.println(">> " + s);
        }
    }

    private static boolean contains(String s, List<String> ls) {
        for (String ss : ls) {
            if (ss.equalsIgnoreCase(s))
                return true;
        }
        return false;
    }
}
