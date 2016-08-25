# builtin
from __future__ import print_function

import re
import sys

DEBUG = False

COMBINED_FLAG_AND_ARG = re.compile(r"^(\-\w)(\d+)$")

def split_flags(cmd, word):

    if cmd == "tar" and all(c in "xtcrujzvf" for c in word):
        for c in word:
            yield "-" + c
    elif cmd != "find":
        if word.startswith("--"):

            for flag in word.split('='):
                yield flag

        elif word.startswith("-"):

            # turn -n1 into -n, 1
            match = COMBINED_FLAG_AND_ARG.match(word)
            if match:
                yield match.group(1)
                yield match.group(2)

            # turns -xyz into -x, -y, -z
            else:
                for flag in word[1:]:
                    yield "-" + flag
        else:
            yield word
    else:
        yield word

def test_split_flags(cmd, flag, expected):
    print(" --> testing flag splitting on {} {}... ".format(cmd, flag), end="")
    result = list(split_flags(cmd, flag))
    if result == expected:
        print("ok {}".format(result))
    else:
        print("got {}".format(result))
        assert result == expected # False

def parse(code):
    """
    Yields all simple bash commands found in the code, e.g. ["ls", "-l"]
    """
    try:
        parts = parse(code)
    except Exception as e:
        if DEBUG: print("warning: failed to parse {} ({}: {})".format(repr(code), type(e), e), file=sys.stderr)
        return

    if DEBUG: print("parsed: {}".format(repr(code)), file=sys.stderr)

    for ast in parts:

        class Visitor(ast.nodevisitor):
            def __init__(self):
                self.simplecmds = []
            def visitcommand(self, cmd, parts):
                if parts[0].kind == "word":
                    cmd = parts[0].word
                    args = []
                    for part in parts[1:]:
                        if part.kind == "word":
                            if cmd in ["xargs", "time", "nohup", "nice"] and \
                               part.word in ["find", "mv", "cp", "tar", "rm"]:
                                self.simplecmds.append([cmd] + args)
                                args = []
                                cmd = part.word
                            else:
                                args += list(split_flags(cmd, part.word))
                    self.simplecmds.append([cmd] + args)

        v = Visitor()
        v.visit(ast)
        for cmd in v.simplecmds:
            yield cmd


if __name__ == "__main__":
    # This lets you call `python bash.py "cmd"` to test the parser
    DEBUG = True
    test_split_flags("ls", "-lsh", ["-l", "-s", "-h"])
    test_split_flags("tar", "--exclude=something", ["--exclude", "something"])
    test_split_flags("tar", "czvf", ["-c", "-z", "-v", "-f"])
    test_split_flags("find", "-iname", ["-iname"])
    test_split_flags("xargs", "-n1", ["-n", "1"])
    test_split_flags("nice", "-n20", ["-n", "20"])
    for cmd in parse(" ".join(sys.argv[1:])):
        print(cmd)