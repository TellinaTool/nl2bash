"""
Functions for parsing bash code. See `parse(code)`
"""

# builtin
from __future__ import print_function

import re
import sys

from bashlex import errors, tokenizer, parser

DEBUG = False

COMBINED_FLAG_AND_ARG = re.compile(r"^(\-\w)(\d+)$")

# Regular expressions used to tokenize an English sentence.
_WORD_SPLIT = re.compile(b"^\s+|\s*,\s*|\s+$|^[\(|\[|\{|\<|\'|\"|\`]|[\)|\]|\}|\>|\'|\"|\`]$")
# _WORD_SPLIT = re.compile(b"^\s+|\s*,\s*|\s+$|^[\(|\[|\{|\<]|[\)|\]|\}|\>]$")
_DIGIT_RE = re.compile(br"\d+")

_NUM = b"_NUM"

head_commands = [
    "find", "xargs",
    "grep", "egrep",
    "sed", "awk",
    "ls", "rm",
    "cp", "mv",
    "cd", "cat",
    "wc", "chmod",
    "zip", "unzip",
    "tar", "sort",
    "head", "tail",
    "du", "echo",
    "diff", "comm",
    "sh"
]

special_operators = [
    "|",
    "`",
    "<(",
    "(",
    ")>",
    ")",
    "$("
]

def is_option(word):
    return word.startswith('-')

def basic_tokenizer(sentence, normalize_digits=True, lower_case=True):
    """Very basic tokenizer: used for English tokenization."""
    words = []
    for space_separated_fragment in sentence.replace('\n', ' ').strip().split():
        words.extend(re.split(_WORD_SPLIT, space_separated_fragment))
    normalized_words = []
    for i in xrange(len(words)):
        w = words[i].lower() if i == 0 else words[i]
        word = re.sub(_DIGIT_RE, _NUM, w) if normalize_digits and not is_option(w) else w
        if lower_case:
            # remove unnecessary upper cases
            if len(word) > 1 and word[0].isupper() and word[1:].islower():
                word = word.lower()
        normalized_words.append(word)
    return normalized_words

def bash_tokenizer(cmd, normalize_digits=True):
    cmd = cmd.replace('\n', ' ').strip()
    tokens = []
    if not cmd:
        return tokens

    def parse(node, tokens):
        if not type(node) is ast.node:
            tokens.append(str(node))
            return
        if node.kind == "word":
            if hasattr(node, 'parts') and node.parts and \
                node.parts[0].kind != "tilde":
                # commandsubstitution, processsubstitution, parameter
                for child in node.parts:
                    parse(child, tokens)
            else:
                w = node.word
                word = re.sub(_DIGIT_RE, _NUM, w) if normalize_digits and not is_option(w) else w
                tokens.append(word)
        elif node.kind == "pipe":
            w = node.pipe
            tokens.append(w)
        elif node.kind == "operator":
            w = node.op
            tokens.append(w)
        elif node.kind == "list":
            if len(node.parts) > 2:
                # multiple commands, not supported
                tokens.append(None)
            else:
                for child in node.parts:
                    parse(child, tokens)
        elif node.kind == "commandsubstitution":
            tokens.append('`')
            parse(node.command, tokens)
            tokens.append('`')
        elif node.kind == "processsubstitution":
            if '>' in node.word:
                tokens.append('>(')
                parse(node.command, tokens)
                tokens.append(')')
            elif '<' in node.word:
                tokens.append('<(')
                parse(node.command, tokens)
                tokens.append(')')
            else:
                # unrecognized syntax
                return None
        elif hasattr(node, 'parts'):
            for child in node.parts:
                parse(child, tokens)
        elif node.kind == "redirect":
            # not supported
            tokens.append(None)
            # if node.type == '>':
            #     parse(node.input, tokens)
            #     tokens.append('>')
            #     parse(node.output, tokens)
            # elif node.type == '<':
            #     parse(node.output, tokens)
            #     tokens.append('<')
            #     parse(node.input, tokens)
        elif node.kind == "for":
            # not supported
            tokens.append(None)
        elif node.kind == "if":
            # not supported
            tokens.append(None)
        elif node.kind == "while":
            # not supported
            tokens.append(None)
        elif node.kind == "until":
            # not supported
            tokens.append(None)
        elif node.kind == "assignment":
            # not supported
            tokens.append(None)
        elif node.kind == "function":
            # not supported
            tokens.append(None)
        elif node.kind == "tilde":
            # not supported
            tokens.append(None)
        elif node.kind == "parameter":
            # not supported
            if node.value.lower() in ['home', 'dir', 'file', 'path']:
                w = node.value
                tokens.append(w)
            else:
                tokens.append(None)
        elif node.kind == "heredoc":
            # not supported
            tokens.append(None)

    try:
        ast = parser.parse(cmd)
    except tokenizer.MatchedPairError, e:
        print("Cannot parse: %s - MatchedPairError" % cmd.encode('utf-8'))
        # return basic_tokenizer(cmd, normalize_digits, False)
        return None
    except errors.ParsingError, e:
        print("Cannot parse: %s - ParsingError" % cmd.encode('utf-8'))
        # return basic_tokenizer(cmd, normalize_digits, False)
        return None
    except NotImplementedError, e:
        print("Cannot parse: %s - NotImplementedError" % cmd.encode('utf-8'))
        # return basic_tokenizer(cmd, normalize_digits, False)
        return None
    except IndexError, e:
        print("Cannot parse: %s - IndexError" % cmd.encode('utf-8'))
        # empty command
        return None
    except AttributeError, e:
        print("Cannot parse: %s - AttributeError" % cmd.encode('utf-8'))
        # not a bash command
        return None

    for node in ast:
        parse(node, tokens)
        if None in tokens:
            print("Unsupported: %s" % cmd.encode('utf-8'))
            return None

    return tokens

def reserved_words_signature(cmd):
    tokens = bash_tokenizer(cmd)
    if not tokens:
        return None
    reserved_words = set()
    for token in tokens:
        if token.startswith('-') or \
           token in head_commands or \
           token in special_operators:
            reserved_words.add(token)
    signature = ' '.join(list(reserved_words))
    return signature

# -- Outdated ---

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
