# builtin
from __future__ import print_function

import re

import bast, errors, tokenizer, bparser, utils

_NUM = b"_NUM"
_LONG_PATTERN = b"_LONG_PATTERN"

_DIGIT_RE = re.compile(br"\d+")

head_commands = [
    "find", "xargs",
    "grep", "egrep",
    "sed", "awk",
    "ls", "rm",
    "cp", "mv",
    "wc", "chmod",
    "tar", "sort",
    "head", "tail",
    "chown"
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

# pseudo command names appeared in the collected data
pseudo_head_commands = [
    "parallel",
    "replace",
    "mplayer",
    "process",
    "execute",
    "rmdir",
    "pdfgrep",
    "fastqc",
    "ffmpeg",
    "cmd2",
    "command1",
    "command2"
]

def reserved_words():
    with open("/home/xilin/Projects/helper/bashlex/bash_keywords.txt") as f:
        _words = f.readlines()
    return [w.strip() for w in _words]

reserved_words = reserved_words()
all_utilities = set(reserved_words[reserved_words.index("alias"):])

def is_option(word):
    return word.startswith('-')

def is_double_option(word):
    return word.startswith('--')

def is_english_word(word):
    """Check if a token is normal English word."""
    return bool(re.match('[A-Za-z\-\'\(\)]+$', word, re.IGNORECASE))

def is_headcommand(word):
    return word in all_utilities or word in pseudo_head_commands

def rw_signature(cmd):
    tokens = bash_tokenizer(cmd)
    if not tokens:
        return None
    rws = set()
    for token in tokens:
        if token.startswith('-') or \
            token in reserved_words or \
            token in pseudo_head_commands or \
            token in special_operators:
            rws.add(token)
    signature = ' '.join(list(rws))
    return signature

@utils.deprecated
def bash_tokenizer(cmd, normalize_digits=True, normalize_long_pattern=True,
                   recover_quotation=True):
    cmd = cmd.replace('\n', ' ').strip()
    tokens = []
    if not cmd:
        return tokens

    def normalize_word(node, norm_digit, norm_long_pattern, recover_quote):
        w = recover_quotation(node) if recover_quote else node.word
        if ' ' in w:
            try:
                assert(w.startswith('"') and w.endswith('"'))
            except AssertionError, e:
                print("Quotation Error: space inside word " + w)
            if norm_long_pattern:
                w = _LONG_PATTERN
        return re.sub(_DIGIT_RE, _NUM, w) if norm_digit and not is_option(w) else w

    def with_quotation(node):
        return (node.pos[1] - node.pos[0] - len(node.word)) == 2

    def recover_quotation(node):
        if with_quotation(node):
            return cmd[node.pos[0] : node.pos[1]]
        else:
            return node.word

    def parse(node, tokens):
        if not type(node) is bast.node:
            tokens.append(str(node))
            return
        if node.kind == "word":
            if node.parts:
                # commandsubstitution, processsubstitution, parameter
                if node.parts[0].kind == "processsubstitution":
                    if '>' in node.word:
                        tokens.append('>(')
                        for child in node.parts:
                            parse(child, tokens)
                        tokens.append(')')
                    elif '<' in node.word:
                        tokens.append('<(')
                        for child in node.parts:
                            parse(child, tokens)
                        tokens.append(')')
                elif node.parts[0].kind == "parameter" or \
                    node.parts[0].kind == "tilde":
                    w = node.word
                    word = normalize_word(node, normalize_digits, normalize_long_pattern,
                                          recover_quotation)
                    tokens.append(word)
                else:
                    for child in node.parts:
                        parse(child, tokens)
            else:
                w = node.word
                word = normalize_word(node, normalize_digits, normalize_long_pattern,
                                      recover_quotation)
                tokens.append(word)
        elif node.kind == "pipe":
            w = node.pipe
            tokens.append(w)
        elif node.kind == "list":
            if len(node.parts) > 2:
                # multiple commands, not supported
                tokens.append(None)
            else:
                parse(node.parts[0], tokens)    # ignoring the ';' operator
        elif node.kind == "commandsubstitution":
            tokens.append('`')
            parse(node.command, tokens)
            tokens.append('`')
        elif node.kind == "processsubstitution":
            parse(node.command, tokens)
        elif node.kind == "parameter":
            # not supported
            tokens.append(None)
        elif hasattr(node, 'parts'):
            for child in node.parts:
                parse(child, tokens)
        elif node.kind == "operator":
            # not supported
            tokens.append(None)
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
        elif node.kind == "heredoc":
            # not supported
            tokens.append(None)

    try:
        bash_ast = bparser.parse(cmd)
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

    for node in bash_ast:
        parse(node, tokens)
        if None in tokens:
            print("Unsupported: %s" % cmd.encode('utf-8'))
            return None

    return [token.encode('utf-8') for token in tokens]

