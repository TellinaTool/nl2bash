"""
Gazetteers for bash.
"""

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

float_arguments = {
    'grep': ['A', 'B', 'C'],
    'head': ['', 'n'],
    'tail': ['', 'n'],
    'awk': ['F'],
    'xargs': ['n', 'l', 'L', 'P', 's']
}