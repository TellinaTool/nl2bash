"""
Functions for parsing bash code. See `parse(code)`
"""

# builtin
from __future__ import print_function
import sys

# 3rd party
import bashlex
import bashlex.ast

DEBUG = False

def split_flags(word):
    """turns -xyz into -x, -y, -z"""
    if word.startswith("-"):
        for flag in word[1:]:
            yield "-" + flag
    else:
        yield word

def parse(code):
    """
    Yields all simple bash commands found in the code, e.g. ["ls", "-l"]
    """
    try:
        parts = bashlex.parse(code)
    except:
        if DEBUG: print("warning: failed to parse {}".format(repr(code)), file=sys.stderr)
        return

    if DEBUG: print("parsed: {}".format(repr(code)), file=sys.stderr)

    for ast in parts:

        class Visitor(bashlex.ast.nodevisitor):
            def __init__(self):
                self.simplecmds = []
            def visitcommand(self, cmd, parts):
                if parts[0].kind == "word":
                    cmd = parts[0].word
                    args = []
                    for part in parts[1:]:
                        if part.kind == "word":
                            if cmd == "tar" and all(c in "xtcjzvf" for c in part.word):
                                args += ["-" + c for c in part.word]
                            elif cmd != "find":
                                args += list(split_flags(part.word))
                            else:
                                args.append(part.word)
                    self.simplecmds.append([cmd] + args)

        v = Visitor()
        v.visit(ast)
        for cmd in v.simplecmds:
            yield cmd

if __name__ == "__main__":
    # This lets you call `python bash.py "cmd"` to test the parser
    DEBUG = True
    for cmd in parse(" ".join(sys.argv[1:])):
        print(cmd)
