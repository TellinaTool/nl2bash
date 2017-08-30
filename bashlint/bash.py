"""
Gazetteers for bash.
"""
utility_stats = """1,find,103,5068,525
2,xargs,32,821,82
3,grep,82,710,70
4,rm,17,505,40
5,ls,84,301,34
6,chmod,14,273,37
7,echo,5,251,26
8,sort,50,214,20
9,wc,13,185,17
10,chown,15,156,17
11,cut,15,146,11
12,mv,20,137,19
13,cp,49,133,9
14,head,12,123,14
15,mkdir,10,118,16
16,cat,19,103,7
17,dirname,4,92,14
18,tail,20,88,13
19,split,21,83,11
20,tar,50,76,11
21,readlink,18,74,6
22,ln,29,73,7
23,basename,8,72,5
24,read,11,70,8
25,rsync,172,67,10
26,tee,6,63,4
27,tr,11,62,11
28,set,19,61,6
29,which,13,61,13
30,ssh,43,57,5
31,uniq,20,55,5
32,mount,14,54,4
33,file,25,51,8
34,shopt,5,48,5
35,pwd,6,47,3
36,du,43,43,5
37,mktemp,12,42,7
38,rename,5,42,5
39,cd,3,41,3
40,md5sum,14,38,1
41,od,33,38,5
42,comm,9,37,3
43,diff,71,37,2
44,rmdir,7,32,5
45,date,18,32,5
46,hostname,26,32,1
47,chgrp,15,30,4
48,paste,6,30,1
49,dig,13,29,1
50,whoami,2,29,3
51,df,27,28,2
52,zcat,10,28,4
53,yes,2,27,1
54,gzip,34,27,3
55,rev,4,27,2
56,nl,24,25,5
57,ifconfig,12,24,4
58,less,98,24,2
59,seq,8,20,7
60,ping,28,19,2
61,history,7,18,3
62,cal,7,15,0
63,ps,22,15,0
64,column,6,15,3"""


top_100_utilities = {
    'echo',
    'bash',
    'sh',
    'chgrp',
    'cpio',
    'file',
    'rename',
    'compress',
    'pwd',
    'cd',
    'ls',
    'mkdir',
    'rmdir',
    'cat',
    'zcat',
    'tac',
    'cp',
    'mv',
    'rm',
    'shred',
    'head',
    'tail',
    'less',
    'zless',
    'more',
    'grep',
    'egrep',
    'fgrep',
    'which',
    'chmod',
    'chown',
    'history',
    'clear',
    'logout',
    'exit',
    'sudo',
    'su',
    'wc',
    'sort',
    'ssh',
    'ssh-keygen',
    'scp',
    'rsync',
    'source',
    'export',
    'ln',
    'readlink',
    'sleep',
    'ps',
    'pstree',
    'jobs',
    'bg',
    'fg',
    'kill',
    'top',
    'nohup',
    'time',
    'seq',
    'cut',
    'paste',
    'awk',
    'sed',
    'date',
    'cal',
    'gzip',
    'gunzip',
    'bzip2',
    'bunzip2',
    'tar',
    'uniq',
    'dirname',
    'basename',
    'set',
    'unset',
    'env',
    'uname',
    'df',
    'du',
    'bind',
    'alias',
    'unalias',
    'column',
    'find',
    'touch',
    'diff',
    'comm',
    'join',
    'md5',
    'md5sum',
    'tr',
    'od',
    'split',
    'nano',
    'emacs',
    'vim',
    'tree',
    'screen',
    'tmux',
    'yes',
    'nl',
    'whoami',
    'groups',
    'who',
    'w',
    'hostname',
    'finger',
    'read',
    'tee',
    'shopt',
    'pushd',
    'popd',
    'true',
    'false',
    'shift',
    'g++',
    'xargs',
    'crontab',
    'info',
    'apropos',
    'fold',
    'rev',
    'mount',
    'mktemp',
    'watch',
    'ping',
    'dig',
    'ifconfig',
    'wget',
    'elinks',
    'curl',
    'apt-get',
    'brew',
    'yum'
}


# Compilers
BLACK_LIST = {
    'cpp',
    'g++',
    'java',
    'perl',
    'python',
    'ruby',
    'nano',
    'emacs',
    'vim',
    'awk',
    'sed',
    'less',
    'more',
    'screen',
    'brew',
    'yum',
    'apt-get'
}


# Flow controls
GREY_LIST = {
    'alias',
    'unalias',
    'set',
    'unset',
    'export',
    'shift',
    'exit',
    'logout',
    'yes'
}

# --- Linux Utility by Category --- #

category_0_builtins = {
    'cd',
    'jobs',
    'bg',
    'fg',
    'set',
    'unset',
    'popd',
    'pushd',
    'source',
    'shopt',
    'set'
}

category_1_user_commands = {
    'pwd',
    'ls',
    'mkdir',
    'rmdir',
    'echo',
    'cat',
    'gzip',
    'gunzip',
    'zcat',
    'tac',
    'cp',
    'mv',
    'rm',
    'man',
    'head',
    'tail',
    'less',
    'zless',
    'more',
    'grep',
    'egrep',
    'fgrep',
    'which',
    'chmod',
    'chown',
    'chgrp',
    'su',
    'wc',
    'sort',
    'ssh',
    'ssh-keygen',
    'scp',
    'rsync',
    'ln',
    'readlink',
    'sleep',
    'ps',
    'pstree',
    'kill',
    'top',
    'nohup',
    'time',
    'seq',
    'cut',
    'sed',
    'paste',
    'which',
    'rename',
    'screen',
    'md5',
    'wget',
    'tmux',
    'find',
    'locate',
    'updatedb',
    'xargs',
    'dig'
}

category_2_system_calls = {}

category_3_library_functions = {}

category_7_conventions_and_miscellany = {}

category_8_administration_and_privileged_commands = {
    'ping',
    'sudo',
    'mount',
    'ifconfig'
}

findutils = {
    'find',
    'locate',
    'updatedb',
    'xargs'
}

# --- Other Constants Lists --- #

reserved_tokens = {
    '+',
    ';',
    '{}'
}

right_associate_unary_logic_operators = {
    '!',
    '-not'
}

left_associate_unary_logic_operators = {
    '-prune'
}

binary_logic_operators = {
    '-and',
    '-or',
    '||',
    '&&',
    '-o',
    '-a'
}
