"""
Gazetteers for bash.
"""

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
    "find",
    "xargs",
    "grep",
    "egrep",
    "fgrep",
    "ls",
    "rm",
    "cp",
    "mv",
    "wc",
    "chmod",
    "chown",
    "chgrp",
    "sort",
    "head",
    "tail",
    "tar"
]
