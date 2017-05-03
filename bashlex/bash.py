"""
Gazetteers for bash.
"""

utilities = [
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
    "tar",
    "du",
    "file",
    "cat",
    "basename",
    "cut",
    "uniq",
    "pwd",
    "cpio",
    "dirname",
    "tee",
    "rename",
    "rmdir",
    "mkdir",
    "less",
    "md5sum",
    "compress"
]

utilities_20_to_15 = [
    "du",
    "file",
    "cat",
    "basename",
    "cut",
    "uniq",
    "pwd",
    "cpio",
    "dirname",
    "tee"
]

utilities_15_to_10 = [
    "rename",
    "rmdir",
    "mkdir",
    "less",
    "md5sum",
    "compress"
]

float_arguments = {
    'grep': ['A', 'B', 'C'],
    'head': ['', 'n'],
    'tail': ['', 'n'],
    'awk': ['F'],
    'xargs': ['n', 'l', 'L', 'P', 's']
}
