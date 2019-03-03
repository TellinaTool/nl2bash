"""
Gazetteers for bash.
"""
utility_stats = """
1,find,103,5457,566
2,xargs,32,981,90
3,grep,82,871,90
4,rm,17,519,40
5,ls,84,351,40
6,echo,5,325,30
7,sort,50,317,30
8,chmod,14,274,38
9,wc,13,221,19
10,cut,15,197,16
11,head,12,163,18
12,chown,15,156,17
13,cat,19,154,13
14,mv,20,143,21
15,cp,49,140,10
16,mkdir,10,132,17
17,tail,20,119,18
18,dirname,4,99,15
19,tr,11,92,17
20,uniq,20,91,8
21,split,21,89,12
22,tar,50,82,12
23,readlink,18,80,6
24,tee,6,76,7
25,basename,8,74,5
26,ln,29,74,7
27,read,11,70,8
28,rsync,172,68,10
29,which,13,67,14
30,mount,14,65,5
31,ssh,43,58,5
32,file,25,57,8
33,pwd,6,54,4
34,du,43,53,8
35,md5sum,14,52,4
36,ifconfig,12,50,5
37,shopt,5,48,5
38,od,33,46,6
39,cd,3,46,4
40,comm,9,45,4
41,diff,71,44,3
42,hostname,26,44,4
43,df,27,43,4
44,rename,12,42,5
45,mktemp,12,42,7
46,date,18,40,5
47,nl,24,40,5
48,column,6,39,7
49,dig,13,39,1
50,paste,6,38,2
51,history,8,37,6
52,rev,4,36,2
53,zcat,10,36,8
54,touch,15,35,1
55,cal,7,34,1
56,chgrp,15,34,4
57,whoami,2,33,4
58,ping,28,33,7
59,gzip,34,32,4
60,rmdir,7,32,5
61,seq,8,31,10
62,tree,37,29,2
63,tac,8,28,6
64,bzip2,34,28,2
65,fold,10,28,3
66,join,15,28,4
67,cpio,54,27,4
68,who,32,26,6
69,pstree,30,25,3
70,uname,20,24,4
71,env,8,24,6
72,kill,9,21,1
"""

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
    'apt-get',
    'tmux'
}

# Flow controls
GREY_LIST = {
    'alias',
    'unalias',
    'set',
    'unset',
    'source',
    'export',
    'shift',
    'true',
    'false',
    'pushd',
    'popd'
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

pattern_argument_types = {
    'Regex',
    'File',
    'Directory',
    'Path'
}

quantity_argument_types = {
    'Number',
    '+Number',
    '-Number',
    'Quantity',
    '+Quantity',
    '-Quantity',
    'Size',
    '+Size',
    '-Size',
    'Timespan',
    '+Timespan',
    '-Timespan',
    'DateTime',
    '+DateTime',
    '-DateTime',
    'Permission',
    '+Permission',
    '-Permission'
}

argument_types = pattern_argument_types | quantity_argument_types | \
                 {'Type', 'Unknown'}

find_common_args = {
    '.',
    './',
    '~',
    '~/',
    '/',
}

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
