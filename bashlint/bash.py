"""
Gazetteers for bash.
"""
utility_stats = """
    0,find,5162,561
    1,xargs,851,88
    2,grep,745,68
    3,rm,479,50
    4,ls,324,39
    5,chmod,288,28
    6,echo,278,34
    7,sort,250,19
    8,wc,188,18
    9,chown,142,22
    10,mv,144,18
    11,cut,145,20
    12,cp,128,11
    13,mkdir,130,8
    14,head,144,16
    15,cat,141,7
    16,tail,102,10
    17,dirname,112,9
    18,split,78,6
    19,tar,80,7
    20,ln,68,12
    21,rsync,64,11
    22,read,72,6
    23,readlink,71,6
    24,basename,71,8
    25,tr,75,9
    26,which,65,10
    27,uniq,66,7
    28,tee,73,7
    29,ssh,57,8
    30,mount,59,0
    31,file,50,6
    32,du,50,5
    33,shopt,43,11
    34,rename,43,8
    35,pwd,50,4
    36,mktemp,44,4
    37,cd,45,3
    38,comm,41,4
    39,date,33,8
    40,md5sum,36,3
    41,diff,27,12
    42,rmdir,33,3
    43,od,31,4
    44,hostname,33,1
    45,cpio,27,7
    46,df,30,5
    47,chgrp,30,4
    48,seq,28,4
    49,touch,30,2
    50,gzip,31,4
    51,dig,27,2
    52,whoami,27,5
    53,bzip2,27,3
    54,nl,24,8
    55,rev,28,1
    56,paste,27,2
    57,tree,24,2
    58,ifconfig,25,4
    59,zcat,26,2
    60,uname,23,3
    61,env,24,1
    62,join,24,2
    63,column,21,3
    64,fold,22,0
    65,history,20,0
    66,ping,19,3
    67,pstree,18,1
    68,cal,14,0
    69,who,13,2
    70,tac,9,1
    71,kill,15,2
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
