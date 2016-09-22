# builtin
from __future__ import print_function

import os
import re

_NUM = b"_NUM"
_LONG_PATTERN = b"_LONG_PATTERN"

_DIGIT_RE = re.compile(br"\d+")

# TODO: add stdin & stdout types
simplified_bash_syntax = [
    "Command ::= SingleCommand | Pipe",
    "Pipe ::= Command '|' Command",
    "SingleCommand ::= HeadCommand [OptionList]",
    "OptionList ::= Option | OptionList",
    "Option ::= Flag [Argument] | LogicOp Option",
    "Argument ::= SingleArgument | CommandSubstitution | ProcessSubstitution",
    "CommandSubstitution ::= ` Command `",
    "ProcessSubstitution ::= <( Command ) | >( Command )"
]

arg_syntax = [
    "File",
    "Pattern",
    "Number",
    "NumberExp ::= -Number | +Number",
    "SizeExp ::= Number(k) | Number(M) | Number(G) | Number(T) | Number(P)",
    "TimeExp ::= Number(s) | Number(m) | Number(h) | Number(d) | Number(w)",
    # TODO: add fine-grained permission pattern
    "PermissionMode",
    "UserName",
    "GroupName",
    "Unknown"
]

head_commands = [
    "find", "xargs",
    "grep", "egrep",
    "fgrep", "sed",
    "awk", "ls",
    "rm", "cp",
    "mv", "wc",
    "chmod", "tar",
    "sort", "head",
    "tail", "chown"
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
    "command2",
    "rename",
    "tac"
]

def reserved_words():
    with open(os.path.join(os.path.dirname(__file__), "bash_keywords.txt")) as f:
        _words = f.readlines()
    return [w.strip() for w in _words]

reserved_words = reserved_words()
all_utilities = set(reserved_words[reserved_words.index("alias"):])

def is_double_option(word):
    return word.startswith('--')

def is_english_word(word):
    """Check if a token is normal English word."""
    return bool(re.match('[A-Za-z\-\'\(\)]+$', word, re.IGNORECASE))

def is_headcommand(word):
    return word in all_utilities or word in pseudo_head_commands

