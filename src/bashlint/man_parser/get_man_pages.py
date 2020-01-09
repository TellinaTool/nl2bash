"""
Extract man page content of the bash commands of interest.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import subprocess
import sys


top_bash_commands = [
    "pwd",
    "cd",
    "ls",
    "mkdir",
    "rmdir",
    "echo",
    "cat",
    "zcat",
    "tac",
    "cp",
    "mv",
    "rm",
    "shred",
    "man",
    "head",
    "tail",
    "less*",
    "zless",
    "more",
    "grep",
    "egrep",
    "which",
    "chmod",
    "chown",
    "history*",
    "clear",
    "logout*",
    "exit*",
    "sudo",
    "su",
    "wc",
    "sort",
    "ssh",
    "ssh-keygen",
    "scp",
    "rsync",
    "source*",
    "export*",
    "ln",
    "readlink",
    "sleep",
    "ps",
    "pstree",
    "jobs",
    "bg",
    "fg",
    "kill",
    "top",
    "nohup",
    "time",
    "seq",
    "cut",
    "paste",
    "awk*",
    "sed",
    "date",
    "cal",
    "gzip",
    "gunzip",
    "bzip2",
    "bunzip2",
    "tar*",
    "uniq",
    "dirname",
    "basename",
    "set*",
    "unset*",
    "env",
    "uname",
    "df",
    "du",
    "bind*",
    "alias*",
    "unalias*",
    "column",
    "find",
    "touch",
    "diff",
    "comm",
    "join",
    "md5*",
    "md5sum",
    "tr",
    "od",
    "split",
    "nano",
    "emacs**",
    "vim",
    "tree*",
    "screen*",
    "tmux**",
    "yes",
    "nl",
    "whoami",
    "groups",
    "who",
    "w",
    "hostname",
    "finger*",
    "read*",
    "tee",
    "shopt*",
    "pushd*",
    "popd*",
    "true",
    "false",
    "shift*",
    "g++",
    "xargs",
    "crontab",
    "type*",
    "info",
    "apropos*",
    "fold",
    "rev",
    "mount*",
    "mktemp",
    "watch",
    "perl**",
    "python**",
    "ping*",
    "dig*",
    "ifconfig*",
    "wget*",
    "elinks*",
    "curl",
    "apt-get*",
    "brew**",
    "yum**",
    "display*",
    "convert*",
    "identify*",
    "gpg2*",
    "datamash*",
    "virtualenv**"
]


def run():
    out_dir = sys.argv[1]
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for cmd in top_bash_commands:
        try:
            output = subprocess.check_output([cmd,'--help'])
            with open(os.path.join(out_dir, cmd), 'w') as o_f:
                o_f.write(output)
        except:
            print(cmd)
            continue


if __name__ == '__main__':
    run()
