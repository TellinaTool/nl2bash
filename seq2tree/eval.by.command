Unrecognized cmd_option type argument_option
basic_tree_encoder: output_projection/proj_w:0
basic_tree_encoder: output_projection/proj_b:0
softmax_loss: output_projection/proj_w:0
softmax_loss: output_projection/proj_b:0
forward: output_projection/proj_w:0
forward: output_projection/proj_b:0
Reading model parameters from ../model/seq2tree.by.command/translate.ckpt-10
Loading data from ../data/reader/seq2tree.by.command/
Example 1 (1)
Original English: Find all files in maximum 1 level down the current directory that were modified less than 1 day ago from today
English: find all file in maximum "_NUM" level down current directory modified le than "_NUM" day ago from today
Original Command: find -maxdepth 1 -type f -daystart -mtime -1

Ground truth: find -maxdepth _NUM -type f -daystart -mtime -_NUM
Prediction: find -maxdepth _NUM -type f -mtime _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-maxdepth)
            ARGUMENT(_NUM)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-mtime)
            ARGUMENT(_NUM)

lS splitted into: -l -S 
Error: -lS is not a flag of ls
Example 2 (1)
Original English: List first 20 files under current directory
English: list first "_NUM" file under current directory
Original Command: find . -type f |xargs ls -lS |head -20

Ground truth: find . -type f | xargs ls -l -S | head -_NUM
Prediction: find . | head
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
        HEADCOMMAND(head)

rf splitted into: -r -f 
Error: -rf is not a flag of rm
Example 3 (1)
Original English: find and delete all the files in the entire file system whose size is greater than 100MB.
English: find and delete all file in entire file system whose size greater than "_NUMMB"
Original Command: find / -size +100M -exec rm -rf {} \;

Ground truth: find / -size +_NUMM -exec rm -r -f {} ;
Prediction: find / -type f -size +_NUMM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-size)
            ARGUMENT(+_NUMM)

Example 4 (1)
Original English: display all the files in the current folder excluding those that are present in the sub directory aa and display those files that start with the word "file"
English: display all file in current folder excluding present in sub directory aa and display file start with word "file"
Original Command: find . \( -type d -name aa -prune \) -o \( -type f -name 'file*' -print \)

Ground truth: find . \( \( -type d -and -name aa -prune \) -or \( -type f -and -name 'file*' -and -print \) \)
Prediction: find . -name *
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        BINARYLOGICOP(-or)
            FLAG(-name)
                ARGUMENT(*)

m1 splitted into: -m -1 
Error: -m1 is not a flag of grep
Example 5 (1)
Original English: find all the files ending with ".coffee" in the current folder and search for the words "re" in each line
English: find all file ending with _UNK in current folder and search for word _UNK in each line
Original Command: find . -name \*.coffee -exec grep -m1 -i 're' {} \;

Ground truth: find . -name *.coffee -exec grep -m -1 -i 're' {} ;
Prediction: find . -name *.ini -exec grep -H UNK -exec grep -H UNK ; ; | xargs grep -H UNK -exec grep -H string-to-find {} ;
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-name)
                ARGUMENT(*.ini)
            FLAG(-exec::;)
                HEADCOMMAND(grep)
                    FLAG(-H)
                    ARGUMENT(UNK)
                    FLAG(-exec::;)
                        HEADCOMMAND(grep)
                            FLAG(-H)
                            ARGUMENT(UNK)
        HEADCOMMAND(xargs)
            HEADCOMMAND(grep)
                FLAG(-H)
                ARGUMENT(UNK)
                FLAG(-exec::;)
                    HEADCOMMAND(grep)
                        FLAG(-H)
                        ARGUMENT(string-to-find)
                        ARGUMENT({})

Example 6 (1)
Original English: Delete all ".DS_Store" files/directories under test directory
English: delete all _UNK "files/directories" under test directory
Original Command: find test -name ".DS_Store" -delete

Ground truth: find test -name ".DS_Store" -delete
Prediction: find test -name "*txt" -delete
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(test)
        FLAG(-name)
            ARGUMENT("*txt")
        FLAG(-delete)

Example 7 (1)
Original English: Find all C source code files from the current directory tree that contain "keyword" in their pathnames, ignoring the case
English: find all C source code file from current directory tree contain _UNK in pathnames ignoring case
Original Command: find . -type f \( -iname “*.c” \) |grep -i “keyword”

Ground truth: find . -type f -iname “*.c” | grep -i “keyword”
Prediction: find . -iname UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-iname)
            ARGUMENT(UNK)

Example 8 (4)
Original English: Search the current directory tree for regular files omitting directory `omit-directory'
English: search current directory tree for regular file omitting directory _UNK
Original Command: find . \( -name omit-directory -prune \) -o \( -type f -print \)

Ground truth: find . \( -name omit-directory -prune -or \( -type f -and -print \) \)
Prediction: find . -type f -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-name)
            ARGUMENT(UNK)

Example 9 (1)
Original English: Search the current directory tree for directories that can be opened by noone
English: search current directory tree for directory _UNK by _UNK
Original Command: find -type d ! -perm -111

Ground truth: find -type d ! -perm -_NUM
Prediction: find . -type d -name Cookbook
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(d)
        FLAG(-name)
            ARGUMENT(Cookbook)

Example 10 (1)
Original English: Search the /usr/bin directory tree for regular files modified or created less than 10 days ago
English: search "/usr/bin" directory tree for regular file modified or created le than "_NUM" day ago
Original Command: find /usr/bin -type f -mtime -10

Ground truth: find /usr/bin -type f -mtime -_NUM
Prediction: find /usr/bin -type f -mtime -_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/usr/bin)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-mtime)
            ARGUMENT(-_NUM)

Example 11 (1)
Original English: Find all regular files in /usr/bin modified less than within the last 10 days
English: find all regular file in "/usr/bin" modified le than within last "_NUM" day
Original Command: find /usr/bin -type f -mtime -10

Ground truth: find /usr/bin -type f -mtime -_NUM
Prediction: find /usr/bin -type f -ctime -_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/usr/bin)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-ctime)
            ARGUMENT(-_NUM)

Example 12 (1)
Original English: Find all files in the current directory tree that are not newer than some_file
English: find all file in current directory tree not newer than _UNK
Original Command: find . ! -newer some_file

Ground truth: find . ! -newer some_file
Prediction: find . -newer /etc/motd
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-newer)
            ARGUMENT(/etc/motd)

Example 13 (1)
Original English: find files matching the given name only in the current directory
English: find file matching given name only in current directory
Original Command: find . -maxdepth 1 -type f -name "$1"

Ground truth: find . -maxdepth _NUM -type f -name "$_NUM"
Prediction: find . -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)

Example 14 (3)
Original English: Search for files/directories which are writable by either their owner or their group
English: search for "files/directories" writable by either owner or group
Original Command: find . -perm /u+w,g+w

Ground truth: find . -perm /u+w,g+w
Prediction: find . \( -newer UNK -or -perm -_NUM \)
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        BINARYLOGICOP(-or)
            FLAG(-newer)
                ARGUMENT(UNK)
            FLAG(-perm)
                ARGUMENT(-_NUM)

Error: -fprint is not a flag of find
Example 15 (1)
Original English: save the list of the files in the current directory to a file “foo”
English: save list of file in current directory to file _UNK
Original Command: find . -fprint foo

Ground truth: find . -fprint foo
Prediction: find . -name '*.rb' -exec rm {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT('*.rb')
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT({})

Example 16 (1)
Original English: find all files in the file system which have been accessed in the last 24 hours
English: find all file in file system accessed in last "_NUM" hour
Original Command: find / -atime 0

Ground truth: find / -atime _NUM
Prediction: find / -amin -_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-amin)
            ARGUMENT(-_NUM)

Example 17 (1)
Original English: find not case sensitive all directories that names are 'project.images'
English: find not case sensitive all directory name _UNK
Original Command: find  / -type d -iname "project.images" -ls

Ground truth: find / -type d -iname "project.images" -ls
Prediction: find / -type d -iname "apt"
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-type)
            ARGUMENT(d)
        FLAG(-iname)
            ARGUMENT("apt")

Example 18 (2)
Original English: Find and remove all .core files
English: find and remove all _UNK file
Original Command: find / -name "*.core" -print -exec rm {} \;

Ground truth: find / -name "*.core" -print -exec rm {} ;
Prediction: find . -inum +_NUM -type f -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-inum)
            ARGUMENT(+_NUM)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-print)

Example 19 (1)
Original English: Print the names and sizes of regular files residing in the "dir" directory tree
English: print name and size of regular file residing in "dir" directory tree
Original Command: find dir -type f -printf "f %s %p\n"

Ground truth: find dir -type f -printf _LONG_PATTERN
Prediction: find | xargs ls -l
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
        HEADCOMMAND(xargs)
            HEADCOMMAND(ls)
                FLAG(-l)

Quotation Error: space inside word '*[+{;"\\=?~()<>&*|$ ]*'
Example 20 (1)
Original English: Search for file names with "bad" characters in the current directory and delete the files.
English: search for file name with _UNK character in current directory and delete file
Original Command: find . -name '*[+{;"\\=?~()<>&*|$ ]*' -maxdepth 0 -exec rm -f '{}' \;

Ground truth: find . -name _LONG_PATTERN -maxdepth _NUM -exec rm -f '{}' ;
Prediction: find . -name UNK -delete
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-delete)

Example 21 (1)
Original English: Find all subdirectories of the current directory except hidden ones
English: find all subdirectory of current directory except hidden "_NUM"
Original Command: find -maxdepth 1 -type d ! -name ".*"

Ground truth: find -maxdepth _NUM -type d ! -name ".*"
Prediction: find -maxdepth _NUM -type d ! -maxdepth _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-maxdepth)
            ARGUMENT(_NUM)
        FLAG(-type)
            ARGUMENT(d)
        UNARYLOGICOP(!)
            FLAG(-maxdepth)
                ARGUMENT(_NUM)

Error: -0002 is not a flag of find
Example 22 (1)
Original English: Search the entire file system for any file that is writable by other.
English: search entire file system for any file writable by other
Original Command: find / – perm -0002

Ground truth: find / – perm -0002
Prediction: find / -perm -_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-perm)
            ARGUMENT(-_NUM)

Example 23 (1)
Original English: Print the list of files in the current directory tree skipping Git files
English: print list of file in current directory tree skipping git file
Original Command: find . -path './.git' -prune -o -type f

Ground truth: find . \( -path './.git' -prune -or -type f \)
Prediction: find . \( -path '*/.*' -prune -or -print \)
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        BINARYLOGICOP(-or)
            UNARYLOGICOP(-prune)
                FLAG(-path)
                    ARGUMENT('*/.*')
            FLAG(-print)

Example 24 (1)
Original English: Search for "www.athabasca" in all files under current directory
English: search for _UNK in all file under current directory
Original Command: find . -exec grep "www.athabasca" '{}' \; -print

Ground truth: find . -exec grep "www.athabasca" '{}' ; -print
Prediction: find . -type f -print | xargs grep "text"
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-type)
                ARGUMENT(f)
            FLAG(-print)
        HEADCOMMAND(xargs)
            HEADCOMMAND(grep)
                ARGUMENT("text")

Example 25 (1)
Original English: find all the mp3 files in the home folder which have been modified today
English: find all "mp_NUM" file in home folder modified today
Original Command: find ~ -type f -mtime 0 -iname '*.mp3'

Ground truth: find ~ -type f -mtime _NUM -iname '*.mp_NUM'
Prediction: find $HOME -name "*blast*" -type f -ls
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT($HOME)
        FLAG(-name)
            ARGUMENT("*blast*")
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-ls)

Example 26 (1)
Original English: display a long listing of all the normal/regular files in the current folder (print0 is used to handle files which have newlines in their names or files with the name only as spaces )
English: display long listing of all "normal/regular" file in current folder ( "print_NUM" used to handle file newlines in name or file with name only space )
Original Command: find . -type f -print0 | xargs -0 ls -l

Ground truth: find . -type f -print0 | xargs -0 ls -l
Prediction: find . \( -name "*.txt" -or -name UNK \) -ls
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        BINARYLOGICOP(-or)
            FLAG(-name)
                ARGUMENT("*.txt")
            FLAG(-name)
                ARGUMENT(UNK)
        FLAG(-ls)

Example 27 (1)
Original English: same as above example with -exec , in this example with -OK it should ask for confirmation before executing the rm command . that is called user intractive command
English: same above example with _UNK in example with _UNK ask for confirmation before _UNK rm command called user _UNK command
Original Command: find . -name core -ok rm {} \;

Ground truth: find . -name core -ok rm {} ;
Prediction: find /usr \( -name CVS -or -name UNK \)
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/usr)
        BINARYLOGICOP(-or)
            FLAG(-name)
                ARGUMENT(CVS)
            FLAG(-name)
                ARGUMENT(UNK)

Example 28 (1)
Original English: How to find for files containing a specific word in its name?
English: to find for file containing specific word in _UNK
Original Command: find -name "*java*"

Ground truth: find -name "*java*"
Prediction: find . -iname UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-iname)
            ARGUMENT(UNK)

Example 29 (1)
Original English: Find all the files in file system which are accessed 50 days back
English: find all file in file system accessed "_NUM" day back
Original Command: find / -atime 50

Ground truth: find / -atime _NUM
Prediction: find / -atime _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-atime)
            ARGUMENT(_NUM)

dlrt splitted into: -d -l -r -t 
Error: -dlrt is not a flag of ls
dlrt splitted into: -d -l -r -t 
Error: -dlrt is not a flag of ls
Example 30 (2)
Original English: List all directories in maximum 1 level down the current directory
English: list all directory in maximum "_NUM" level down current directory
Original Command: find . -type d -maxdepth 1 -exec ls -dlrt {} \;

Ground truth: find . -type d -maxdepth _NUM -exec ls -d -l -r -t {} ;
Prediction: find -maxdepth _NUM -type d -maxdepth _NUM -type d
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-maxdepth)
            ARGUMENT(_NUM)
        FLAG(-type)
            ARGUMENT(d)
        FLAG(-maxdepth)
            ARGUMENT(_NUM)
        FLAG(-type)
            ARGUMENT(d)

Example 31 (1)
Original English: To list all of the files in your home directory tree that were modified from two to four days ago
English: to list all of file in home directory tree modified from "_NUM" to "_NUM" day ago
Original Command: find ~ -mtime 2 -mtime -4 -daystart

Ground truth: find ~ -mtime _NUM -mtime -_NUM -daystart
Prediction: find $HOME -mtime _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT($HOME)
        FLAG(-mtime)
            ARGUMENT(_NUM)

Example 32 (1)
Original English: list all samba files in /var/l* directory ( /var/lib or /var/log )
English: list all _UNK file in _UNK directory ( _UNK or "/var/log" )
Original Command: find  /var -path */l??/samba*

Ground truth: find /var -path */l??/samba*
Prediction: find /var/log/ \( -name /var/log/ -prune -or -iname UNK \)
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/var/log/)
        BINARYLOGICOP(-or)
            UNARYLOGICOP(-prune)
                FLAG(-name)
                    ARGUMENT(/var/log/)
            FLAG(-iname)
                ARGUMENT(UNK)

Example 33 (1)
Original English: find all the files in the current directory ending with ".i"
English: find all file in current directory ending with _UNK
Original Command: find . -name ".*\.i"

Ground truth: find . -name ".*\.i"
Prediction: find . -name *.ini
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(*.ini)

Example 34 (1)
Original English: Search the bla directory recursively for *.so files
English: search _UNK directory recursively for _UNK file
Original Command: find bla -name "*.so"

Ground truth: find bla -name "*.so"
Prediction: find UNK -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(f)

Example 35 (1)
Original English: Find files recursively with extension "ext"
English: find file recursively with extension _UNK
Original Command: find . -name "*.ext"

Ground truth: find . -name "*.ext"
Prediction: find . -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)

Example 36 (1)
Original English: Copy all regular files whose names end in "~" from the /path directory tree to ~/backups/
English: copy all regular file whose name end in "~" from "/path" directory tree to _UNK
Original Command: find /path -type f -name '*~' -print0 | xargs -0 -I % cp -a % ~/backups

Ground truth: find /path -type f -name '*~' -print0 | xargs -0 -I % cp -a % ~/backups
Prediction: find /path -name "*blast*" -exec cp '{}' ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/path)
        FLAG(-name)
            ARGUMENT("*blast*")
        FLAG(-exec::;)
            HEADCOMMAND(cp)
                ARGUMENT('{}')

Example 37 (1)
Original English: change the permission of all php files in current folder
English: change permission of all php file in current folder
Original Command: find . -name "*.php" -exec chmod 755 {} \;

Ground truth: find . -name "*.php" -exec chmod _NUM {} ;
Prediction: find . -type f -perm _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-perm)
            ARGUMENT(_NUM)

lrt splitted into: -l -r -t 
Error: -lrt is not a flag of ls
F  splitted into: -F -  
Error: -F  is not a flag of awk
Quotation Error: space inside word '{print $1 $2  $9}'
Example 38 (1)
Original English: Find only number of hard link & name of files from long list
English: find only number of hard link "&" name of file from long list
Original Command: find -type f -iname "*.txt" -exec ls -lrt {} \;|awk -F' ' '{print $1 $2  $9}'

Ground truth: find -type f -iname "*.txt" -exec ls -l -r -t {} ; | awk -F' ' -F' ' _LONG_PATTERN
Prediction: find . -type f -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-name)
            ARGUMENT(UNK)

Example 39 (1)
Original English: Find directories named `build'
English: find directory named _UNK
Original Command: find . -type d -name build

Ground truth: find . -type d -name build
Prediction: find . -name Cookbook
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(Cookbook)

Example 40 (1)
Original English: Count the total number of lines in all HTML files under /usr/src that contain string "foo"
English: count total number of line in all HTML file under "/usr/src" contain string "foo"
Original Command: find /usr/src -name "*.html" -execdir /usr/bin/grep -H "foo" {} ';' | wc -l

Ground truth: find /usr/src -name "*.html" -execdir grep -H "foo" {} ; | wc -l
Prediction: find /usr/src -type f -name '*.c' -exec grep -l '{}' ; | xargs -0
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(/usr/src)
            FLAG(-type)
                ARGUMENT(f)
            FLAG(-name)
                ARGUMENT('*.c')
            FLAG(-exec::;)
                HEADCOMMAND(grep)
                    FLAG(-l)
                    ARGUMENT('{}')
        HEADCOMMAND(xargs)
            FLAG(-0)

Example 41 (1)
Original English: Print the empty files/directories among empty1, empty2 and not_empty
English: print empty "files/directories" among _UNK _UNK and _UNK
Original Command: find empty1 empty2 not_empty -prune -empty

Ground truth: find empty_NUM empty_NUM not_empty -prune -empty
Prediction: find UNK \( -newer UNK -or -name UNK \)
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        BINARYLOGICOP(-or)
            FLAG(-newer)
                ARGUMENT(UNK)
            FLAG(-name)
                ARGUMENT(UNK)

Example 42 (1)
Original English: Find all files on the system whose names are 'drush'
English: find all file on system whose name _UNK
Original Command: find / -name drush

Ground truth: find / -name drush
Prediction: find / -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-name)
            ARGUMENT(UNK)

qiF splitted into: -q -i -F 
Error: -qiF is not a flag of grep
Example 43 (1)
Original English: Delete all files under /path/to/input/ that match the case insensitive string literal 'spammer@spammy.com' in their contents
English: delete all file under _UNK match case insensitive string literal _UNK in content
Original Command: find /path/to/input/ -type f -exec grep -qiF spammer@spammy.com \{\} \; -delete

Ground truth: find /path/to/input/ -type f -exec grep -q -i -F spammer@spammy.com {} ; -delete
Prediction: find UNK -exec rm -i UNK UNK ; -print -exec rm {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                FLAG(-i)
                    ARGUMENT(UNK)
                ARGUMENT(UNK)
        FLAG(-print)
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT({})

Example 44 (2)
Original English: Identify CMS version/releases accross all your Wordpress websites
English: identify CMS "version/releases" accross all _UNK website
Original Command: find /var/www/vhosts/*/httpdocs/ -type f -iwholename "*/wp-includes/version.php" -exec grep -H "\$wp_version =" {} \;

Ground truth: find /var/www/vhosts/*/httpdocs/ -type f -iwholename "*/wp-includes/version.php" -exec grep -H _LONG_PATTERN {} ;
Prediction: find /home/*/public_html/ -type f -name "*.txt" -exec rm {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/home/*/public_html/)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-name)
            ARGUMENT("*.txt")
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT({})

Example 45 (1)
Original English: Find recursively all files whose names begin with "foo"
English: find recursively all file whose name begin with "foo"
Original Command: find . -name "foo*"

Ground truth: find . -name "foo*"
Prediction: find / -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-name)
            ARGUMENT(UNK)

Example 46 (2)
Original English: Force delete all jpg files in current directory which are less than 50KB and do not search in the sub directories
English: force delete all jpg file in current directory le than "_NUMKB" and not search in sub directory
Original Command: find . -maxdepth 1 -name "*.jpg" -size -50k -exec rm {} \;

Ground truth: find . -maxdepth _NUM -name "*.jpg" -size -_NUMk -exec rm {} ;
Prediction: find -maxdepth _NUM -type f -perm -_NUM -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-maxdepth)
            ARGUMENT(_NUM)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-perm)
            ARGUMENT(-_NUM)
        FLAG(-type)
            ARGUMENT(f)

Example 47 (1)
Original English: change html files to mode 644
English: change html file to mode "_NUM"
Original Command: find /usr/local -name "*.html" -type f -exec chmod 644 {} \;

Ground truth: find /usr/local -name "*.html" -type f -exec chmod _NUM {} ;
Prediction: find htdocs -name "*.cgi" -exec chmod _NUM {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(htdocs)
        FLAG(-name)
            ARGUMENT("*.cgi")
        FLAG(-exec::;)
            HEADCOMMAND(chmod)
                ARGUMENT(_NUM)
                ARGUMENT({})

Example 48 (1)
Original English: Print the names and sizes of all regular files from the current directory tree
English: print name and size of all regular file from current directory tree
Original Command: find . -type f -printf "%f %s\n"

Ground truth: find . -type f -printf _LONG_PATTERN
Prediction: find . -type f | awk _LONG_PATTERN
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-type)
                ARGUMENT(f)
        HEADCOMMAND(awk)
            ARGUMENT(_LONG_PATTERN)

Example 49 (1)
Original English: Search the /Path directory tree for files whose pathnames match pattern "/Path/bar*" and whose names match pattern "file_name*"
English: search _UNK directory tree for file whose pathnames match pattern _UNK and whose name match pattern "file_name*"
Original Command: find /Path -path "/Path/bar*" -name "file_name*"

Ground truth: find /Path -path "/Path/bar*" -name "file_name*"
Prediction: find UNK -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-name)
            ARGUMENT(UNK)

Example 50 (2)
Original English: find all normal/regular files in current folder and display the total lines in them
English: find all "normal/regular" file in current folder and display total line in
Original Command: find . -type f -print0 | xargs -0 wc -l

Ground truth: find . -type f -print0 | xargs -0 wc -l
Prediction: find . -type f | xargs wc -l
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-type)
                ARGUMENT(f)
        HEADCOMMAND(xargs)
            HEADCOMMAND(wc)
                FLAG(-l)

Example 51 (1)
Original English: Find all directories named build under the current directory
English: find all directory named build under current directory
Original Command: find . -type d -name build

Ground truth: find . -type d -name build
Prediction: find . -name nasa
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(nasa)

Example 52 (1)
Original English: Find all files/directories in all paths expanded by the glob pattern *
English: find all "files/directories" in all path expanded by glob pattern "*"
Original Command: find *

Ground truth: find *
Prediction: find .*
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.*)

Example 53 (1)
Original English: find files matching the given name
English: find file matching given name
Original Command: find ./ -type f -name NAME

Ground truth: find ./ -type f -name NAME
Prediction: find -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-name)
            ARGUMENT(UNK)

rn splitted into: -r -n 
Error: -rn is not a flag of sort
Example 54 (1)
Original English: Find the largest files in a particular location
English: find largest file in particular location
Original Command: find /home/tecmint/Downloads/ -type f -printf "%s %p\n" | sort -rn | head -n 5

Ground truth: find /home/tecmint/Downloads/ -type f -printf _LONG_PATTERN | sort -r -n | head -n _NUM
Prediction: find . -n _LONG_PATTERN | sort -n ls -l -n
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-n)
            ARGUMENT(_LONG_PATTERN)
        HEADCOMMAND(sort)
            FLAG(-n)
            HEADCOMMAND(ls)
                FLAG(-l)
                FLAG(-n)

Example 55 (1)
Original English: Search .c and .h files in the current directory tree for "expr"
English: search ".c" and ".h" file in current directory tree for "expr"
Original Command: find . -name '*.[ch]' | xargs grep -E 'expr'

Ground truth: find . -name '*.[ch]' | xargs grep -E 'expr'
Prediction: find -name '*.[ch]' | xargs grep -E -E
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            FLAG(-name)
                ARGUMENT('*.[ch]')
        HEADCOMMAND(xargs)
            HEADCOMMAND(grep)
                FLAG(-E)
                FLAG(-E)

Example 56 (1)
Original English: find all the files in the current directory and sub-directories whose status was changed after /etc/fstab was modified
English: find all file in current directory and sub-directories whose status wa changed after _UNK wa modified
Original Command: find -cnewer /etc/fstab

Ground truth: find -cnewer /etc/fstab
Prediction: find . -newer UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-newer)
            ARGUMENT(UNK)

Error: -t is not a flag of mv
Error: -t is not a flag of mv
Error: -t is not a flag of mv
Example 57 (4)
Original English: find all the directories in the current folder which have been modified in 24 hours and move them to the folder  /path/to/target-dir
English: find all directory in current folder modified in "_NUM" hour and move to folder _UNK
Original Command: find . -type d -mtime -0 -print0 | xargs -0 mv -t /path/to/target-dir

Ground truth: find . -type d -mtime -_NUM -print0 | xargs -0 mv -t /path/to/target-dir
Prediction: find . -type d -name UNK -exec mv {} UNK ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(d)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-exec::;)
            HEADCOMMAND(mv)
                ARGUMENT({})
                ARGUMENT(UNK)

Example 58 (1)
Original English: lists all files that are greater than 10,000 bytes, but less than 50,000 bytes
English: list all file greater than "_NUM" "_NUM" byte but le than "_NUM" "_NUM" byte
Original Command: find . -size +10000c -size -50000c -print

Ground truth: find . -size +_NUMc -size -_NUMc -print
Prediction: find / -size +_NUM -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-size)
            ARGUMENT(+_NUM)
        FLAG(-print)

Example 59 (1)
Original English: Find all hidden (regular) files under /tmp
English: find all hidden ( regular ) file under "/tmp"
Original Command: find /tmp -type f -name ".*"

Ground truth: find /tmp -type f -name ".*"
Prediction: find /tmp -name ".*" -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/tmp)
        FLAG(-name)
            ARGUMENT(".*")
        FLAG(-type)
            ARGUMENT(f)

Example 60 (1)
Original English: Remove all *.sql files in the $backup_path directory tree that were last modified more than 30 days ago
English: remove all "*.sql" file in "$backup_path" directory tree last modified more than "_NUM" day ago
Original Command: find $backup_path/* -name *.sql -mtime +30 -exec rm {} \;

Ground truth: find $backup_path/* -name *.sql -mtime +_NUM -exec rm {} ;
Prediction: find UNK -exec rm {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT({})

Example 61 (1)
Original English: Find files belonging to particular user
English: find file belonging to particular user
Original Command: find . -user bob

Ground truth: find . -user bob
Prediction: find / -user UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-user)
            ARGUMENT(UNK)

Example 62 (1)
Original English: Search the /Applications directory tree for *.app directories
English: search _UNK directory tree for _UNK directory
Original Command: find /Applications -type d -name "*.app"

Ground truth: find /Applications -type d -name "*.app"
Prediction: find UNK -type d
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(d)

Example 63 (2)
Original English: Search for occurrences of string "main(" in the .c files from the current directory tree
English: search for occurrence of string _LONG_PATTERN in ".c" file from current directory tree
Original Command: find . -name "*.c" -print | xargs grep "main("

Ground truth: find . -name "*.c" -print | xargs grep "main("
Prediction: find . -name UNK -type f -print | xargs grep -i -n _LONG_PATTERN
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-name)
                ARGUMENT(UNK)
            FLAG(-type)
                ARGUMENT(f)
            FLAG(-print)
        HEADCOMMAND(xargs)
            HEADCOMMAND(grep)
                FLAG(-i)
                FLAG(-n)
                ARGUMENT(_LONG_PATTERN)

Example 64 (1)
Original English: display all files in the current folder that have been modified in the last 24 hours whose name has only 1 letter
English: display all file in current folder modified in last "_NUM" hour whose name ha only "_NUM" letter
Original Command: find . -name \? -mtime -1

Ground truth: find . -name ? -mtime -_NUM
Prediction: find . -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)

Example 65 (1)
Original English: find file which case-insensitive name is foo in current directory.
English: find file case-insensitive name foo in current directory
Original Command: find . -iname foo

Ground truth: find . -iname foo
Prediction: find . -type f -name foo
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-name)
            ARGUMENT(foo)

Example 66 (1)
Original English: Find all regular files that reside in the current directory tree and were last modified more than 5 days ago
English: find all regular file reside in current directory tree and last modified more than "_NUM" day ago
Original Command: find . -type f -mtime +5

Ground truth: find . -type f -mtime +_NUM
Prediction: find . -type f -mtime +_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-mtime)
            ARGUMENT(+_NUM)

Error: - is not a flag of tar
Example 67 (1)
Original English: Archive all *html files using tar.
English: archive all _UNK file using tar
Original Command: find . -type f -name "*html" | xargs tar cvf htmlfiles.tar -

Ground truth: find . -type f -name "*html" | xargs tar cvf htmlfiles.tar -
Prediction: find . -iname *.jpg -exec tar -z UNK ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-iname)
            ARGUMENT(*.jpg)
        FLAG(-exec::;)
            HEADCOMMAND(tar)
                FLAG(-z)
                ARGUMENT(UNK)

rf splitted into: -r -f 
Error: -rf is not a flag of rm
Example 68 (2)
Original English: search for the folder .dummy and remove it from the folder "Test folder"
English: search for folder _UNK and remove from folder _LONG_PATTERN
Original Command: find "Test Folder" -type d -name '.dummy' -delete

Ground truth: find _LONG_PATTERN -type d -name '.dummy' -delete
Prediction: find . -type f -name UNK -exec rm {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT({})

Example 69 (1)
Original English: Show what content owned by root has been modified within the last day
English: show content owned by root ha modified within last day
Original Command: find /etc/ -user root -mtime 1

Ground truth: find /etc/ -user root -mtime _NUM
Prediction: find / -user UNK -type f -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-user)
            ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-print)

Example 70 (1)
Original English: search all files in a folder which are bigger than 100MB and which are atleast 1 level deep and delete them
English: search all file in folder bigger than "_NUMMB" and atleast "_NUM" level deep and delete
Original Command: find .cache/chromium/Default/Cache/ -mindepth 1 -size +100M -delete

Ground truth: find .cache/chromium/Default/Cache/ -mindepth _NUM -size +_NUMM -delete
Prediction: find .cache/chromium/Default/Cache/ -mindepth _NUM -type d -delete
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.cache/chromium/Default/Cache/)
        FLAG(-mindepth)
            ARGUMENT(_NUM)
        FLAG(-type)
            ARGUMENT(d)
        FLAG(-delete)

Example 71 (1)
Original English: Find all files that are exactly 50 bytes
English: find all file exactly "_NUM" byte
Original Command: find / -size 50c

Ground truth: find / -size _NUMc
Prediction: find . -size _NUMc
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-size)
            ARGUMENT(_NUMc)

Example 72 (1)
Original English: display all the files in current folder which have write permission to all the users
English: display all file in current folder write permission to all user
Original Command: find . -perm /222

Ground truth: find . -perm /_NUM
Prediction: find . -perm _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-perm)
            ARGUMENT(_NUM)

nr splitted into: -n -r 
Error: -nr is not a flag of sort
Example 73 (1)
Original English: Find all files under current directory with their size and paths, reverse sort them numerically, then print the 2nd field (with space as the delimiter) of the first 4 entries
English: find all file under current directory with size and path reverse sort numerically print "_NUMnd" field ( with space delimiter ) of first "_NUM" entry
Original Command: find -type f -printf "%s %p\n" | sort -nr | head -n 4 | awk "{print $2}"

Ground truth: find -type f -printf _LONG_PATTERN | sort -n -r | head -n _NUM | awk _LONG_PATTERN
Prediction: find -maxdepth _NUM -type f -printf _LONG_PATTERN | sort
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            FLAG(-maxdepth)
                ARGUMENT(_NUM)
            FLAG(-type)
                ARGUMENT(f)
            FLAG(-printf)
                ARGUMENT(_LONG_PATTERN)
        HEADCOMMAND(sort)

Example 74 (1)
Original English: search for all the file having a specific word in a folder and delete the file. delete the file as super user
English: search for all file having specific word in folder and delete file delete file _UNK user
Original Command: sudo find /home/user/Series/ -iname sample -print0 | sudo xargs -0 rm -r

Ground truth: find /home/user/Series/ -iname sample -print0 | xargs -0 rm -r
Prediction: find /home/user/Series/ -iname '*.ogg' -exec rm {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/home/user/Series/)
        FLAG(-iname)
            ARGUMENT('*.ogg')
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT({})

Example 75 (1)
Original English: Serach for all the files containing grep in man pages
English: serach for all file containing grep in _UNK page
Original Command: find /usr/share/man/ -regex .*grep*

Ground truth: find /usr/share/man/ -regex .*grep*
Prediction: find . -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-print)

Example 76 (1)
Original English: Display the 5 smallest files in the current directory and its sub-directories.
English: display "_NUM" smallest file in current directory and sub-directories
Original Command: find . -type f -exec ls -s {} \; | sort -n  | head -5

Ground truth: find . -type f -exec ls -s {} ; | sort -n | head -_NUM
Prediction: find . -type f | sort -k | tail -_NUM
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-type)
                ARGUMENT(f)
        HEADCOMMAND(sort)
            FLAG(-k)
        HEADCOMMAND(tail)
            ARGUMENT(-_NUM)

Example 77 (1)
Original English: find all directories with the name test in a directory
English: find all directory with name test in directory
Original Command: find /home/john -type d -name test -print

Ground truth: find /home/john -type d -name test -print
Prediction: find . -name 'httpdocs'
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT('httpdocs')

Example 78 (1)
Original English: Find all files with a filename beginning with a specified string which may match thousands of files
English: find all file with filename beginning with specified string may match _UNK of file
Original Command: find . -name 'mystring*'

Ground truth: find . -name 'mystring*'
Prediction: find / -not -name 'top?????*'
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        UNARYLOGICOP(-not)
            FLAG(-name)
                ARGUMENT('top?????*')

Quotation Error: space inside word 'Name: %16f Size: %6s\n'
Example 79 (1)
Original English: search for all the non-hidden files in the current directory and do not search in the subfolders and dispaly their name and size.
English: search for all non-hidden file in current directory and not search in subfolders and dispaly name and size
Original Command: find . -maxdepth 1 -name '[!.]*' -printf 'Name: %16f Size: %6s\n'

Ground truth: find . -maxdepth _NUM -name '[!.]*' -printf _LONG_PATTERN
Prediction: find . \( -path '*/\.*' -prune -or -iname '*' \) ! -path '*/\.*'
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        BINARYLOGICOP(-or)
            UNARYLOGICOP(-prune)
                FLAG(-path)
                    ARGUMENT('*/\.*')
            FLAG(-iname)
                ARGUMENT('*')
        UNARYLOGICOP(!)
            FLAG(-path)
                ARGUMENT('*/\.*')

Example 80 (1)
Original English: Find files and directories newer than CompareFile under current directory
English: find file and directory newer than _UNK under current directory
Original Command: find . -newer CompareFile -print

Ground truth: find . -newer CompareFile -print
Prediction: find . -newer UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-newer)
            ARGUMENT(UNK)

Example 81 (1)
Original English: Remove all files whose names start with spam-
English: remove all file whose name start with _UNK
Original Command: find . -name 'spam-*' | xargs rm

Ground truth: find . -name 'spam-*' | xargs rm
Prediction: find . -name UNK -exec rm {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT({})

Example 82 (1)
Original English: search for the file picasso in the folder /home/calvin/ (case insensitive search)
English: search for file _UNK in folder _UNK ( case insensitive search )
Original Command: find /home/calvin/ -iname “picasso”

Ground truth: find /home/calvin/ -iname “picasso”
Prediction: find UNK -iname UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-iname)
            ARGUMENT(UNK)

Example 83 (1)
Original English: Locate all passwd files on the system
English: locate all passwd file on system
Original Command: find / -name passwd

Ground truth: find / -name passwd
Prediction: find / -name 'top?????*'
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-name)
            ARGUMENT('top?????*')

Example 84 (1)
Original English: find all files under the /etc/sysconfig directory that were accessed in the last 30 minutes
English: find all file under "/etc/sysconfig" directory accessed in last "_NUM" minute
Original Command: find /etc/sysconfig -amin -30

Ground truth: find /etc/sysconfig -amin -_NUM
Prediction: find /etc/sysconfig -amin -_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/etc/sysconfig)
        FLAG(-amin)
            ARGUMENT(-_NUM)

Example 85 (1)
Original English: Search for files/directories that are readable for everybody, have at least one write bit set but are not executable for anybody
English: search for "files/directories" readable for _UNK at least "_NUM" write bit set but not executable for _UNK
Original Command: find . -perm -444 -perm /222 ! -perm /111

Ground truth: find . -perm -_NUM -perm /_NUM ! -perm /_NUM
Prediction: find / -perm /_NUM \( -newer UNK -or -perm /_NUM \) -type f -perm /_NUM -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-perm)
            ARGUMENT(/_NUM)
            BINARYLOGICOP(-or)
                FLAG(-newer)
                    ARGUMENT(UNK)
                FLAG(-perm)
                    ARGUMENT(/_NUM)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-perm)
            ARGUMENT(/_NUM)
        FLAG(-print)

Example 86 (3)
Original English: List all regular files in the current directory tree
English: list all regular file in current directory tree
Original Command: find . -type f -exec ls -l '{}' \;

Ground truth: find . -type f -exec ls -l '{}' ;
Prediction: find . -type f -ls
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-ls)

Example 87 (1)
Original English: Find all read only files in  /home directory
English: find all read only file in "/home" directory
Original Command: find /home -type f -perm /u=r

Ground truth: find /home -type f -perm /u=r
Prediction: find /home -perm /u=r
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/home)
        FLAG(-perm)
            ARGUMENT(/u=r)

rf splitted into: -r -f 
Error: -rf is not a flag of rm
Example 88 (1)
Original English: Find all 100MB+ files and delete them
English: find all _UNK file and delete
Original Command: find / -size +100M -exec rm -rf {} \;

Ground truth: find / -size +_NUMM -exec rm -r -f {} ;
Prediction: find . -type f -name UNK -delete
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-delete)

Example 89 (1)
Original English: Find all files that aren't owned by user www-data
English: find all file _UNK owned by user www-data
Original Command: find -not -user www-data

Ground truth: find -not -user www-data
Prediction: find / -user UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-user)
            ARGUMENT(UNK)

Example 90 (1)
Original English: count all the html files having a specifc word in a folder.
English: count all html file having _UNK word in folder
Original Command: find /usr/src -name "*.html" -exec grep -l foo '{}' ';' | wc -l

Ground truth: find /usr/src -name "*.html" -exec grep -l foo '{}' ; | wc -l
Prediction: find UNK -name UNK | xargs wc -l
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(UNK)
            FLAG(-name)
                ARGUMENT(UNK)
        HEADCOMMAND(xargs)
            HEADCOMMAND(wc)
                FLAG(-l)

Example 91 (1)
Original English: find all the files in a folder which belong to a specific user.
English: find all file in folder belong to specific user
Original Command: find /home -user bob

Ground truth: find /home -user bob
Prediction: find /usr -user UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/usr)
        FLAG(-user)
            ARGUMENT(UNK)

Quotation Error: space inside word '*[+{;"\\=?~()<>&*|$ ]*'
Example 92 (1)
Original English: Delete files containing whitespaces without recursion
English: delete file containing whitespaces without _UNK
Original Command: find . -name '*[+{;"\\=?~()<>&*|$ ]*' -maxdepth 0 -exec rm -f '{}' \;

Ground truth: find . -name _LONG_PATTERN -maxdepth _NUM -exec rm -f '{}' ;
Prediction: find . -type f -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-print)

Example 93 (1)
Original English: Search the current directory recursively for files last modified within the past 24 hours ignoring paths ./es* and ./en*
English: search current directory recursively for file last modified within past "_NUM" hour ignoring path "./es*" and "./en*"
Original Command: find . -mtime 0 | grep -v '^\./en' | grep -v '^\./es'

Ground truth: find . -mtime _NUM | grep -v '^\./en' | grep -v '^\./es'
Prediction: find . -not -name UNK -not -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        UNARYLOGICOP(-not)
            FLAG(-name)
                ARGUMENT(UNK)
        UNARYLOGICOP(-not)
            FLAG(-name)
                ARGUMENT(UNK)

Example 94 (2)
Original English: search for wordpress version in all the version.php files in a folder and display the matched file name
English: search for _UNK version in all _UNK file in folder and display matched file name
Original Command: find /home/*/public_html/ -type f -iwholename "*/wp-includes/version.php" -exec grep -H "\$wp_version =" {} \;

Ground truth: find /home/*/public_html/ -type f -iwholename "*/wp-includes/version.php" -exec grep -H _LONG_PATTERN {} ;
Prediction: find UNK -type f -exec grep -H UNK {} ; -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-exec::;)
            HEADCOMMAND(grep)
                FLAG(-H)
                ARGUMENT(UNK)
                ARGUMENT({})
        FLAG(-print)

Example 95 (1)
Original English: Find empty regular files in /dir and its subdirectories
English: find empty regular file in "/dir" and subdirectory
Original Command: find /dir -type f -size 0 -print

Ground truth: find /dir -type f -size _NUM -print
Prediction: find /dir -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/dir)
        FLAG(-type)
            ARGUMENT(f)

Example 96 (1)
Original English: Delete files under $LOCATION that match $REQUIRED_FILES in their names and were modified more than 360 minutes ago
English: delete file under _UNK match _UNK in name and modified more than "_NUM" minute ago
Original Command: find $LOCATION -name $REQUIRED_FILES -type f -mmin +360 -delete

Ground truth: find $LOCATION -name $REQUIRED_FILES -type f -mmin +_NUM -delete
Prediction: find UNK -type f -mmin +_NUM -delete
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-mmin)
            ARGUMENT(+_NUM)
        FLAG(-delete)

Example 97 (1)
Original English: find all files in home folder which have been modified exactly 1 day before
English: find all file in home folder modified exactly "_NUM" day before
Original Command: find ~ -mtime 1 -daystart

Ground truth: find ~ -mtime _NUM -daystart
Prediction: find $HOME -mtime _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT($HOME)
        FLAG(-mtime)
            ARGUMENT(_NUM)

Example 98 (3)
Original English: find a directory called project.images
English: find directory called _UNK
Original Command: find  / -type d -iname "project.images" -ls

Ground truth: find / -type d -iname "project.images" -ls
Prediction: find -name Cookbook
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-name)
            ARGUMENT(Cookbook)

Example 99 (1)
Original English: Search for files/directories which are writable by somebody (their owner, or their group, or anybody else)
English: search for "files/directories" writable by _UNK ( owner or group or _UNK _UNK )
Original Command: find . -perm /222

Ground truth: find . -perm /_NUM
Prediction: find . -perm UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        BINARYLOGICOP(-or)
            FLAG(-perm)
                ARGUMENT(UNK)

Example 100 (1)
Original English: Find all files that belongs to group 'root' under / directory and show a few lines of output from the beginning
English: find all file belongs to group "root" under "/" directory and show few line of output from beginning
Original Command: find / -group root | head

Ground truth: find / -group root | head
Prediction: find / -group | head
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(/)
            FLAG(-group)
        HEADCOMMAND(head)

Example 101 (2)
Original English: Find all .core files on the system starting from / and delete them
English: find all _UNK file on system starting from "/" and delete
Original Command: find / -name "*.core" -print -exec rm {} \;

Ground truth: find / -name "*.core" -print -exec rm {} ;
Prediction: find / -user UNK -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-user)
            ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(f)

Example 102 (2)
Original English: display all file in the folder /dir/to/search except ".c" files
English: display all file in folder _UNK except ".c" file
Original Command: find /dir/to/search/ -not -name "*.c" -print

Ground truth: find /dir/to/search/ -not -name "*.c" -print
Prediction: find $HOME -not -iname "*.c" -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT($HOME)
        UNARYLOGICOP(-not)
            FLAG(-iname)
                ARGUMENT("*.c")
        FLAG(-print)

Example 103 (1)
Original English: Remove all files from the current directory tree whose names do not match regular expression "excluded files criteria"
English: remove all file from current directory tree whose name not match regular expression _LONG_PATTERN
Original Command: find . | grep -v "excluded files criteria" | xargs rm

Ground truth: find . | grep -v _LONG_PATTERN | xargs rm
Prediction: find . -not -regex UNK | egrep rm
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            UNARYLOGICOP(-not)
                FLAG(-regex)
                    ARGUMENT(UNK)
        HEADCOMMAND(egrep)
            HEADCOMMAND(rm)

Example 104 (1)
Original English: Look for *log files in directories at most three levels down the directory tree
English: look for _UNK file in directory at most "_NUM" level down directory tree
Original Command: find / -maxdepth 3  -name "*log"

Ground truth: find / -maxdepth _NUM -name "*log"
Prediction: find -mindepth _NUM -type f -name CVS
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-mindepth)
            ARGUMENT(_NUM)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-name)
            ARGUMENT(CVS)

Example 105 (1)
Original English: Count the number of files named `file1'
English: count number of file named "file_NUM"
Original Command: find -name file1 | wc -l

Ground truth: find -name file_NUM | wc -l
Prediction: find -name file_NUM
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            FLAG(-name)
                ARGUMENT(file_NUM)

Example 106 (1)
Original English: Find the .groovy files outside the "./target" directory path
English: find _UNK file _UNK _UNK directory path
Original Command: find .  -name "*.groovy" -not -path "./target/*" -print

Ground truth: find . -name "*.groovy" -not -path "./target/*" -print
Prediction: find UNK -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(f)

Example 107 (1)
Original English: Find all regular files that reside in the current directory tree and were last modified more than 3 days ago
English: find all regular file reside in current directory tree and last modified more than "_NUM" day ago
Original Command: find . -type f -mtime +3

Ground truth: find . -type f -mtime +_NUM
Prediction: find . -type f -mtime +_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-mtime)
            ARGUMENT(+_NUM)

Example 108 (1)
Original English: Find all files and directories that do not match the pattern given as the $controlchars variable
English: find all file and directory not match pattern given _UNK variable
Original Command: find . ! -name "$controlchars"

Ground truth: find . ! -name "$controlchars"
Prediction: find . -mmin -_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-mmin)
            ARGUMENT(-_NUM)

Example 109 (1)
Original English: find all the normal/regular files in several folders and search for a specific pattern in these files
English: find all "normal/regular" file in several folder and search for specific pattern in file
Original Command: find ./online_admin/*/UTF-8/* -type f -exec grep -H "invalidTemplateName" {} \;

Ground truth: find ./online_admin/*/UTF-_NUM/* -type f -exec grep -H "invalidTemplateName" {} ;
Prediction: find /usr/bin -name UNK -type f -exec grep -H string-to-find {} +
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/usr/bin)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-exec::+)
            HEADCOMMAND(grep)
                FLAG(-H)
                ARGUMENT(string-to-find)
                ARGUMENT({})

Example 110 (1)
Original English: Show all files in /etc that are owned by root have been modified within the last minute
English: show all file in "/etc" owned by root modified within last minute
Original Command: find /etc/ -user root -mtime 1

Ground truth: find /etc/ -user root -mtime _NUM
Prediction: find / -mmin -_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-mmin)
            ARGUMENT(-_NUM)

Example 111 (1)
Original English: find files which full path name is /tmp/foo/bar under foo directory and print
English: find file full path name "/tmp/foo/bar" under foo directory and print
Original Command: find /tmp/foo -path /tmp/foo/bar -print

Ground truth: find /tmp/foo -path /tmp/foo/bar -print
Prediction: find foo -path /tmp/foo/bar -wholename /tmp/foo/bar -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(foo)
        FLAG(-path)
            ARGUMENT(/tmp/foo/bar)
        FLAG(-wholename)
            ARGUMENT(/tmp/foo/bar)
        FLAG(-print)

Example 112 (1)
Original English: Find directories in the current directory recursively that are not "executable" by all
English: find directory in current directory recursively not _UNK by all
Original Command: find -type d ! -perm -111

Ground truth: find -type d ! -perm -_NUM
Prediction: find -type d
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-type)
            ARGUMENT(d)

Example 113 (1)
Original English: Search the current directory tree for *.c and *.sh files
English: search current directory tree for "*.c" and "*.sh" file
Original Command: find . -type f \( -name "*.c" -o -name "*.sh" \)

Ground truth: find . -type f \( -name "*.c" -or -name "*.sh" \)
Prediction: find . -name '*.[ch]'
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        BINARYLOGICOP(-or)
            FLAG(-name)
                ARGUMENT('*.[ch]')

Example 114 (1)
Original English: display the count of regular files in a folder which have specific permission to the owner
English: display count of regular file in folder specific permission to owner
Original Command: find home/magie/d2 -type f -perm -u+rx | wc -l

Ground truth: find home/magie/d_NUM -type f -perm -u+rx | wc -l
Prediction: find $dir -type f -perm -_NUM | wc -l
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT($dir)
            FLAG(-type)
                ARGUMENT(f)
            FLAG(-perm)
                ARGUMENT(-_NUM)
        HEADCOMMAND(wc)
            FLAG(-l)

Example 115 (1)
Original English: Print a colon-separated list of all directories from the ~/code directory tree, except hidden ones and those below them
English: print colon-separated list of all directory from _UNK directory tree except hidden "_NUM" and below
Original Command: find ~/code -name '.*' -prune -o -type d -printf ':%p'

Ground truth: find ~/code \( -name '.*' -prune -or -type d \) -printf ':%p'
Prediction: find $dir -mindepth _NUM -type d ! -name '.*'
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT($dir)
        FLAG(-mindepth)
            ARGUMENT(_NUM)
        FLAG(-type)
            ARGUMENT(d)
        UNARYLOGICOP(!)
            FLAG(-name)
                ARGUMENT('.*')

Example 116 (1)
Original English: search for the file job.hostory in the folder "/data/Spoolln"
English: search for file _UNK in folder "/data/Spoolln"
Original Command: find /data/SpoolIn -name job.history

Ground truth: find /data/SpoolIn -name job.history
Prediction: find UNK -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-name)
            ARGUMENT(UNK)

Hn splitted into: -H -n 
Error: -Hn is not a flag of grep
Quotation Error: space inside word '/<\?php \/\*\*\/eval(base64_decode(.*));.*\?>/d'
Example 117 (1)
Original English: Find all php files in current directory and delete lines matching the regex '<\?php \/\*\*\/eval(base64_decode(.*));.*\?>' in those files
English: find all php file in current directory and delete line matching regex _LONG_PATTERN in file
Original Command: find . \( -name "*.php" \) -exec grep -Hn "<\?php /\*\*/eval(base64_decode(.*));.*\?>" {} \; -exec sed -i '/<\?php \/\*\*\/eval(base64_decode(.*));.*\?>/d' {} \;

Ground truth: find . -name "*.php" -exec grep -H -n _LONG_PATTERN {} ; -exec sed -i _LONG_PATTERN {} ;
Prediction: find . -type f -name "*.php" -exec rm {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-name)
            ARGUMENT("*.php")
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT({})

Example 118 (1)
Original English: Find all regular files starting from / that have permissions 777
English: find all regular file starting from "/" permission "_NUM"
Original Command: find / -type f -perm 0777

Ground truth: find / -type f -perm _NUM
Prediction: find / -type f -perm _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-perm)
            ARGUMENT(_NUM)

Example 119 (1)
Original English: find all the files that belong  to a specific user
English: find all file belong to specific user
Original Command: find -user takuya

Ground truth: find -user takuya
Prediction: find -user UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-user)
            ARGUMENT(UNK)

Example 120 (1)
Original English: sort based on size and display top ten small normal/regular files in the current folder
English: sort based on size and display top "_NUM" small "normal/regular" file in current folder
Original Command: find . -type f -exec ls -s {} \; | sort -n | head -10

Ground truth: find . -type f -exec ls -s {} ; | sort -n | head -_NUM
Prediction: find . -type f | head -_NUM
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-type)
                ARGUMENT(f)
        HEADCOMMAND(head)
            ARGUMENT(-_NUM)

Example 121 (1)
Original English: Search the current directory tree for .rb files ignoring the "./vendor" subdirectory
English: search current directory tree for ".rb" file ignoring _UNK subdirectory
Original Command: find . -name '*.rb' ! -wholename "./vendor/*" -print

Ground truth: find . -name '*.rb' ! -wholename "./vendor/*" -print
Prediction: find . \( -name '*.rb' -prune -or -name '*.rb' \) -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        BINARYLOGICOP(-or)
            UNARYLOGICOP(-prune)
                FLAG(-name)
                    ARGUMENT('*.rb')
            FLAG(-name)
                ARGUMENT('*.rb')
        FLAG(-print)

Quotation Error: space inside word '[Nn] utshell'
Example 122 (1)
Original English: search for the word "nutshell" or "Nutshell" in all the files in the folder book
English: search for word _UNK or _UNK in all file in folder _UNK
Original Command: find /book -print | xargs grep '[Nn] utshell'

Ground truth: find /book -print | xargs grep _LONG_PATTERN
Prediction: find ~jsmith -type f -exec grep LOG '{}' ; -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(~jsmith)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-exec::;)
            HEADCOMMAND(grep)
                ARGUMENT(LOG)
                ARGUMENT('{}')
        FLAG(-print)

Example 123 (1)
Original English: copy all the regular files in the current directory to the temporary diectory.
English: copy all regular file in current directory to temporary _UNK
Original Command: find . -type f -exec cp {} /tmp +

Ground truth: find . -type f -exec cp {} /tmp +
Prediction: find . -type f -exec cp UNK ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-exec::;)
            HEADCOMMAND(cp)
                ARGUMENT(UNK)

Warning: -exec missing ending ';'
il splitted into: -i -l 
Error: -il is not a flag of grep
Example 124 (1)
Original English: find all the normal/regular files in the current directory and search for the word mail and display the file names
English: find all "normal/regular" file in current directory and search for word _UNK and display file name
Original Command: find . -type f -exec grep -il mail

Ground truth: find . -type f -exec grep -i -l mail \;
Prediction: find . -type f -name '*.rb' -exec grep -H {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-name)
            ARGUMENT('*.rb')
        FLAG(-exec::;)
            HEADCOMMAND(grep)
                FLAG(-H)
                ARGUMENT({})

Error: -writable is not a flag of find
Example 125 (1)
Original English: Find writable files in the current directory tree
English: find writable file in current directory tree
Original Command: find . -writable

Ground truth: find . -writable
Prediction: find . -writable
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-writable)

Example 126 (1)
Original English: change the ownership of all regular/normal files in the current directory after users confirmation
English: change ownership of all "regular/normal" file in current directory after user confirmation
Original Command: find . -type f -ok chown username {} \;

Ground truth: find . -type f -ok chown username {} ;
Prediction: find . -user username -ok chown username {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-user)
            ARGUMENT(username)
        FLAG(-ok::;)
            HEADCOMMAND(chown)
                ARGUMENT(username)
                ARGUMENT({})

0r splitted into: -0 -r 
Error: -0r is not a flag of xargs
Error: -t is not a flag of mv
Example 127 (1)
Original English: Move the directory named "some-dir" and residing under the current one to x/
English: move directory named _UNK and residing under current "_NUM" to _UNK
Original Command: find ./ -maxdepth 1 -name "some-dir" -type d -print0 | xargs -0r mv -t x/

Ground truth: find ./ -maxdepth _NUM -name "some-dir" -type d -print0 | xargs -0 -r mv -t x/
Prediction: find . -name UNK -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(f)

Example 128 (1)
Original English: search for all the normal/regular files in the current folder and replace a pattern in them globally
English: search for all "normal/regular" file in current folder and replace pattern in _UNK
Original Command: find ./ -type f -name \*.php -exec sed -i ’s/^.*iframe bla bla bla.*$//g’ {} \;

Ground truth: find ./ -type f -name *.php -exec sed -i ’s/^.*iframe bla bla bla.*$//g’ {} ;
Prediction: find . -type f -type f -exec sed -i 's/previousword/newword/g' {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-exec::;)
            HEADCOMMAND(sed)
                FLAG(-i)
                    ARGUMENT('s/previousword/newword/g')
                ARGUMENT({})

Example 129 (1)
Original English: find all the files in the entire file system that have been accessed exactly  50 days ago
English: find all file in entire file system accessed exactly "_NUM" day ago
Original Command: find / -atime 50

Ground truth: find / -atime _NUM
Prediction: find / -atime _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-atime)
            ARGUMENT(_NUM)

Example 130 (1)
Original English: Find all *.mp4 files under /working
English: find all "*.mp_NUM" file under _UNK
Original Command: find /working -type f -name '*.mp4'

Ground truth: find /working -type f -name '*.mp_NUM'
Prediction: find UNK -name '*.mp_NUM'
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-name)
            ARGUMENT('*.mp_NUM')

Example 131 (1)
Original English: search for a file using name pattern in the multiple folders and limit the search to 2 levels.
English: search for file using name pattern in multiple folder and limit search to "_NUM" level
Original Command: find "$DIR_TEMPORAL" "$DIR_DESCARGA" -maxdepth 2 -name "$nombre" -printf '%f.torrent\n'

Ground truth: find "$DIR_TEMPORAL" "$DIR_DESCARGA" -maxdepth _NUM -name "$nombre" -printf '%f.torrent\n'
Prediction: find . -maxdepth _NUM -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-maxdepth)
            ARGUMENT(_NUM)
        FLAG(-name)
            ARGUMENT(UNK)

Quotation Error: space inside word 'Name: %16f Size: %6s\n'
Example 132 (1)
Original English: Display non-hidden files in the current directory with the given output format
English: display non-hidden file in current directory with given output format
Original Command: find . -maxdepth 1 -name '[!.]*' -printf 'Name: %16f Size: %6s\n'

Ground truth: find . -maxdepth _NUM -name '[!.]*' -printf _LONG_PATTERN
Prediction: find . -not -name "*"
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        UNARYLOGICOP(-not)
            FLAG(-name)
                ARGUMENT("*")

Example 133 (1)
Original English: Find all directories under /fss/fin
English: find all directory under "/fss/fin"
Original Command: find /fss/fin -type d

Ground truth: find /fss/fin -type d
Prediction: find /fss/fin -type d -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/fss/fin)
        FLAG(-type)
            ARGUMENT(d)
        FLAG(-print)

Example 134 (1)
Original English: Find all *1234.56789* files/directories under current directory
English: find all _UNK "files/directories" under current directory
Original Command: find . -name '*1234.56789*'

Ground truth: find . -name '*_NUM._NUM*'
Prediction: find . -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)

Error: -i is not a flag of xargs
rf splitted into: -r -f 
Error: -rf is not a flag of rm
Example 135 (1)
Original English: Remove all vmware-*.log files/directories under current directory
English: remove all _UNK "files/directories" under current directory
Original Command: find . -name vmware-*.log | xargs -i rm -rf {}

Ground truth: find . -name vmware-*.log | xargs -i rm -r -f {}
Prediction: find . -name UNK -exec rm {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT({})

Example 136 (1)
Original English: Find all files under $d directory (no sub-directories) that are executable by owner and print only their names
English: find all file under "$d" directory ( no sub-directories ) executable by owner and print only name
Original Command: find $d -maxdepth 1 -perm -100 -type f | sed 's#.*/##'

Ground truth: find $d -maxdepth _NUM -perm -_NUM -type f | sed 's#.*/##'
Prediction: find . -mindepth _NUM -type f -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-mindepth)
            ARGUMENT(_NUM)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-print)

Example 137 (1)
Original English: find all files in the file system which belong to no user or which have no user
English: find all file in file system belong to no user or no user
Original Command: find / -nouser

Ground truth: find / -nouser
Prediction: find / -nouser -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-nouser)
        FLAG(-print)

Example 138 (1)
Original English: List non-hidden regular files in the current directory tree that were last modified more than 500 days ago
English: list non-hidden regular file in current directory tree last modified more than "_NUM" day ago
Original Command: find . -type f -not -name '.*' -mtime +500 -exec ls {} \;

Ground truth: find . -type f -not -name '.*' -mtime +_NUM -exec ls {} ;
Prediction: find ~/ -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(~/)
        FLAG(-type)
            ARGUMENT(f)

Example 139 (1)
Original English: Find files modified between 6 and 9 minutes ago
English: find file modified between "_NUM" and "_NUM" minute ago
Original Command: find . -mmin +5 -mmin -10

Ground truth: find . -mmin +_NUM -mmin -_NUM
Prediction: find -mmin -_NUM -mmin -_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-mmin)
            ARGUMENT(-_NUM)
        FLAG(-mmin)
            ARGUMENT(-_NUM)

Example 140 (1)
Original English: display the three smallest files by size in a folder.
English: display "_NUM" smallest file by size in folder
Original Command: find /etc/ -type f -exec ls -s {} + | sort -n | head -3

Ground truth: find /etc/ -type f -exec ls -s {} + | sort -n | head -_NUM
Prediction: find $HOME -type f -exec ls -l {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT($HOME)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-exec::;)
            HEADCOMMAND(ls)
                FLAG(-l)
                ARGUMENT({})

Example 141 (1)
Original English: Delete all files in the "${S}/bundled-libs" folder except "libbass.so"
English: delete all file in _UNK folder except _UNK
Original Command: find "${S}/bundled-libs" \! -name 'libbass.so' -delete

Ground truth: find "${S}/bundled-libs" ! -name 'libbass.so' -delete
Prediction: find UNK -iname UNK -delete
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-iname)
            ARGUMENT(UNK)
        FLAG(-delete)

Example 142 (2)
Original English: remove all core files in the file system
English: remove all core file in file system
Original Command: find / -name "*.core" -print -exec rm {} \;

Ground truth: find / -name "*.core" -print -exec rm {} ;
Prediction: find / -name UNK exec rm -f -delete
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-name)
            ARGUMENT(UNK)
        ARGUMENT(exec)
        ARGUMENT(rm)
        FLAG(-f)
        FLAG(-delete)

Example 143 (1)
Original English: Search for all files and directories named foo, FOO, or any other combination of uppercase and lowercase characters beneath the current directory.
English: search for all file and directory named foo FOO or any other _UNK of _UNK and _UNK character beneath current directory
Original Command: find . -iname foo

Ground truth: find . -iname foo
Prediction: find . \( -name foo -prune -or -name foo \)
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        BINARYLOGICOP(-or)
            UNARYLOGICOP(-prune)
                FLAG(-name)
                    ARGUMENT(foo)
            FLAG(-name)
                ARGUMENT(foo)

Example 144 (1)
Original English: Find all *.jpg files/directories under current directory
English: find all "*.jpg" "files/directories" under current directory
Original Command: find . -name '*.jpg'

Ground truth: find . -name '*.jpg'
Prediction: find . -name "*.jpg"
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT("*.jpg")

0r splitted into: -0 -r 
Error: -0r is not a flag of xargs
Error: -t is not a flag of mv
Example 145 (1)
Original English: find all the directories with the name "some-dir" in the current folder and move them to another folder and do not search in subfolders
English: find all directory with name _UNK in current folder and move to another folder and not search in subfolders
Original Command: find ./ -maxdepth 1 -name "some-dir" -type d -print0 | xargs -0r mv -t x/

Ground truth: find ./ -maxdepth _NUM -name "some-dir" -type d -print0 | xargs -0 -r mv -t x/
Prediction: find -maxdepth _NUM -type d ! -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-maxdepth)
            ARGUMENT(_NUM)
        FLAG(-type)
            ARGUMENT(d)
        UNARYLOGICOP(!)
            FLAG(-name)
                ARGUMENT(UNK)

Example 146 (1)
Original English: find for a file in the current directory only
English: find for file in current directory only
Original Command: find -maxdepth 1 -name "sum.java"

Ground truth: find -maxdepth _NUM -name "sum.java"
Prediction: find -maxdepth _NUM -empty
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-maxdepth)
            ARGUMENT(_NUM)
        FLAG(-empty)

Example 147 (1)
Original English: Search the current directory tree for regular files whose names begin with "orapw"
English: search current directory tree for regular file whose name begin with _UNK
Original Command: find . -name "orapw*" -type f

Ground truth: find . -name "orapw*" -type f
Prediction: find . -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)

Error: --with-filename is not a flag of grep
Example 148 (1)
Original English: Search all files in the current directory tree that are named "whatever" for "you_search_for_it"
English: search all file in current directory tree named "whatever" for _UNK
Original Command: find -name whatever -exec grep --with-filename you_search_for_it {} \;

Ground truth: find -name whatever -exec grep --with-filename you_search_for_it {} ;
Prediction: find . -name '*.html' | xargs grep whatever
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-name)
                ARGUMENT('*.html')
        HEADCOMMAND(xargs)
            HEADCOMMAND(grep)
                ARGUMENT(whatever)

Example 149 (1)
Original English: copy all java files from current folder to another folder
English: copy all java file from current folder to another folder
Original Command: find . -name "*.java" -print0 | xargs -0 -J % cp % destinationFolder

Ground truth: find . -name "*.java" -print0 | xargs -0 -J % cp % destinationFolder
Prediction: find . -name "*.java" -exec cp _NUM ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT("*.java")
        FLAG(-exec::;)
            HEADCOMMAND(cp)
                ARGUMENT(_NUM)

I{} splitted into: -I -{ -} 
Error: -I{} is not a flag of xargs
Example 150 (1)
Original English: Find all *.txt files under current directory and copy them to ./tmp
English: find all "*.txt" file under current directory and copy to _UNK
Original Command: find . -type f -name '*.txt' | sed 's/'"'"'/\'"'"'/g' | sed 's/.*/"&"/'  | xargs -I{} cp -v {} ./tmp/

Ground truth: find . -type f -name '*.txt' | sed 's/'"'"'/\'"'"'/g' | sed 's/.*/"&"/' | xargs -I -{ -} cp -v {} ./tmp/
Prediction: find . -name "*.txt" -type f | xargs cp -f UNK
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-name)
                ARGUMENT("*.txt")
            FLAG(-type)
                ARGUMENT(f)
        HEADCOMMAND(xargs)
            HEADCOMMAND(cp)
                FLAG(-f)
                ARGUMENT(UNK)

Quotation Error: space inside word '%s %p\n'
Example 151 (1)
Original English: List all files under current directory with their sizes and paths
English: list all file under current directory with size and path
Original Command: find . -type f -printf '%s %p\n'

Ground truth: find . -type f -printf _LONG_PATTERN
Prediction: find . -type f -printf _LONG_PATTERN
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-printf)
            ARGUMENT(_LONG_PATTERN)

Example 152 (1)
Original English: Find recursively all regular files changed within the last 5 minutes starting from directory b
English: find recursively all regular file changed within last "_NUM" minute starting from directory b
Original Command: find b -type f -cmin -5

Ground truth: find b -type f -cmin -_NUM
Prediction: find b -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(b)
        FLAG(-type)
            ARGUMENT(f)

Example 153 (1)
Original English: Find the passwd file in the current directory and one level down
English: find passwd file in current directory and "_NUM" level down
Original Command: find -maxdepth 2 -name passwd

Ground truth: find -maxdepth _NUM -name passwd
Prediction: find -maxdepth _NUM -mindepth _NUM -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-maxdepth)
            ARGUMENT(_NUM)
        FLAG(-mindepth)
            ARGUMENT(_NUM)
        FLAG(-type)
            ARGUMENT(f)

Example 154 (1)
Original English: Find all jpg images
English: find all jpg image
Original Command: find . -name "*.jpg"

Ground truth: find . -name "*.jpg"
Prediction: find . -type f -iregex UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-iregex)
            ARGUMENT(UNK)

Error: --transform=s|^.*/|| is not a flag of tar
Error: --show-transformed is not a flag of tar
zcpvf splitted into: -z -c -p -v -f 
Error: -zcpvf is not a flag of tar
Example 155 (1)
Original English: Archive all directories in /path/to/directory/* (only command line arguments, no sub-directories) to files with .tar.gz extension transforming the full paths to relative paths
English: archive all directory in _UNK ( only command line argument no sub-directories ) to file with ".tar.gz" extension _UNK full path to relative path
Original Command: find /path/* -maxdepth 0 -type d -exec sudo tar --transform='s|^.*/||' --show-transformed -zcpvf {}.tar.gz {} \;

Ground truth: find /path/* -maxdepth _NUM -type d -exec tar --transform='s|^.*/||' --show-transformed -z -c -p -v -f {}.tar.gz {} ;
Prediction: find '*/\.*' -mindepth _NUM -type f -printf "%P\n"
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT('*/\.*')
        FLAG(-mindepth)
            ARGUMENT(_NUM)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-printf)
            ARGUMENT("%P\n")

Error: -chour is not a flag of find
Error: -exit is not a flag of find
Error: -exit is not a flag of find
Example 156 (2)
Original English: Test if a file named 'file' in the current directory is more than 1 hour old
English: test if file named "file" in current directory more than "_NUM" hour old
Original Command: find file -prune -cmin +60 -print | grep -q .

Ground truth: find file -prune -cmin +_NUM -print | grep -q .
Prediction: find . -newer +_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-newer)
            ARGUMENT(+_NUM)

Error: -regextype is not a flag of find
Example 157 (1)
Original English: Find all directories under current directory whose paths are 5 characters long
English: find all directory under current directory whose path "_NUM" character long
Original Command: find . -regextype posix-extended -type d -regex ".{5}"

Ground truth: find . -regextype posix-extended -type d -regex ".{_NUM}"
Prediction: find . -type d -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(d)
        FLAG(-name)
            ARGUMENT(UNK)

Example 158 (1)
Original English: Search the current directory recursively for regular files last accessed more than 2 days ago
English: search current directory recursively for regular file last accessed more than "_NUM" day ago
Original Command: find . type -f -atime +2

Ground truth: find . type -f -atime +_NUM
Prediction: find . type -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        ARGUMENT(type)
        FLAG(-type)
            ARGUMENT(f)

Example 159 (1)
Original English: display all files in the folder bar only in the path /foo/bar/myfile (no output is generated)
English: display all file in folder bar only in path _UNK ( no output _UNK )
Original Command: find bar -path /foo/bar/myfile -print

Ground truth: find bar -path /foo/bar/myfile -print
Prediction: find UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)

Example 160 (1)
Original English: Find all the files in entire file system  which are accessed 50 days back
English: find all file in entire file system accessed "_NUM" day back
Original Command: find / -atime 50

Ground truth: find / -atime _NUM
Prediction: find / -atime _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-atime)
            ARGUMENT(_NUM)

Error: -mitime is not a flag of find
Error: -1 is not a flag of find
Example 161 (1)
Original English: find all the files that have been modified in the last 2 day
English: find all file modified in last "_NUM" day
Original Command: find -daystart -mitime -1

Ground truth: find -daystart -mitime -1
Prediction: find -daystart -daystart -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-daystart)
        FLAG(-daystart)
        FLAG(-type)
            ARGUMENT(f)

Example 162 (1)
Original English: Find all files/directories in entire file system that are exactly 50 bytes
English: find all "files/directories" in entire file system exactly "_NUM" byte
Original Command: find / -size 50c

Ground truth: find / -size _NUMc
Prediction: find / -size _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-size)
            ARGUMENT(_NUM)

iazZ splitted into: -i -a -z -Z 
Error: -iazZ is not a flag of egrep
vazZ splitted into: -v -a -z -Z 
Error: -vazZ is not a flag of grep
Hi splitted into: -H -i 
Error: -Hi is not a flag of grep
Example 163 (1)
Original English: FInd files in current directory and grep text and html files - but not index.html and report things that contain the word 'elevator' in four or more lines
English: _UNK file in current directory and grep text and html file _UNK but not _UNK and report _UNK contain word _UNK in "_NUM" or more line
Original Command: find . -type f -print0 | egrep -iazZ '(\.txt|\.html?)$' | grep -vazZ 'index.html' | xargs -n 1 -0 grep -c -Hi elevator | egrep -v ':[0123]$'

Ground truth: find . -type f -print0 | egrep -i -a -z -Z '(\.txt|\.html?)$' | grep -v -a -z -Z 'index.html' | xargs -n _NUM -0 grep -c -H -i elevator | egrep -v ':[_NUM]$'
Prediction: find . -name UNK -exec rm {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT({})

Example 164 (1)
Original English: Find out all *.sh owned by user vivek
English: find out all "*.sh" owned by user _UNK
Original Command: find / -user vivek -name "*.sh"

Ground truth: find / -user vivek -name "*.sh"
Prediction: find / -user UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-user)
            ARGUMENT(UNK)

Example 165 (1)
Original English: search for directories in a folder and change the permissions to 755
English: search for directory in folder and change permission to "_NUM"
Original Command: find "$d/" -type d -print0 | xargs -0 chmod 755

Ground truth: find "$d/" -type d -print0 | xargs -0 chmod _NUM
Prediction: find . -type d -exec chmod _NUM ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(d)
        FLAG(-exec::;)
            HEADCOMMAND(chmod)
                ARGUMENT(_NUM)

Example 166 (1)
Original English: Find all *.* directories under /home/feeds/data directory
English: find all _UNK directory under "/home/feeds/data" directory
Original Command: find /home/feeds/data -type d \( -name 'def/incoming' -o -name '456/incoming' -o -name arkona \) -prune -o -name '*.*' -print

Ground truth: find /home/feeds/data -type d \( -name 'def/incoming' -or -name '_NUM/incoming' -or -name arkona \) \( -prune -or -name '*.*' \) -print
Prediction: find /home/feeds/data -type d -name Cookbook
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/home/feeds/data)
        FLAG(-type)
            ARGUMENT(d)
        FLAG(-name)
            ARGUMENT(Cookbook)

Example 167 (1)
Original English: List all *.bak files in the current directory tree
English: list all "*.bak" file in current directory tree
Original Command: find  . -name '*.bak' -ls

Ground truth: find . -name '*.bak' -ls
Prediction: find . -name UNK -exec ls -l {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-exec::;)
            HEADCOMMAND(ls)
                FLAG(-l)
                ARGUMENT({})

Example 168 (1)
Original English: Find all files in  /mydir  and replace every occurrences of <string1> with <string2> in those files invoking sed as few times as possible
English: find all file in "/mydir" and replace every occurrence of _UNK with _UNK in file _UNK sed few time _UNK
Original Command: find /mydir -type f -exec sed -i 's/<string1>/<string2>/g' {} +

Ground truth: find /mydir -type f -exec sed -i 's/<string_NUM>/<string_NUM>/g' {} +
Prediction: find /usr -type f -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/usr)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-print)

Example 169 (1)
Original English: Find all files/directories named file in 2 and 3 levels down the current directory
English: find all "files/directories" named file in "_NUM" and "_NUM" level down current directory
Original Command: find -mindepth 2 -maxdepth 3 -name file

Ground truth: find -mindepth _NUM -maxdepth _NUM -name file
Prediction: find -mindepth _NUM -name file
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-mindepth)
            ARGUMENT(_NUM)
        FLAG(-name)
            ARGUMENT(file)

Quotation Error: space inside word 'admin.log. [0-9] [0-9][О-9] '
Quotation Error: space inside word  rm
Example 170 (1)
Original English: remove all the log files  which have not been accessed in the last 7 days and which have specific name pattern
English: remove all log file not accessed in last "_NUM" day and specific name pattern
Original Command: find /logs -name 'admin.log. [0-9] [0-9][О-9] ' — atime +7 exec \ rm {} \;

Ground truth: find /logs -name _LONG_PATTERN — atime +_NUM exec _LONG_PATTERN {} ;
Prediction: find . -name '*.ogg' -exec rm {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT('*.ogg')
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT({})

Error: -executable is not a flag of find
Example 171 (1)
Original English: Search the current directory tree for executable files and searchable directories
English: search current directory tree for executable file and _UNK directory
Original Command: find -executable

Ground truth: find -executable
Prediction: find . -perm /etc
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-perm)
            ARGUMENT(/etc)

Example 172 (1)
Original English: find all the configuration files which have been accessed in the last 30 minutes.
English: find all configuration file accessed in last "_NUM" minute
Original Command: find /etc/sysconfig -amin -30

Ground truth: find /etc/sysconfig -amin -_NUM
Prediction: find / -amin -_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-amin)
            ARGUMENT(-_NUM)

Example 173 (1)
Original English: Search the current directory and its sub-directories for any file that has "bsd" somewhere in its name.
English: search current directory and sub-directories for any file ha _UNK somewhere in name
Original Command: find . -name "*bsd*" -print

Ground truth: find . -name "*bsd*" -print
Prediction: find . -name *disc*
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(*disc*)

Example 174 (1)
Original English: Print the file names along with their sizes under current directory tree
English: print file name along with size under current directory tree
Original Command: find . -type f -printf "%f %s\n"

Ground truth: find . -type f -printf _LONG_PATTERN
Prediction: find . -type d -printf _LONG_PATTERN
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(d)
        FLAG(-printf)
            ARGUMENT(_LONG_PATTERN)

Example 175 (1)
Original English: display all the files with the names "name1" and "name2" in the current folder and do not search in the sub directories
English: display all file with name _UNK and _UNK in current folder and not search in sub directory
Original Command: find . -maxdepth 1 -name "name1" -o -name "name2"

Ground truth: find . -maxdepth _NUM \( -name "name_NUM" -or -name "name_NUM" \)
Prediction: find -maxdepth _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-maxdepth)
            ARGUMENT(_NUM)

Example 176 (1)
Original English: Print a sorted list of regular files from directory tree /folder/of/stuff
English: print sorted list of regular file from directory tree _UNK
Original Command: find /folder/of/stuff -type f | sort

Ground truth: find /folder/of/stuff -type f | sort
Prediction: find UNK -type f | sort -u
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(UNK)
            FLAG(-type)
                ARGUMENT(f)
        HEADCOMMAND(sort)
            FLAG(-u)

Example 177 (1)
Original English: find all the files in the current folder and display them in the sorted order of their name
English: find all file in current folder and display in sorted order of name
Original Command: find . | sort

Ground truth: find . | sort
Prediction: find . | awk _LONG_PATTERN
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
        HEADCOMMAND(awk)
            ARGUMENT(_LONG_PATTERN)

Example 178 (1)
Original English: Remove all files under current directory
English: remove all file under current directory
Original Command: find -exec rm '{}' +

Ground truth: find -exec rm '{}' +
Prediction: find . -type f | xargs rm
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-type)
                ARGUMENT(f)
        HEADCOMMAND(xargs)
            HEADCOMMAND(rm)

Example 179 (1)
Original English: Locate all files in the current directory and below that do not have "testfileasdf" in their names
English: locate all file in current directory and below not _UNK in name
Original Command: find -not -name "*testfileasdf*"

Ground truth: find -not -name "*testfileasdf*"
Prediction: find . -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)

Example 180 (1)
Original English: Find files that don’t have 644 permissions
English: find file _UNK "_NUM" permission
Original Command: find / -type f ! -perm 644

Ground truth: find / -type f ! -perm _NUM
Prediction: find . -perm _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-perm)
            ARGUMENT(_NUM)

Example 181 (1)
Original English: Find all hidden files
English: find all hidden file
Original Command: find /tmp -type f -name ".*"

Ground truth: find /tmp -type f -name ".*"
Prediction: find . -name ".*"
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(".*")

Error: -xdev is not a flag of find
Example 182 (1)
Original English: Delete all hard links to the physical file with inode number 2655341
English: delete all hard link to _UNK file with inode number "_NUM"
Original Command: find /home -xdev -inum 2655341 | xargs rm

Ground truth: find /home -xdev -inum _NUM | xargs rm
Prediction: find / -inum _NUM -inum _NUM -exec rm _NUM ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-inum)
            ARGUMENT(_NUM)
        FLAG(-inum)
            ARGUMENT(_NUM)
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT(_NUM)

Error: -xdev is not a flag of find
Error: -xdev is not a flag of find
Example 183 (2)
Original English: Delete all contents form the files that contain the case insensitive regex 'stringtofind' in maximum 1 level down the / directory excluding other partitions
English: delete all content form file contain case insensitive regex "stringtofind" in maximum "_NUM" level down "/" directory excluding other partition
Original Command: find / -maxdepth 1 -xdev -type f -exec grep -i "stringtofind" -l {} \; -exec sed -i '/./d' {} \;

Ground truth: find / -maxdepth _NUM -xdev -type f -exec grep -i "stringtofind" -l {} ; -exec sed -i '/./d' {} ;
Prediction: find / -maxdepth _NUM -type f | xargs -0 grep -i "stringtofind"
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(/)
            FLAG(-maxdepth)
                ARGUMENT(_NUM)
            FLAG(-type)
                ARGUMENT(f)
        HEADCOMMAND(xargs)
            FLAG(-0)
            HEADCOMMAND(grep)
                FLAG(-i)
                ARGUMENT("stringtofind")

Example 184 (1)
Original English: Print the list of files in directory /tmp/a1 recursively
English: print list of file in directory _UNK recursively
Original Command: find /tmp/a1

Ground truth: find /tmp/a_NUM
Prediction: find /usr -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/usr)
        FLAG(-print)

Example 185 (1)
Original English: Find all *.mp3 (case insensitive) files/directories under /tmp and remove them
English: find all "*.mp_NUM" ( case insensitive ) "files/directories" under "/tmp" and remove
Original Command: find /tmp -iname '*.mp3' -print0 | xargs -0 rm

Ground truth: find /tmp -iname '*.mp_NUM' -print0 | xargs -0 rm
Prediction: find /tmp -iname '*.ogg' -type f -exec rm {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/tmp)
        FLAG(-iname)
            ARGUMENT('*.ogg')
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT({})

Example 186 (1)
Original English: Find all the files without permission 777 in the file system
English: find all file without permission "_NUM" in file system
Original Command: find / -type f ! -perm 777

Ground truth: find / -type f ! -perm _NUM
Prediction: find / -type f -perm _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-perm)
            ARGUMENT(_NUM)

Example 187 (1)
Original English: find all jpg files in the current folder
English: find all jpg file in current folder
Original Command: find . -name "*.jpg"

Ground truth: find . -name "*.jpg"
Prediction: find . -type f -name "*.JPG"
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-name)
            ARGUMENT("*.JPG")

Example 188 (1)
Original English: Count the number of files/directories named file1 under current directory
English: count number of "files/directories" named "file_NUM" under current directory
Original Command: find -name file1 | wc -l

Ground truth: find -name file_NUM | wc -l
Prediction: find -name file_NUM
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            FLAG(-name)
                ARGUMENT(file_NUM)

Example 189 (1)
Original English: display all the files in the current folder excluding the directory aa
English: display all file in current folder excluding directory aa
Original Command: find . -type d ! -name aa

Ground truth: find . -type d ! -name aa
Prediction: find . \( -name UNK -prune -or -print \)
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        BINARYLOGICOP(-or)
            UNARYLOGICOP(-prune)
                FLAG(-name)
                    ARGUMENT(UNK)
            FLAG(-print)

x+r splitted into: -x -+ -r 
Error: -x+r is not a flag of chmod
Example 190 (1)
Original English: change the permissions of all the files ending with "fits" in the folder "/store/01"
English: change permission of all file ending with _UNK in folder _UNK
Original Command: find /store/01 -name "*.fits" -exec chmod -x+r {} \; \

Ground truth: find /store/_NUM -name "*.fits" -exec chmod -x -+ -r {} ;
Prediction: find UNK -name UNK -type f -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-print)

Example 191 (1)
Original English: Find all files in the /home/ directory tree that are owned by bob
English: find all file in "/home/" directory tree owned by _UNK
Original Command: find /home -user bob

Ground truth: find /home -user bob
Prediction: find /home
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/home)

Example 192 (1)
Original English: Search directories "./dir1" and "./dir2" for a file "foo.bar"
English: search directory "./dir_NUM" and "./dir_NUM" for file "foo.bar"
Original Command: find ./dir1 ./dir2 -name foo.bar -print

Ground truth: find ./dir_NUM ./dir_NUM -name foo.bar -print
Prediction: find /etc -name foo.bar
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/etc)
        FLAG(-name)
            ARGUMENT(foo.bar)

Example 193 (1)
Original English: Find all regular files in the current directory tree that have been modified within the last 10 minutes
English: find all regular file in current directory tree modified within last "_NUM" minute
Original Command: find . –type f -mmin -10

Ground truth: find . –type f -mmin -_NUM
Prediction: find . -mmin -_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-mmin)
            ARGUMENT(-_NUM)

Example 194 (1)
Original English: display all the regular files in current folder that belong to the user "tom"
English: display all regular file in current folder belong to user _UNK
Original Command: find . -type f -user tom

Ground truth: find . -type f -user tom
Prediction: find . -type f -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-print)

Example 195 (1)
Original English: Find files in the current directory tree whose pathnames contain "sub"
English: find file in current directory tree whose pathnames contain _UNK
Original Command: find ./ | grep "sub"

Ground truth: find ./ | grep "sub"
Prediction: find . UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        ARGUMENT(UNK)

Example 196 (1)
Original English: delete all the files in the file system which belong to the user edwarda
English: delete all file in file system belong to user _UNK
Original Command: find / -user edwarda -exec rm "{}" \;

Ground truth: find / -user edwarda -exec rm "{}" ;
Prediction: find / -user www -user www -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-user)
            ARGUMENT(www)
        FLAG(-user)
            ARGUMENT(www)
        FLAG(-print)

rvf splitted into: -r -v -f 
Error: -rvf is not a flag of rm
Example 197 (1)
Original English: To descend at most one levels of directories below the command line arguments pass the -maxdepth 1 option. This will avoid deleting nested directories:
English: to descend at most "_NUM" level of directory below command line argument pas _UNK "_NUM" option will _UNK _UNK _UNK directory
Original Command: find .  -maxdepth 1 -type d -iname ".[^.]*" -print0 | xargs -I {} -0 rm -rvf "{}"

Ground truth: find . -maxdepth _NUM -type d -iname ".[^.]*" -print0 | xargs -I {} -0 rm -r -v -f "{}"
Prediction: find -path UNK -prune -path "*/.*" -prune
AST: 
ROOT(root)
    HEADCOMMAND(find)
        UNARYLOGICOP(-prune)
            FLAG(-path)
                ARGUMENT(UNK)
        BINARYLOGICOP(-or)
            UNARYLOGICOP(-prune)
                FLAG(-path)
                    ARGUMENT("*/.*")

Example 198 (1)
Original English: Search /usr, /home, /tmp for *.jar files
English: search "/usr" "/home" "/tmp" for _UNK file
Original Command: find /usr /home  /tmp -name "*.jar"

Ground truth: find /usr /home /tmp -name "*.jar"
Prediction: find /usr /usr -name foo
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/usr)
        ARGUMENT(/usr)
        FLAG(-name)
            ARGUMENT(foo)

Example 199 (3)
Original English: Search for all files with either "sitesearch" or "demo" in their path names
English: search for all file with either "sitesearch" or "demo" in path name
Original Command: find . -ipath '*sitesearch*' -ipath '*demo*'

Ground truth: find . -ipath '*sitesearch*' -ipath '*demo*'
Prediction: find . -regex UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-regex)
            ARGUMENT(UNK)

Example 200 (1)
Original English: Look for a file by group
English: look for file by group
Original Command: find /  -type f -group users

Ground truth: find / -type f -group users
Prediction: find . -perm /_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-perm)
            ARGUMENT(/_NUM)

Example 201 (1)
Original English: Search for 'mystring' in all *.txt (case insensitive) files under current directory
English: search for "mystring" in all "*.txt" ( case insensitive ) file under current directory
Original Command: find . -iname *.txt -exec egrep mystring \{\} \;

Ground truth: find . -iname *.txt -exec egrep mystring {} ;
Prediction: find . -iname "*.txt" -exec egrep mystring ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-iname)
            ARGUMENT("*.txt")
        FLAG(-exec::;)
            HEADCOMMAND(egrep)
                ARGUMENT(mystring)

Example 202 (1)
Original English: find all the files in the entire filesystem which belong to the group root and display the ten files.
English: find all file in entire filesystem belong to group root and display "_NUM" file
Original Command: find / -group root | head

Ground truth: find / -group root | head
Prediction: find / -group
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-group)

Example 203 (1)
Original English: Search the home directory tree for files matching pattern '*.txt'
English: search home directory tree for file matching pattern "*.txt"
Original Command: find ~ -name *.txt

Ground truth: find ~ -name *.txt
Prediction: find build -name *.txt egrep '.*myfile[_NUM-_NUM][_NUM-_NUM]?'
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(build)
        FLAG(-name)
            ARGUMENT(*.txt)
    HEADCOMMAND(egrep)
        ARGUMENT('.*myfile[_NUM-_NUM][_NUM-_NUM]?')

Example 204 (1)
Original English: Find *.txt files in the current directory tree, ignoring paths ./Movies/*, ./Downloads/*, and ./Music/*
English: find "*.txt" file in current directory tree ignoring path _UNK _UNK and _UNK
Original Command: find . -type f -name "*.txt" ! -path "./Movies/*" ! -path "./Downloads/*" ! -path "./Music/*"

Ground truth: find . -type f -name "*.txt" ! -path "./Movies/*" ! -path "./Downloads/*" ! -path "./Music/*"
Prediction: find . \( -path excluded_path -prune -or -name '*.rb' \) -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        BINARYLOGICOP(-or)
            UNARYLOGICOP(-prune)
                FLAG(-path)
                    ARGUMENT(excluded_path)
            FLAG(-name)
                ARGUMENT('*.rb')
        FLAG(-print)

Example 205 (1)
Original English: find all directories that names are 'project.images'
English: find all directory name _UNK
Original Command: find  / -type d -name "project.images"

Ground truth: find / -type d -name "project.images"
Prediction: find -name Cookbook
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-name)
            ARGUMENT(Cookbook)

Example 206 (1)
Original English: Search for all files that end in ".conf"
English: search for all file end in ".conf"
Original Command: find / -type f -name "*.conf"

Ground truth: find / -type f -name "*.conf"
Prediction: find $HOME -name *.tar.gz
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT($HOME)
        FLAG(-name)
            ARGUMENT(*.tar.gz)

Example 207 (1)
Original English: display all files in the entire file system excluding those that are in the transfer directory
English: display all file in entire file system excluding in _UNK directory
Original Command: find / -name /transfer -prune -o -print

Ground truth: find / \( -name /transfer -prune -or -print \)
Prediction: find / -wholename UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-wholename)
            ARGUMENT(UNK)

Example 208 (1)
Original English: Find all regular files in the current directory tree whose names end with ".DS_Store" and delete them
English: find all regular file in current directory tree whose name end with _UNK and delete
Original Command: find . -type f -name '*.DS_Store' -ls -delete

Ground truth: find . -type f -name '*.DS_Store' -ls -delete
Prediction: find . -type f -name UNK -delete
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-delete)

Example 209 (1)
Original English: display all the directories in the current folder excluding those that are present in the folder secret
English: display all directory in current folder excluding present in folder _UNK
Original Command: find . -name secret -type d -prune -o -print

Ground truth: find . -name secret \( -type d -prune -or -print \)
Prediction: find . -type d -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(d)
        FLAG(-print)

Example 210 (1)
Original English: list symbolic links under the directory "$directory" using contents of the $IFS variable between output of each one
English: list symbolic link under directory "$directory" using content of _UNK variable between output of each "_NUM"
Original Command: find $directory -type l -printf "%p$IFS"

Ground truth: find $directory -type l -printf "%p$IFS"
Prediction: find /usr -type l -perm +_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/usr)
        FLAG(-type)
            ARGUMENT(l)
        FLAG(-perm)
            ARGUMENT(+_NUM)

Example 211 (1)
Original English: find all the files in the current directory which have been modified in the  last 6 days.
English: find all file in current directory modified in last "_NUM" day
Original Command: find . -atime +6

Ground truth: find . -atime +_NUM
Prediction: find . -mtime -_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-mtime)
            ARGUMENT(-_NUM)

Example 212 (1)
Original English: display all the normal/regular files in a directory
English: display all "normal/regular" file in directory
Original Command: find $dir -type f -name $name -print

Ground truth: find $dir -type f -name $name -print
Prediction: find UNK -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(f)

Example 213 (1)
Original English: Find all *.sh files owned by user vivek
English: find all "*.sh" file owned by user _UNK
Original Command: find / -user vivek -name "*.sh"

Ground truth: find / -user vivek -name "*.sh"
Prediction: find / -user UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-user)
            ARGUMENT(UNK)

Example 214 (1)
Original English: Find all *.tex files/directories in maximum 2 levels down the current directory
English: find all "*.tex" "files/directories" in maximum "_NUM" level down current directory
Original Command: find . -maxdepth 2 -name '*.tex'

Ground truth: find . -maxdepth _NUM -name '*.tex'
Prediction: find -maxdepth _NUM -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-maxdepth)
            ARGUMENT(_NUM)
        FLAG(-type)
            ARGUMENT(f)

Example 215 (1)
Original English: find all files in a folder that start with a specific name ( case insensitive search)
English: find all file in folder start with specific name ( case insensitive search )
Original Command: find /usr/share/doc -iname readme\*

Ground truth: find /usr/share/doc -iname readme*
Prediction: find . -iname "*blast*"
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-iname)
            ARGUMENT("*blast*")

Example 216 (1)
Original English: Find all files that belongs to user Tecmint under /home directory
English: find all file belongs to user tecmint under "/home" directory
Original Command: find /home -user tecmint

Ground truth: find /home -user tecmint
Prediction: find /home -user UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/home)
        FLAG(-user)
            ARGUMENT(UNK)

Example 217 (1)
Original English: search all the files in the current folder using regex excluding those that are present in the folder test
English: search all file in current folder using regex excluding present in folder test
Original Command: find . -name test -prune -o -regex ".*/my.*p.$"

Ground truth: find . \( -name test -prune -or -regex ".*/my.*p.$" \)
Prediction: find . -regex ".*/my.*p.$"
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-regex)
            ARGUMENT(".*/my.*p.$")

Quotation Error: space inside word 's/ *$//'
Example 218 (1)
Original English: Remove trailing white spaces from all files under dir directory
English: remove trailing white space from all file under dir directory
Original Command: find dir -type f -exec sed -i 's/ *$//' '{}' ';'

Ground truth: find dir -type f -exec sed -i _LONG_PATTERN '{}' ;
Prediction: find /path/to/dir \( -name '*.rb' -prune -or -name *.png \) -exec sed -i {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/path/to/dir)
        BINARYLOGICOP(-or)
            UNARYLOGICOP(-prune)
                FLAG(-name)
                    ARGUMENT('*.rb')
            FLAG(-name)
                ARGUMENT(*.png)
        FLAG(-exec::;)
            HEADCOMMAND(sed)
                FLAG(-i)
                ARGUMENT({})

Example 219 (1)
Original English: Find all directories under /home/username/public_html/sites/default/files and set their permission to 770
English: find all directory under _UNK and set permission to "_NUM"
Original Command: find /home/username/public_html/sites/default/files -type d -exec chmod 770 {} +

Ground truth: find /home/username/public_html/sites/default/files -type d -exec chmod _NUM {} +
Prediction: find UNK -type d -exec chmod _NUM +
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(d)
        FLAG(-exec::+)
            HEADCOMMAND(chmod)
                ARGUMENT(_NUM)

Quotation Error: space inside word '{total += $7} END {print total}'
Example 220 (1)
Original English: find all the files ending with undo in the current folder and calculate the total size of these files
English: find all file ending with undo in current folder and calculate total size of file
Original Command: find . -name "*.undo" -ls | awk '{total += $7} END {print total}'

Ground truth: find . -name "*.undo" -ls | awk _LONG_PATTERN
Prediction: find . -name *.ini | tail _NUM
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-name)
                ARGUMENT(*.ini)
        HEADCOMMAND(tail)
            ARGUMENT(_NUM)

I@ splitted into: -I -@ 
Error: -I@ is not a flag of xargs
Example 221 (1)
Original English: find all the files with a specific permissin and change the permissions
English: find all file with specific _UNK and change permission
Original Command: find -perm 777 | xargs -I@ sudo chmod 755 '@'

Ground truth: find -perm _NUM | xargs -I -@ chmod _NUM '@'
Prediction: find . -perm _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-perm)
            ARGUMENT(_NUM)

Example 222 (1)
Original English: remove all the log files which have not been modified in the last 5 days
English: remove all log file not modified in last "_NUM" day
Original Command: find /logs -type f -mtime +5 -exec rm {} \;

Ground truth: find /logs -type f -mtime +_NUM -exec rm {} ;
Prediction: find -not -name +_NUM -daystart -mtime +_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        UNARYLOGICOP(-not)
            FLAG(-name)
                ARGUMENT(+_NUM)
        FLAG(-daystart)
        FLAG(-mtime)
            ARGUMENT(+_NUM)

Example 223 (1)
Original English: Print a sorted list of all .jpg files in the current directory and below
English: print sorted list of all ".jpg" file in current directory and below
Original Command: find -name '*.jpg' | sort -n

Ground truth: find -name '*.jpg' | sort -n
Prediction: find . -name UNK | sort
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-name)
                ARGUMENT(UNK)
        HEADCOMMAND(sort)

Example 224 (1)
Original English: search for the file "file" in the current folder excluding those in the sub directory ".git"
English: search for file "file" in current folder excluding in sub directory ".git"
Original Command: find . -path ./.git  -prune -o -name file  -print

Ground truth: find . \( -path ./.git -prune -or -name file \) -print
Prediction: find . \( -name '*.foo' -prune -or -name '*.foo' \) -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        BINARYLOGICOP(-or)
            UNARYLOGICOP(-prune)
                FLAG(-name)
                    ARGUMENT('*.foo')
            FLAG(-name)
                ARGUMENT('*.foo')
        FLAG(-print)

Example 225 (1)
Original English: Find all files under current directory and print only the filenames (not paths)
English: find all file under current directory and print only filename ( not path )
Original Command: find . -type f -printf "%f\n"

Ground truth: find . -type f -printf "%f\n"
Prediction: find . -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)

Example 226 (1)
Original English: Find *.c and *.sh files
English: find "*.c" and "*.sh" file
Original Command: find . -type f \( -name "*.c" -o -name "*.sh" \)

Ground truth: find . -type f \( -name "*.c" -or -name "*.sh" \)
Prediction: find . -name '*.[ch]'
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT('*.[ch]')

Example 227 (1)
Original English: search for the file, filename.txt in the current folder ( case insensitive search )
English: search for file "filename.txt" in current folder ( case insensitive search )
Original Command: find . -iname filename.txt

Ground truth: find . -iname filename.txt
Prediction: find . -iname UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-iname)
            ARGUMENT(UNK)

Example 228 (1)
Original English: display all directories in the entire file system
English: display all directory in entire file system
Original Command: find / -type d -print

Ground truth: find / -type d -print
Prediction: find / -type d
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-type)
            ARGUMENT(d)

Example 229 (1)
Original English: Find all files on the system whose names are 'composer.json'
English: find all file on system whose name _UNK
Original Command: find / -name composer.json

Ground truth: find / -name composer.json
Prediction: find / -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-name)
            ARGUMENT(UNK)

Example 230 (1)
Original English: Search the "your/dir" directory for empty subdirectories
English: search "your/dir" directory for empty subdirectory
Original Command: find your/dir -mindepth 1 -prune -empty

Ground truth: find your/dir -mindepth _NUM -prune -empty
Prediction: find -prune -mindepth _NUM -type d -empty
AST: 
ROOT(root)
    HEADCOMMAND(find)
        UNARYLOGICOP(-prune)
        FLAG(-mindepth)
            ARGUMENT(_NUM)
        FLAG(-type)
            ARGUMENT(d)
        FLAG(-empty)

Example 231 (1)
Original English: Find all files named "something" in the current folder and below and run them through the ls -l command in a one batch.
English: find all file named "something" in current folder and below and run through l _UNK command in "_NUM" _UNK
Original Command: find . -name something | xargs -0 ls

Ground truth: find . -name something | xargs -0 ls
Prediction: find . -name something -exec ls -l {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(something)
        FLAG(-exec::;)
            HEADCOMMAND(ls)
                FLAG(-l)
                ARGUMENT({})

Example 232 (1)
Original English: Find all *.swp files/directories under current directory
English: find all "*.swp" "files/directories" under current directory
Original Command: find . -name "*.swp"

Ground truth: find . -name "*.swp"
Prediction: find . -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)

Error: -newermt is not a flag of find
Error: -newermt is not a flag of find
Example 233 (1)
Original English: display a long listing of all the regular/normal files in the current folder that have been modified after a specific timestamp
English: display long listing of all "regular/normal" file in current folder modified after specific timestamp
Original Command: find . -type f -newermt ‘Apr 18 23:59:59 EDT 2013’ ! -newermt ‘Apr 20 00:00:00 EDT 2013’ -exec ls -l ‘{}’ \;

Ground truth: find . -type f -newermt ‘Apr _NUM _NUM:_NUM:_NUM EDT _NUM’ ! -newermt ‘Apr _NUM _NUM:_NUM:_NUM EDT _NUM’ -exec ls -l ‘{}’ ;
Prediction: find . -type f UNK UNK UNK UNK UNK UNK UNK -exec ls -l UNK ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        ARGUMENT(UNK)
        ARGUMENT(UNK)
        ARGUMENT(UNK)
        ARGUMENT(UNK)
        ARGUMENT(UNK)
        ARGUMENT(UNK)
        ARGUMENT(UNK)
        FLAG(-exec::;)
            HEADCOMMAND(ls)
                FLAG(-l)
                ARGUMENT(UNK)

Example 234 (1)
Original English: display the three largest files by size in current folder
English: display "_NUM" largest file by size in current folder
Original Command: find . -type f -exec ls -s {} + | sort -n -r | head -3

Ground truth: find . -type f -exec ls -s {} + | sort -n -r | head -_NUM
Prediction: find . -type f -perm -_NUM | awk _LONG_PATTERN
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-type)
                ARGUMENT(f)
            FLAG(-perm)
                ARGUMENT(-_NUM)
        HEADCOMMAND(awk)
            ARGUMENT(_LONG_PATTERN)

Example 235 (1)
Original English: Find all `$VERSION*` files/directories under current directory where `$VERSION` is a string literal
English: find all _UNK "files/directories" under current directory where "$VERSION" string literal
Original Command: find . -name '*`$VERSION`*'

Ground truth: find . -name '*`$VERSION`*'
Prediction: find . -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)

Example 236 (1)
Original English: Find all the files without permission 777
English: find all file without permission "_NUM"
Original Command: find / -type f ! -perm 777

Ground truth: find / -type f ! -perm _NUM
Prediction: find . -type f -perm _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-perm)
            ARGUMENT(_NUM)

Example 237 (1)
Original English: List all your files including everything in sub-directories
English: list all file including everything in sub-directories
Original Command: find ~

Ground truth: find ~
Prediction: find . -name "*.txt"
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT("*.txt")

Quotation Error: space inside word '* *'
Example 238 (1)
Original English: Find all files/directories with spaces in their names under ~/Library directory
English: find all "files/directories" with space in name under "~/Library" directory
Original Command: find ~/Library -name '* *'

Ground truth: find ~/Library -name _LONG_PATTERN
Prediction: find ~/Library -name ~/Library
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(~/Library)
        FLAG(-name)
            ARGUMENT(~/Library)

Error: -i is not a flag of xargs
rf splitted into: -r -f 
Error: -rf is not a flag of rm
Example 239 (5)
Original English: Remove all files with names like "vmware-*.log" from the current directory tree
English: remove all file with name like _UNK from current directory tree
Original Command: find . -name vmware-*.log | xargs -i rm -rf {}

Ground truth: find . -name vmware-*.log | xargs -i rm -r -f {}
Prediction: find . -name UNK | xargs rm
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-name)
                ARGUMENT(UNK)
        HEADCOMMAND(xargs)
            HEADCOMMAND(rm)

Example 240 (1)
Original English: Search the current directory and directories below for .sql files
English: search current directory and directory below for _UNK file
Original Command: find . -name \*.sql

Ground truth: find . -name *.sql
Prediction: find . -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)

Quotation Error: space inside word '%M %u %g %p\n'
Example 241 (2)
Original English: List level 2 subdirectories of the current directory
English: list level "_NUM" subdirectory of current directory
Original Command: find . -mindepth 2 -maxdepth 2 -type d -printf '%M %u %g %p\n'

Ground truth: find . -mindepth _NUM -maxdepth _NUM -type d -printf _LONG_PATTERN
Prediction: find -mindepth _NUM -mindepth _NUM -mindepth _NUM -type d
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-mindepth)
            ARGUMENT(_NUM)
        FLAG(-mindepth)
            ARGUMENT(_NUM)
        FLAG(-mindepth)
            ARGUMENT(_NUM)
        FLAG(-type)
            ARGUMENT(d)

Example 242 (1)
Original English: search in the current folder for all the regular/normal file with the name "test"
English: search in current folder for all "regular/normal" file with name "test"
Original Command: find . -type f -name test

Ground truth: find . -type f -name test
Prediction: find . -type f -name test
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-name)
            ARGUMENT(test)

Example 243 (1)
Original English: find all the directories in the current directory which dont have the execute permission.
English: find all directory in current directory dont execute permission
Original Command: find -type d ! -perm -111

Ground truth: find -type d ! -perm -_NUM
Prediction: find . -type d -perm _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(d)
        FLAG(-perm)
            ARGUMENT(_NUM)

Example 244 (1)
Original English: find all the files in the folder /usr/bin which have been modified in the last 10 days
English: find all file in folder "/usr/bin" modified in last "_NUM" day
Original Command: find /usr/bin -type f -mtime -10

Ground truth: find /usr/bin -type f -mtime -_NUM
Prediction: find /usr/bin -type f -mtime -_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/usr/bin)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-mtime)
            ARGUMENT(-_NUM)

Example 245 (1)
Original English: find all the files in the file system which belong to the user "pat" and with the name "dateiname"
English: find all file in file system belong to user _UNK and with name "dateiname"
Original Command: find / -user pat -iname "Dateiname"

Ground truth: find / -user pat -iname "Dateiname"
Prediction: find / -user www -iname "Dateiname"
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-user)
            ARGUMENT(www)
        FLAG(-iname)
            ARGUMENT("Dateiname")

Example 246 (1)
Original English: find all the regular files in a folder which have not been modified in the last 15 days and delete them
English: find all regular file in folder not modified in last "_NUM" day and delete
Original Command: find "$DIR" -type f -mtime +15 -exec rm {} \;

Ground truth: find "$DIR" -type f -mtime +_NUM -exec rm {} ;
Prediction: find UNK -daystart -type f -exec rm {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-daystart)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT({})

Example 247 (1)
Original English: Perform a default Plesk configuration
English: perform default _UNK configuration
Original Command: find /var/www/vhosts/*/httpdocs -type f -iwholename “*/wp-includes/version.php” -exec grep -H “\$wp_version =” {} \;

Ground truth: find /var/www/vhosts/*/httpdocs -type f -iwholename “*/wp-includes/version.php” -exec grep -H “$wp_version =” {} ;
Prediction: find /home/*/public_html/ -type f UNK -exec grep -H UNK ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/home/*/public_html/)
        FLAG(-type)
            ARGUMENT(f)
        ARGUMENT(UNK)
        FLAG(-exec::;)
            HEADCOMMAND(grep)
                FLAG(-H)
                ARGUMENT(UNK)

Error: -fprintf is not a flag of find
Example 248 (1)
Original English: List all files/directories under current directory with their inode numbers, disk space, permission, number of hard links, user name, group name, size, status change time in Y-m-d format and name filed,  then write the outptut to /tmp/files.txt
English: list all "files/directories" under current directory with inode number disk space permission number of hard link user name group name size status change time in _UNK format and name _UNK write _UNK to _UNK
Original Command: find . -type f -fprintf /tmp/files.txt "%i,%b,%M,%n,%u,%g,%s,%CY-%Cm-%Cd %CT,%p\n"

Ground truth: find . -type f -fprintf /tmp/files.txt _LONG_PATTERN
Prediction: find . -inum _NUM -exec chmod _NUM {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-inum)
            ARGUMENT(_NUM)
        FLAG(-exec::;)
            HEADCOMMAND(chmod)
                ARGUMENT(_NUM)
                ARGUMENT({})

Example 249 (1)
Original English: Fix permissions for a group of files with given extension
English: fix permission for group of file with given extension
Original Command: find /usr/local -name "*.html" -type f -exec chmod 644 {} \;

Ground truth: find /usr/local -name "*.html" -type f -exec chmod _NUM {} ;
Prediction: find . -group UNK -name UNK -exec chmod _NUM ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-group)
            ARGUMENT(UNK)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-exec::;)
            HEADCOMMAND(chmod)
                ARGUMENT(_NUM)

Example 250 (1)
Original English: show all the ".acc" files in the folder /home
English: show all _UNK file in folder "/home"
Original Command: find /home -type f -name '*.aac'

Ground truth: find /home -type f -name '*.aac'
Prediction: find /home -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/home)
        FLAG(-name)
            ARGUMENT(UNK)

Example 251 (1)
Original English: find all files in etc which have been changed in the last 25 hours
English: find all file in etc changed in last "_NUM" hour
Original Command: find /etc -ctime -1

Ground truth: find /etc -ctime -_NUM
Prediction: find / -ctime -_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-ctime)
            ARGUMENT(-_NUM)

Example 252 (1)
Original English: change the owner of all the regular/normal files which belong to the root user to "tom" in the current folder
English: change owner of all "regular/normal" file belong to root user to _UNK in current folder
Original Command: find .-type f -user root -exec chown tom {} \;

Ground truth: find .-type f -user root -exec chown tom {} ;
Prediction: find . -user UNK -user UNK -type f -user UNK -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-user)
            ARGUMENT(UNK)
        FLAG(-user)
            ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-user)
            ARGUMENT(UNK)
        FLAG(-print)

Example 253 (1)
Original English: Find all files in /var/www/html/zip/data/*/*/*/*/* that are older than 90 days
English: find all file in _UNK older than "_NUM" day
Original Command: find /var/www/html/zip/data/*/*/*/*/* -type f -mtime +90

Ground truth: find /var/www/html/zip/data/*/*/*/*/* -type f -mtime +_NUM
Prediction: find /usr -mtime +_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/usr)
        FLAG(-mtime)
            ARGUMENT(+_NUM)

Example 254 (1)
Original English: find all files in home folder that begin with a specific word
English: find all file in home folder begin with specific word
Original Command: find ~ -iname "screen*"

Ground truth: find ~ -iname "screen*"
Prediction: find $HOME -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT($HOME)
        FLAG(-name)
            ARGUMENT(UNK)

Example 255 (1)
Original English: find all regular files in current folder with a specific permission and display the total count
English: find all regular file in current folder with specific permission and display total count
Original Command: find . -type f -perm 755 | wc -l

Ground truth: find . -type f -perm _NUM | wc -l
Prediction: find . -type f -perm _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-perm)
            ARGUMENT(_NUM)

Example 256 (1)
Original English: search for all the files in the folder /data/images which have been modified after /tmp/start and before /tmp/end
English: search for all file in folder _UNK modified after _UNK and before _UNK
Original Command: find /data/images -type f -newer /tmp/start -not -newer /tmp/end

Ground truth: find /data/images -type f -newer /tmp/start -not -newer /tmp/end
Prediction: find /etc -newer UNK -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/etc)
        FLAG(-newer)
            ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(f)

Example 257 (1)
Original English: Find files/directories named<filetype> under current directory which were accessed less than 5 days ago
English: find "files/directories" _UNK under current directory accessed le than "_NUM" day ago
Original Command: find -name "<filetype>" -atime -5

Ground truth: find -name "<filetype>" -atime -_NUM
Prediction: find . -atime -_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-atime)
            ARGUMENT(-_NUM)

Example 258 (1)
Original English: Find *log files/directories within a maximum of 3 levels of directories
English: find _UNK "files/directories" within maximum of "_NUM" level of directory
Original Command: find / -maxdepth 3  -name "*log"

Ground truth: find / -maxdepth _NUM -name "*log"
Prediction: find -maxdepth _NUM -mindepth _NUM -name 'upvoter-*'
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-maxdepth)
            ARGUMENT(_NUM)
        FLAG(-mindepth)
            ARGUMENT(_NUM)
        FLAG(-name)
            ARGUMENT('upvoter-*')

Example 259 (1)
Original English: List all .jpg files in the home directory tree in a fast way
English: list all ".jpg" file in home directory tree in _UNK way
Original Command: find . -name "*.jpg" -exec ls {} +

Ground truth: find . -name "*.jpg" -exec ls {} +
Prediction: find . -name "*.jpg" -exec ls ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT("*.jpg")
        FLAG(-exec::;)
            HEADCOMMAND(ls)

Example 260 (1)
Original English: display all directories in current folder excluding those that are present in .git folder
English: display all directory in current folder excluding present in ".git" folder
Original Command: find . -iregex '.*/.git/.*' -prune -o -type d -name 'CVS'

Ground truth: find . \( -iregex '.*/.git/.*' -prune -or -type d \) -name 'CVS'
Prediction: find . -type d -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(d)
        FLAG(-print)

Example 261 (1)
Original English: list all .c or .sh regular files.
English: list all ".c" or ".sh" regular file
Original Command: find . -type f \( -name "*.c" -o -name "*.sh" \)

Ground truth: find . -type f \( -name "*.c" -or -name "*.sh" \)
Prediction: find . \( -name "*.sh" -or -name "*.sh" \)
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        BINARYLOGICOP(-or)
            FLAG(-name)
                ARGUMENT("*.sh")
            FLAG(-name)
                ARGUMENT("*.sh")

Example 262 (1)
Original English: find all  tools generated files  a.out , *.o and core dump files which not required to us these all junk files & delete from  current  directory .
English: find all _UNK _UNK file "a.out" "*.o" and core _UNK file not _UNK to _UNK all junk file "&" delete from current directory
Original Command: find . \( -name a.out -o -name '*.' -o -name  'core' \) -exec rm {} \;

Ground truth: find . \( -name a.out -or -name '*.' -or -name 'core' \) -exec rm {} ;
Prediction: find . \( -name a.out -or -name UNK \) -type f -name UNK -exec rm {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        BINARYLOGICOP(-or)
            FLAG(-name)
                ARGUMENT(a.out)
            FLAG(-name)
                ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT({})

Example 263 (1)
Original English: Find all files that belong to group root
English: find all file belong to group root
Original Command: find / -group root

Ground truth: find / -group root
Prediction: find / -group developer
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-group)
            ARGUMENT(developer)

Example 264 (1)
Original English: To list files in your home directory tree whose names begin with the string `top', and that are newer than the file `/etc/motd'.  You can combine many of find's options to find files that match multiple criteria.
English: to list file in home directory tree whose name begin with string _LONG_PATTERN combine many of "find\'s" option to find file match multiple _UNK
Original Command: find ~ -name 'top*' -newer /etc/motd

Ground truth: find ~ -name 'top*' -newer /etc/motd
Prediction: find . -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)

Example 265 (1)
Original English: Find all image.pdf files under ./polkadots
English: find all "image.pdf" file under "./polkadots"
Original Command: find ./polkadots -type f -name "image.pdf"

Ground truth: find ./polkadots -type f -name "image.pdf"
Prediction: find ./polkadots -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(./polkadots)
        FLAG(-name)
            ARGUMENT(UNK)

Example 266 (1)
Original English: display all text files in the current folder
English: display all text file in current folder
Original Command: find . -type f -name "*.txt"

Ground truth: find . -type f -name "*.txt"
Prediction: find . -name ".txt"
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(".txt")

Quotation Error: space inside word '/re/ {print FILENAME ":" $0;exit}'
Example 267 (1)
Original English: Search for first match of the regex 're' in all *.coffee files under current directory and print the file names
English: search for first match of regex _UNK in all "*.coffee" file under current directory and print file name
Original Command: find . -name \*.coffee -exec awk '/re/ {print FILENAME ":" $0;exit}' {} \;

Ground truth: find . -name *.coffee -exec awk _LONG_PATTERN {} ;
Prediction: find . -name UNK -type f -print | xargs grep -l -i {}
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-name)
                ARGUMENT(UNK)
            FLAG(-type)
                ARGUMENT(f)
            FLAG(-print)
        HEADCOMMAND(xargs)
            HEADCOMMAND(grep)
                FLAG(-l)
                FLAG(-i)
                ARGUMENT({})

Example 268 (1)
Original English: Find all directories under current directory whose names are 33 characters long
English: find all directory under current directory whose name "_NUM" character long
Original Command: find . -type d -name "?????????????????????????????????"

Ground truth: find . -type d -name "?????????????????????????????????"
Prediction: find . -type d -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(d)
        FLAG(-name)
            ARGUMENT(UNK)

Quotation Error: space inside word 's/2013 Magento Inc./2012 Magento Inc./g'
Example 269 (1)
Original English: search for php, xml, phtml files in current folder and replace a pattern in all these files
English: search for php xml _UNK file in current folder and replace pattern in all file
Original Command: find . -name '*.php' -print0 -o -name '*.xml' -print0 -o -name '*.phtml' -print0 | xargs -0 sed -i '' 's/2013 Magento Inc./2012 Magento Inc./g'

Ground truth: find . -name '*.php' \( -print0 -or -name '*.xml' \) \( -print0 -or -name '*.phtml' \) -print0 | xargs -0 sed -i '' _LONG_PATTERN
Prediction: find . -name '*.php' -exec sed -i UNK {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT('*.php')
        FLAG(-exec::;)
            HEADCOMMAND(sed)
                FLAG(-i)
                    ARGUMENT(UNK)
                ARGUMENT({})

Example 270 (1)
Original English: list txt files older than 5 days or html files of any age, null separated
English: list txt file older than "_NUM" day or html file of any _UNK null separated
Original Command: find . \( -name '*.txt'  -mtime +5 -o -name '*.html' \) -print0

Ground truth: find . \( -name '*.txt' -and \( -mtime +_NUM -or -name '*.html' \) \) -print0
Prediction: find UNK -name '*.html'
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        BINARYLOGICOP(-or)
            FLAG(-name)
                ARGUMENT('*.html')

Example 271 (1)
Original English: Find all MP3 files in the home directory tree that were modified in the last 24 hours
English: find all "MP_NUM" file in home directory tree modified in last "_NUM" hour
Original Command: find ~ -type f -mtime 0 -iname '*.mp3'

Ground truth: find ~ -type f -mtime _NUM -iname '*.mp_NUM'
Prediction: find $HOME -mtime +_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT($HOME)
        FLAG(-mtime)
            ARGUMENT(+_NUM)

Example 272 (1)
Original English: Find all files in the current directory tree whose names are ".DS_STORE"
English: find all file in current directory tree whose name _UNK
Original Command: find . -name ".DS_STORE"

Ground truth: find . -name ".DS_STORE"
Prediction: find . -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)

Example 273 (1)
Original English: display all the files in the current directory excluding those that are in the 'secret' directory
English: display all file in current directory excluding in _UNK directory
Original Command: find . -name 'secret' -prune -o -print

Ground truth: find . \( -name 'secret' -prune -or -print \)
Prediction: find . -wholename UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-wholename)
            ARGUMENT(UNK)

Example 274 (1)
Original English: find all the directories in the file system which begin with "man"
English: find all directory in file system begin with _UNK
Original Command: find / -type d -name 'man*' -print

Ground truth: find / -type d -name 'man*' -print
Prediction: find / -name UNK -type d
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(d)

Example 275 (1)
Original English: Find files owned by no user
English: find file owned by no user
Original Command: find / -nouser

Ground truth: find / -nouser
Prediction: find / -nouser
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-nouser)

Example 276 (1)
Original English: To list all files in the `/usr/local/fonts' directory tree owned by the user warwick  To find files owned by a particular user, give the username to search for as an argument to the `-user' option.
English: to list all file in _UNK directory tree owned by user _UNK to find file owned by particular user give _UNK to search for argument to _UNK option
Original Command: find /usr/local/fonts -user warwick

Ground truth: find /usr/local/fonts -user warwick
Prediction: find /var/www -user UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/var/www)
        FLAG(-user)
            ARGUMENT(UNK)

Example 277 (1)
Original English: search for a pattern in all the files in the current folder which have a specific name pattern
English: search for pattern in all file in current folder specific name pattern
Original Command: find . -name '*.[ch]' | xargs grep -E 'expr'

Ground truth: find . -name '*.[ch]' | xargs grep -E 'expr'
Prediction: find . -name * -exec grep -H string-to-find {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(*)
        FLAG(-exec::;)
            HEADCOMMAND(grep)
                FLAG(-H)
                ARGUMENT(string-to-find)
                ARGUMENT({})

Example 278 (1)
Original English: Find files that do not have a listing in the /etc/passwd or /etc/group in the file system
English: find file not listing in "/etc/passwd" or _UNK in file system
Original Command: find / -nouser -o  -nogroup

Ground truth: find / \( -nouser -or -nogroup \)
Prediction: find / \( -newer UNK -or -name UNK \)
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        BINARYLOGICOP(-or)
            FLAG(-newer)
                ARGUMENT(UNK)
            FLAG(-name)
                ARGUMENT(UNK)

Example 279 (1)
Original English: search for a file "file" in current folder and display the file.
English: search for file "file" in current folder and display file
Original Command: find -name file -prune

Ground truth: find -name file -prune
Prediction: find -name file
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-name)
            ARGUMENT(file)

Example 280 (1)
Original English: Search the current directory recursively for .sh files whose names begin with "new"
English: search current directory recursively for ".sh" file whose name begin with "new"
Original Command: find . -name "new*.sh"

Ground truth: find . -name "new*.sh"
Prediction: find . -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)

Example 281 (1)
Original English: find all the files in the current directory which have been modified in the last 30 days and display the contents.
English: find all file in current directory modified in last "_NUM" day and display content
Original Command: find . -atime +30 -exec ls \;

Ground truth: find . -atime +_NUM -exec ls ;
Prediction: find . -mtime -_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-mtime)
            ARGUMENT(-_NUM)

Quotation Error: space inside word  
Quotation Error: space inside word  
Quotation Error: space inside word  
Quotation Error: space inside word  
Quotation Error: space inside word  
Quotation Error: space inside word  
Quotation Error: space inside word  
Quotation Error: space inside word  
Example 282 (1)
Original English: list all js files under currect directory exculde the directory which path contain "/path/to/search/exclude_me" or name isexclude_me_too_anywhere
English: list all j file under _UNK directory _UNK directory path contain _UNK or name _UNK
Original Command: find /path/to/search                    \   -type d                               \     \( -path /path/to/search/exclude_me \        -o                               \        -name exclude_me_too_anywhere    \      \)                                 \     -prune                              \   -o                                    \   -type f -name '*\.js' -print

Ground truth: find /path/to/search _LONG_PATTERN -type d _LONG_PATTERN \( -path /path/to/search/exclude_me -and \( _LONG_PATTERN -or _LONG_PATTERN \) -and -name exclude_me_too_anywhere -and _LONG_PATTERN \) _LONG_PATTERN -prune \( _LONG_PATTERN -or _LONG_PATTERN \) -type f -name '*\.js' -print
Prediction: find UNK -name UNK -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(f)

Example 283 (1)
Original English: List all *.jar files/directories under /usr, /home and /tmp directory
English: list all _UNK "files/directories" under "/usr" "/home" and "/tmp" directory
Original Command: find /usr /home  /tmp -name "*.jar"

Ground truth: find /usr /home /tmp -name "*.jar"
Prediction: find /usr -name *stat
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/usr)
        FLAG(-name)
            ARGUMENT(*stat)

Example 284 (2)
Original English: Remove all files with a txt extension under current directory
English: remove all file with txt extension under current directory
Original Command: find . -type f -name "*.txt" -print|xargs rm

Ground truth: find . -type f -name "*.txt" -print | xargs rm
Prediction: find . -name UNK -exec rm {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT({})

Example 285 (1)
Original English: display a long list of all the files that are bigger than 10KB in current folder
English: display long list of all file bigger than "_NUMKB" in current folder
Original Command: find . -size +10k -exec ls -l {} \;

Ground truth: find . -size +_NUMk -exec ls -l {} ;
Prediction: find . -xdev -ls
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-xdev)
        FLAG(-ls)

Example 286 (1)
Original English: display all instances of the .profile file in the entire file system
English: display all instance of _UNK file in entire file system
Original Command: find / -name .profile -print

Ground truth: find / -name .profile -print
Prediction: find / \( -newer UNK -or -name UNK -or -name UNK \)
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        BINARYLOGICOP(-or)
            FLAG(-newer)
                ARGUMENT(UNK)
            FLAG(-name)
                ARGUMENT(UNK)
            FLAG(-name)
                ARGUMENT(UNK)

Example 287 (1)
Original English: To list all of the files in your home directory tree that were modified yesterday  Include the `-daystart' option to measure time from the beginning of the current day instead of 24 hours ago.
English: to list all of file in home directory tree modified yesterday include _UNK option to measure time from beginning of current day instead of "_NUM" hour ago
Original Command: find ~ -mtime 1 -daystart

Ground truth: find ~ -mtime _NUM -daystart
Prediction: find UNK -mindepth _NUM -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-mindepth)
            ARGUMENT(_NUM)
        FLAG(-type)
            ARGUMENT(f)

Example 288 (1)
Original English: Searches through the /usr/local directory for files that end with the extension .html. When these files are found, their permission is changed to mode 644 (rw-r--r--).
English: search through "/usr/local" directory for file end with extension ".html" when file found permission changed to mode "_NUM" ( _UNK )
Original Command: find /usr/local -name "*.html" -type f -exec chmod 644 {} \;

Ground truth: find /usr/local -name "*.html" -type f -exec chmod _NUM {} ;
Prediction: find /usr/local -name "*.html" -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/usr/local)
        FLAG(-name)
            ARGUMENT("*.html")
        FLAG(-type)
            ARGUMENT(f)

Example 289 (1)
Original English: Find all *foo files/directories under current directory
English: find all _UNK "files/directories" under current directory
Original Command: find . -name '*foo'

Ground truth: find . -name '*foo'
Prediction: find . -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)

Example 290 (1)
Original English: Find all directories named 'octave' under current directory tree
English: find all directory named _UNK under current directory tree
Original Command: find . -name "octave" -type d

Ground truth: find . -name "octave" -type d
Prediction: find . -type d -name Cookbook
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(d)
        FLAG(-name)
            ARGUMENT(Cookbook)

Example 291 (1)
Original English: Find all regular files under ${S} directory
English: find all regular file under _UNK directory
Original Command: find "${S}" -type f

Ground truth: find "${S}" -type f
Prediction: find UNK -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(f)

Error: -xdev is not a flag of find
Error: -xdev is not a flag of find
Example 292 (2)
Original English: Find and delete all hard links in the /home directory to file1
English: find and delete all hard link in "/home" directory to "file_NUM"
Original Command: find /home -xdev -samefile file1 -print0 | xargs -0 rm

Ground truth: find /home -xdev -samefile file_NUM -print0 | xargs -0 rm
Prediction: find /home -xdev -samefile file_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/home)
        FLAG(-xdev)
        FLAG(-samefile)
            ARGUMENT(file_NUM)

Example 293 (1)
Original English: Find all .c, .h files in the current directory tree and search them for string "expr"
English: find all ".c" ".h" file in current directory tree and search for string "expr"
Original Command: find . -name '*.[ch]' | xargs grep -E 'expr'

Ground truth: find . -name '*.[ch]' | xargs grep -E 'expr'
Prediction: find -name '*.[ch]' | xargs grep -E 'expr'
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            FLAG(-name)
                ARGUMENT('*.[ch]')
        HEADCOMMAND(xargs)
            HEADCOMMAND(grep)
                FLAG(-E)
                ARGUMENT('expr')

Example 294 (1)
Original English: Find all regular files that reside in the current directory tree and were last modified more than 2 days ago
English: find all regular file reside in current directory tree and last modified more than "_NUM" day ago
Original Command: find . -type f -mtime +2

Ground truth: find . -type f -mtime +_NUM
Prediction: find . -type f -mtime +_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-mtime)
            ARGUMENT(+_NUM)

Example 295 (1)
Original English: Find all the files which are accessed 50 days back
English: find all file accessed "_NUM" day back
Original Command: find / -atime 50

Ground truth: find / -atime _NUM
Prediction: find / -atime _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-atime)
            ARGUMENT(_NUM)

Example 296 (1)
Original English: Find directories in the current directory tree whose names are 33 characters in length
English: find directory in current directory tree whose name "_NUM" character in length
Original Command: find . -type d -name "?????????????????????????????????"

Ground truth: find . -type d -name "?????????????????????????????????"
Prediction: find . -name Cookbook
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(Cookbook)

Example 297 (1)
Original English: Search the /usr/ directory tree for files newer than file /tmp/stamp
English: search _UNK directory tree for file newer than file _UNK
Original Command: find /usr -newer /tmp/stamp

Ground truth: find /usr -newer /tmp/stamp
Prediction: find UNK -newer /etc/motd
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-newer)
            ARGUMENT(/etc/motd)

Error: -2 is not a flag of find
Example 298 (1)
Original English: Search the current directory recursively for regular files last accessed less than 2 days ago
English: search current directory recursively for regular file last accessed le than "_NUM" day ago
Original Command: find . type -f -atime -2

Ground truth: find . type -f -atime -2
Prediction: find . type type -2
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        ARGUMENT(type)
        ARGUMENT(type)
        FLAG(-2)

Example 299 (1)
Original English: display long listing of all the empty files in the current folder
English: display long listing of all empty file in current folder
Original Command: find . -empty -exec ls -l {} \;

Ground truth: find . -empty -exec ls -l {} ;
Prediction: find . -empty -delete
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-empty)
        FLAG(-delete)

Example 300 (1)
Original English: Find the passwd file under root and one level down.
English: find passwd file under root and "_NUM" level down
Original Command: find -maxdepth 2 -name passwd

Ground truth: find -maxdepth _NUM -name passwd
Prediction: find / -maxdepth _NUM -name passwd
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-maxdepth)
            ARGUMENT(_NUM)
        FLAG(-name)
            ARGUMENT(passwd)

Example 301 (1)
Original English: Find all directories in the current directory tree that are not accessible by all
English: find all directory in current directory tree not accessible by all
Original Command: find -type d ! -perm -111

Ground truth: find -type d ! -perm -_NUM
Prediction: find -type d
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-type)
            ARGUMENT(d)

Example 302 (1)
Original English: Search /usr/bin for regular files that have been modified within the last 10 days
English: search "/usr/bin" for regular file modified within last "_NUM" day
Original Command: find /usr/bin -type f -mtime -10

Ground truth: find /usr/bin -type f -mtime -_NUM
Prediction: find /usr/bin -type f -mtime -_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/usr/bin)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-mtime)
            ARGUMENT(-_NUM)

al splitted into: -a -l 
Error: -al is not a flag of ls
Example 303 (1)
Original English: display a long listing of all the directories in the entire file system
English: display long listing of all directory in entire file system
Original Command: find / -print0 -type d | xargs -0 ls -al

Ground truth: find / -print0 -type d | xargs -0 ls -a -l
Prediction: find / -type d -ls
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-type)
            ARGUMENT(d)
        FLAG(-ls)

Example 304 (1)
Original English: find all the cpp files in the folder "/myprojects" and replace a pattern in these files for each file
English: find all cpp file in folder _UNK and replace pattern in file for each file
Original Command: find /myprojects -type f -name '*.cpp' -print0 | xargs -0 -n 1 sed -i 's/previousword/newword/g'

Ground truth: find /myprojects -type f -name '*.cpp' -print0 | xargs -0 -n _NUM sed -i 's/previousword/newword/g'
Prediction: find UNK -type f -name UNK -exec sed -i 's/previousword/newword/g' {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-exec::;)
            HEADCOMMAND(sed)
                FLAG(-i)
                    ARGUMENT('s/previousword/newword/g')
                ARGUMENT({})

Example 305 (1)
Original English: This command will only list files that contain between 1,000 and 10,000 characters.
English: command will only list file contain between "_NUM" "_NUM" and "_NUM" "_NUM" character
Original Command: find . -size +1000c -size -10000c -print

Ground truth: find . -size +_NUMc -size -_NUMc -print
Prediction: find . -size -_NUMk -type f -size -_NUMk | awk "filename"
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-size)
                ARGUMENT(-_NUMk)
            FLAG(-type)
                ARGUMENT(f)
            FLAG(-size)
                ARGUMENT(-_NUMk)
        HEADCOMMAND(awk)
            ARGUMENT("filename")

Quotation Error: space inside word '/re/ {print;exit}'
Example 306 (1)
Original English: find all the files ending with ".coffee" in the current folder and search for the first occurence of the word "re" in each line
English: find all file ending with _UNK in current folder and search for first _UNK of word _UNK in each line
Original Command: find . -name '*.coffee' -exec awk '/re/ {print;exit}' {} \;

Ground truth: find . -name '*.coffee' -exec awk _LONG_PATTERN {} ;
Prediction: find . -name UNK -exec grep -H UNK -exec grep -H UNK {} ; ; | xargs grep -H UNK
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-name)
                ARGUMENT(UNK)
            FLAG(-exec::;)
                HEADCOMMAND(grep)
                    FLAG(-H)
                    ARGUMENT(UNK)
                    FLAG(-exec::;)
                        HEADCOMMAND(grep)
                            FLAG(-H)
                            ARGUMENT(UNK)
                            ARGUMENT({})
        HEADCOMMAND(xargs)
            HEADCOMMAND(grep)
                FLAG(-H)
                ARGUMENT(UNK)

Example 307 (1)
Original English: Count total number of lines in all *txt files  in current directory
English: count total number of line in all _UNK file in current directory
Original Command: wc -l `find . -type f -name '*.txt' `

Ground truth: wc -l $( find . -type f -name '*.txt' )
Prediction: find . -type f -name '*' -exec wc -l ; | wc -l
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-type)
                ARGUMENT(f)
            FLAG(-name)
                ARGUMENT('*')
            FLAG(-exec::;)
                HEADCOMMAND(wc)
                    FLAG(-l)
        HEADCOMMAND(wc)
            FLAG(-l)

Example 308 (1)
Original English: Find all hidden files under /tmp
English: find all hidden file under "/tmp"
Original Command: find /tmp -type f -name ".*"

Ground truth: find /tmp -type f -name ".*"
Prediction: find /tmp -path '*/.*'
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/tmp)
        FLAG(-path)
            ARGUMENT('*/.*')

Example 309 (1)
Original English: Change permissions to 644 for *.html files under /usr/local
English: change permission to "_NUM" for "*.html" file under "/usr/local"
Original Command: find /usr/local -name "*.html" -type f -exec chmod 644 {} \;

Ground truth: find /usr/local -name "*.html" -type f -exec chmod _NUM {} ;
Prediction: find /usr/local -type f -name "*.html" -exec chmod _NUM ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/usr/local)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-name)
            ARGUMENT("*.html")
        FLAG(-exec::;)
            HEADCOMMAND(chmod)
                ARGUMENT(_NUM)

Example 310 (1)
Original English: find foo, Foo, FOo, FOO, etc.
English: find foo foo _UNK FOO etc
Original Command: find . -iname foo

Ground truth: find . -iname foo
Prediction: find . -iname foo
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-iname)
            ARGUMENT(foo)

Example 311 (1)
Original English: display all regular/normal files in the folder "dir" and display the filename along with file size
English: display all "regular/normal" file in folder "dir" and display filename along with file size
Original Command: find dir -type f -printf "f %s %p\n"

Ground truth: find dir -type f -printf _LONG_PATTERN
Prediction: find . -type f -printf _LONG_PATTERN
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-printf)
            ARGUMENT(_LONG_PATTERN)

Example 312 (1)
Original English: count lines of C or C++ or Obj-C or Java code under the current directory
English: count line of C or "C++" or _UNK or java code under current directory
Original Command: find . \( -name "*.c" -or -name "*.cpp" -or -name "*.h" -or -name "*.m" -or -name '*.java' \) -print0 | xargs -0 wc

Ground truth: find . \( -name "*.c" -or -name "*.cpp" -or -name "*.h" -or -name "*.m" -or -name '*.java' \) -print0 | xargs -0 wc
Prediction: find . \( -name UNK -or -name "*.cpp" \)
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        BINARYLOGICOP(-or)
            FLAG(-name)
                ARGUMENT(UNK)
            FLAG(-name)
                ARGUMENT("*.cpp")

Example 313 (1)
Original English: Search for symlinks pointing to anywhere within /mnt/oldname/
English: search for symlinks pointing to anywhere within _UNK
Original Command: find / -type l -lname '/mnt/oldname*'

Ground truth: find / -type l -lname '/mnt/oldname*'
Prediction: find -L -type l
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-L)
        FLAG(-type)
            ARGUMENT(l)

Example 314 (1)
Original English: Find all links to path/to/file
English: find all link to _UNK
Original Command: find -L -samefile path/to/file

Ground truth: find -L -samefile path/to/file
Prediction: find / -samefile UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-samefile)
            ARGUMENT(UNK)

il splitted into: -i -l 
Error: -il is not a flag of grep
Example 315 (1)
Original English: search for a specific word in all the normal files in a folder(print0 is used to handle files with new line in their names)
English: search for specific word in all normal file in folder( "print_NUM" used to handle file with new line in name )
Original Command: find ~/Documents -type f -print0 | xargs -0 grep -il birthday

Ground truth: find ~/Documents -type f -print0 | xargs -0 grep -i -l birthday
Prediction: find . -iname "*.php" -exec grep -H {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-iname)
            ARGUMENT("*.php")
        FLAG(-exec::;)
            HEADCOMMAND(grep)
                FLAG(-H)
                ARGUMENT({})

Example 316 (1)
Original English: Search three folders named foo, bar, and baz for all "*.rb" files
English: search "_NUM" folder named foo bar and _UNK for all "*.rb" file
Original Command: find foo bar baz -name "*.rb"

Ground truth: find foo bar baz -name "*.rb"
Prediction: find . \( -name '*.rb' -or -name UNK -or -name UNK \) -exec grep -l UNK {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        BINARYLOGICOP(-or)
            FLAG(-name)
                ARGUMENT('*.rb')
            FLAG(-name)
                ARGUMENT(UNK)
            FLAG(-name)
                ARGUMENT(UNK)
        FLAG(-exec::;)
            HEADCOMMAND(grep)
                FLAG(-l)
                ARGUMENT(UNK)
                ARGUMENT({})

Example 317 (1)
Original English: display all normal/regular files in the folder "pathfolder"
English: display all "normal/regular" file in folder "pathfolder"
Original Command: find pathfolder -type f

Ground truth: find pathfolder -type f
Prediction: find pathfolder -name '*.conf'
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(pathfolder)
        FLAG(-name)
            ARGUMENT('*.conf')

Error: -t is not a flag of mv
Error: -t is not a flag of mv
Error: -t is not a flag of mv
Example 318 (4)
Original English: Find directories in the current directory tree that were modified within the last 24 hours and move them to /path/to/target-dir
English: find directory in current directory tree modified within last "_NUM" hour and move to _UNK
Original Command: find . -type d -mtime -0 -print0 | xargs -0 mv -t /path/to/target-dir

Ground truth: find . -type d -mtime -_NUM -print0 | xargs -0 mv -t /path/to/target-dir
Prediction: find . -mtime _NUM -type f -exec mv {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-mtime)
            ARGUMENT(_NUM)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-exec::;)
            HEADCOMMAND(mv)
                ARGUMENT({})

Example 319 (1)
Original English: Find all executable files under current directory and reverse sort them
English: find all executable file under current directory and reverse sort
Original Command: find . -perm -111 -type f | sort -r

Ground truth: find . -perm -_NUM -type f | sort -r
Prediction: find . -type f -perm _NUM | sort -r chmod _NUM
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-type)
                ARGUMENT(f)
            FLAG(-perm)
                ARGUMENT(_NUM)
        HEADCOMMAND(sort)
            FLAG(-r)
            HEADCOMMAND(chmod)
                ARGUMENT(_NUM)

Example 320 (1)
Original English: Search for file "file" between level 2 and 3 of the directory tree
English: search for file "file" between level "_NUM" and "_NUM" of directory tree
Original Command: find -mindepth 2 -maxdepth 3 -name file

Ground truth: find -mindepth _NUM -maxdepth _NUM -name file
Prediction: find -mindepth _NUM -mindepth _NUM -name -mindepth _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-mindepth)
            ARGUMENT(_NUM)
        FLAG(-mindepth)
            ARGUMENT(_NUM)
        FLAG(-name)
            FLAG(-mindepth)
                ARGUMENT(_NUM)

Example 321 (1)
Original English: Find all directories under ~/code without descending into hidden directories and print them appended with : (colon)
English: find all directory under _UNK without descending into hidden directory and print appended with ( colon )
Original Command: find ~/code -name '.*' -prune -o -type d -printf ':%p'

Ground truth: find ~/code \( -name '.*' -prune -or -type d \) -printf ':%p'
Prediction: find UNK -type d
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(d)

Example 322 (1)
Original English: Find all files begging with a specific string.
English: find all file _UNK with specific string
Original Command: find . -name 'mystring*'

Ground truth: find . -name 'mystring*'
Prediction: find . -name '*.rb'
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT('*.rb')

Example 323 (1)
Original English: find all files under the current folder except dir1 dir2 dir3  folder
English: find all file under current folder except "dir_NUM" "dir_NUM" "dir_NUM" folder
Original Command: find . -type d \( -path dir1 -o -path dir2 -o -path dir3 \) -prune -o -print

Ground truth: find . -type d \( -path dir_NUM -or -path dir_NUM -or -path dir_NUM \) \( -prune -or -print \)
Prediction: find . -iname file_name
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-iname)
            ARGUMENT(file_name)

Example 324 (2)
Original English: change the ownership of all the files in the file system from edwarda to earnestc
English: change ownership of all file in file system from _UNK to _UNK
Original Command: find / -user edwarda -exec chown earnestc "{}" \;

Ground truth: find / -user edwarda -exec chown earnestc "{}" ;
Prediction: find / -user myuser:a-common-group-name
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-user)
            ARGUMENT(myuser:a-common-group-name)

Example 325 (2)
Original English: List all regular files under the current directory and below it
English: list all regular file under current directory and below
Original Command: find . -type f -print0 | xargs -0 ls -l

Ground truth: find . -type f -print0 | xargs -0 ls -l
Prediction: find . -type f -ls
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-ls)

Quotation Error: space inside word '/re/ {print;exit}'
Quotation Error: space inside word '/re/ {print;exit}'
Example 326 (2)
Original English: Search for first match of the regex 're' in all *.coffee files under current directory
English: search for first match of regex _UNK in all "*.coffee" file under current directory
Original Command: find . -name '*.coffee' -exec awk '/re/ {print;exit}' {} \;

Ground truth: find . -name '*.coffee' -exec awk _LONG_PATTERN {} ;
Prediction: find . -name '*.rb' -type f | xargs grep -l -i {}
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-name)
                ARGUMENT('*.rb')
            FLAG(-type)
                ARGUMENT(f)
        HEADCOMMAND(xargs)
            HEADCOMMAND(grep)
                FLAG(-l)
                FLAG(-i)
                ARGUMENT({})

Example 327 (1)
Original English: find all the files in a folder which have been modified from the start of the day
English: find all file in folder modified from start of day
Original Command: find /tmp/test/* -daystart -mtime -0

Ground truth: find /tmp/test/* -daystart -mtime -_NUM
Prediction: find /tmp/test/* -daystart -daystart -mtime _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/tmp/test/*)
        FLAG(-daystart)
        FLAG(-daystart)
        FLAG(-mtime)
            ARGUMENT(_NUM)

Example 328 (1)
Original English: search files  in the file system excluding those in the paths "10_Recommended" and "/export/repo"
English: search file in file system excluding in path _UNK and _UNK
Original Command: find / -name whatever -not -path "/10_Recommended*" -not -path "/export/repo/*"

Ground truth: find / -name whatever -not -path "/_NUM_Recommended*" -not -path "/export/repo/*"
Prediction: find / -wholename "*target*" -wholename "*target*" -wholename UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-wholename)
            ARGUMENT("*target*")
        FLAG(-wholename)
            ARGUMENT("*target*")
        FLAG(-wholename)
            ARGUMENT(UNK)

Example 329 (1)
Original English: find all the pdf files in the current directory and display only the directory name in which the pdf file is present
English: find all pdf file in current directory and display only directory name in pdf file present
Original Command: find . -type f -name '*.pdf' |sed 's#\(.*\)/.*#\1#' |sort -u

Ground truth: find . -type f -name '*.pdf' | sed 's#\(.*\)/.*#\_NUM#' | sort -u
Prediction: find . -name *.pdf
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(*.pdf)

Example 330 (1)
Original English: Search the current directory and two levels below for file `teste.tex'
English: search current directory and "_NUM" level below for file _UNK
Original Command: find ~/ -maxdepth 3 -name teste.tex

Ground truth: find ~/ -maxdepth _NUM -name teste.tex
Prediction: find -mindepth _NUM -name document
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-mindepth)
            ARGUMENT(_NUM)
        FLAG(-name)
            ARGUMENT(document)

Example 331 (1)
Original English: search for all the files in current folder which start with "file2015-0" and move them to frst 400 fiiles  to another folder
English: search for all file in current folder start with "file_NUM-_NUM" and move to _UNK "_NUM" _UNK to another folder
Original Command: find . -name "file2015-0*" | head -400 | xargs -I filename mv  filename

Ground truth: find . -name "file_NUM-_NUM*" | head -_NUM | xargs -I filename mv filename
Prediction: find . -name "file_NUM-_NUM*" -exec mv {} . ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT("file_NUM-_NUM*")
        FLAG(-exec::;)
            HEADCOMMAND(mv)
                ARGUMENT({})
                ARGUMENT(.)

Example 332 (1)
Original English: Print the sizes of all files from the current directory tree
English: print size of all file from current directory tree
Original Command: find . -iname '*.jpg' -type f -printf +%b

Ground truth: find . -iname '*.jpg' -type f -printf +%b
Prediction: find . | xargs ls -l
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
        HEADCOMMAND(xargs)
            HEADCOMMAND(ls)
                FLAG(-l)

rf splitted into: -r -f 
Error: -rf is not a flag of rm
Example 333 (1)
Original English: Find all files larger than 100M and delete them
English: find all file larger than "_NUMM" and delete
Original Command: find / -size +100M -exec rm -rf {} \;

Ground truth: find / -size +_NUMM -exec rm -r -f {} ;
Prediction: find / -type f -size +_NUMM -delete
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-size)
            ARGUMENT(+_NUMM)
        FLAG(-delete)

Quotation Error: space inside word '*.pl| *.pm'
Example 334 (1)
Original English: show all files in /usr/tom and display only files ending with ".pl" or ".pm"
English: show all file in _UNK and display only file ending with ".pl" or ".pm"
Original Command: find /usr/tom | egrep '*.pl| *.pm'

Ground truth: find /usr/tom | egrep _LONG_PATTERN
Prediction: find /etc \( -newer UNK -or -name CVS -or -name CVS \)
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/etc)
        BINARYLOGICOP(-or)
            FLAG(-newer)
                ARGUMENT(UNK)
            FLAG(-name)
                ARGUMENT(CVS)
            FLAG(-name)
                ARGUMENT(CVS)

Example 335 (1)
Original English: List all regular files under current directory (not white space sage)
English: list all regular file under current directory ( not white space _UNK )
Original Command: find . -type f -print | xargs -n 1

Ground truth: find . -type f -print | xargs -n _NUM
Prediction: find . -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)

Error: -newermt is not a flag of find
Example 336 (1)
Original English: Find all files/directories that are not newer than Jul 01 by modification time
English: find all "files/directories" not newer than _UNK "_NUM" by modification time
Original Command: find /file/path ! -newermt "Jul 01"

Ground truth: find /file/path ! -newermt _LONG_PATTERN
Prediction: find ! -newer UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        UNARYLOGICOP(!)
            FLAG(-newer)
                ARGUMENT(UNK)

Example 337 (2)
Original English: Find all *.m4a files/directories under /home/family/Music directory
English: find all _UNK "files/directories" under _UNK directory
Original Command: find /home/family/Music -name *.m4a -print0

Ground truth: find /home/family/Music -name *.m_NUMa -print0
Prediction: find UNK -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-name)
            ARGUMENT(UNK)

Example 338 (1)
Original English: Find files/directories under current directory that matches 'projects/insanewebproject' in their paths
English: find "files/directories" under current directory match _UNK in path
Original Command: find -ipath 'projects/insanewebproject'

Ground truth: find -ipath 'projects/insanewebproject'
Prediction: find . -wholename UNK | grep -q UNK
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-wholename)
                ARGUMENT(UNK)
        HEADCOMMAND(grep)
            FLAG(-q)
            ARGUMENT(UNK)

Example 339 (1)
Original English: List all regular files under current directory ensuring white space safety
English: list all regular file under current directory ensuring white space safety
Original Command: find . -type f -print0 | xargs -0 -n 1

Ground truth: find . -type f -print0 | xargs -0 -n _NUM
Prediction: find . -type f | xargs --null
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-type)
                ARGUMENT(f)
        HEADCOMMAND(xargs)
            FLAG(--null)

il splitted into: -i -l 
Error: -il is not a flag of grep
Quotation Error: space inside word '^Subject:.*unique subject'
il splitted into: -i -l 
Error: -il is not a flag of grep
Quotation Error: space inside word '^Subject:.*unique subject'
Example 340 (2)
Original English: List the files from the current directory tree that contain lines matching regular expression  '^Subject:.*unique subject'
English: list file from current directory tree contain line matching regular expression _LONG_PATTERN
Original Command: find . -type f -print0 | xargs -0 grep -il '^Subject:.*unique subject'

Ground truth: find . -type f -print0 | xargs -0 grep -i -l _LONG_PATTERN
Prediction: find . -regex UNK -exec egrep -n ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-regex)
            ARGUMENT(UNK)
        FLAG(-exec::;)
            HEADCOMMAND(egrep)
                FLAG(-n)

Example 341 (1)
Original English: Delete all MP3 files under /tmp
English: delete all "MP_NUM" file under "/tmp"
Original Command: find /tmp -iname '*.mp3' -print0 | xargs -0 rm

Ground truth: find /tmp -iname '*.mp_NUM' -print0 | xargs -0 rm
Prediction: find /tmp -name '.*' -delete
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/tmp)
        FLAG(-name)
            ARGUMENT('.*')
        FLAG(-delete)

rn splitted into: -r -n 
Error: -rn is not a flag of sort
Example 342 (1)
Original English: Find and the 5 largest regular files in the Downloads folder of tecmint's home directory and output the file sizes in bytes.
English: find and "_NUM" largest regular file in _UNK folder of _UNK home directory and output file size in byte
Original Command: find /home/tecmint/Downloads/ -type f -printf "%s %p\n" | sort -rn | head -n 5

Ground truth: find /home/tecmint/Downloads/ -type f -printf _LONG_PATTERN | sort -r -n | head -n _NUM
Prediction: find UNK -type f | sort
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(UNK)
            FLAG(-type)
                ARGUMENT(f)
        HEADCOMMAND(sort)

Example 343 (1)
Original English: Find all files under /home that belong to user tecmint
English: find all file under "/home" belong to user tecmint
Original Command: find /home -user tecmint

Ground truth: find /home -user tecmint
Prediction: find /home/ -user joe
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/home/)
        FLAG(-user)
            ARGUMENT(joe)

Example 344 (1)
Original English: Change permissions for all PHP files under the current directory tree to 755
English: change permission for all PHP file under current directory tree to "_NUM"
Original Command: find . -name "*.php" -exec chmod 755 {} \;

Ground truth: find . -name "*.php" -exec chmod _NUM {} ;
Prediction: find . -type f -name *.php -exec chmod _NUM {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-name)
            ARGUMENT(*.php)
        FLAG(-exec::;)
            HEADCOMMAND(chmod)
                ARGUMENT(_NUM)
                ARGUMENT({})

Example 345 (1)
Original English: show all regular/normal the files in the current folder whose size is bigger than 0 bytes excluding everything
English: show all "regular/normal" file in current folder whose size bigger than "_NUM" byte excluding everything
Original Command: find * -prune -type f -size +0c -print

Ground truth: find * -prune -type f -size +_NUMc -print
Prediction: find . -type f -size _NUM -not -empty
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-size)
            ARGUMENT(_NUM)
        UNARYLOGICOP(-not)
            FLAG(-empty)

Example 346 (1)
Original English: find all files in the file system whose size is exactly 2KB
English: find all file in file system whose size exactly "_NUMKB"
Original Command: find / -size 2048c

Ground truth: find / -size _NUMc
Prediction: find / -size _NUMk
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-size)
            ARGUMENT(_NUMk)

Example 347 (1)
Original English: List all *fink* files/directories in entire file system
English: list all "*fink*" "files/directories" in entire file system
Original Command: find / \( -type f -or -type d \) -name \*fink\* -ls

Ground truth: find / \( -type f -or -type d \) -name *fink* -ls
Prediction: find / -newer UNK -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-newer)
            ARGUMENT(UNK)
        FLAG(-print)

Example 348 (1)
Original English: find all the hidden files in the temp folder
English: find all hidden file in temp folder
Original Command: find /tmp -type f -name ".*"

Ground truth: find /tmp -type f -name ".*"
Prediction: find /tmp/* -name ".*"
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/tmp/*)
        FLAG(-name)
            ARGUMENT(".*")

dn splitted into: -d -n 
Error: -dn is not a flag of xargs
Example 349 (1)
Original English: Find all files/directories under current directory and print them with newline as the delimiter
English: find all "files/directories" under current directory and print with newline delimiter
Original Command: find -print | xargs -d'\n'

Ground truth: find -print | xargs -d'\n' -d'\n'
Prediction: find -print0
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-print0)

Example 350 (1)
Original English: Find all files that were accessed in the last 50 days.
English: find all file accessed in last "_NUM" day
Original Command: find / -atime 50

Ground truth: find / -atime _NUM
Prediction: find . -amin -_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-amin)
            ARGUMENT(-_NUM)

lrt splitted into: -l -r -t 
Error: -lrt is not a flag of ls
F  splitted into: -F -  
Error: -F  is not a flag of awk
Quotation Error: space inside word '{print $1  $9}'
Example 351 (1)
Original English: Find only permission field & file name from long listing with find command .
English: find only permission field "&" file name from long listing with find command
Original Command: find -type f -iname "*.txt" -exec ls -lrt {} \;|awk -F' ' '{print $1  $9}'

Ground truth: find -type f -iname "*.txt" -exec ls -l -r -t {} ; | awk -F' ' -F' ' _LONG_PATTERN
Prediction: find . -type f -name "*.txt"
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-name)
            ARGUMENT("*.txt")

Example 352 (1)
Original English: find all the text files present in the current directory excluding the search in certain paths.
English: find all text file present in current directory excluding search in certain path
Original Command: find . -type f -name "*.txt" ! -path "./Movies/*" ! -path "./Downloads/*" ! -path "./Music/*"

Ground truth: find . -type f -name "*.txt" ! -path "./Movies/*" ! -path "./Downloads/*" ! -path "./Music/*"
Prediction: find . -wholename "./Downloads/*" ! -wholename "./Downloads/*"
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-wholename)
            ARGUMENT("./Downloads/*")
        UNARYLOGICOP(!)
            FLAG(-wholename)
                ARGUMENT("./Downloads/*")

Example 353 (1)
Original English: Find find symlinks pointing to /mnt/oldname* in the entire file system
English: find find symlinks pointing to _UNK in entire file system
Original Command: find / -type l -lname '/mnt/oldname*'

Ground truth: find / -type l -lname '/mnt/oldname*'
Prediction: find / -type l
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-type)
            ARGUMENT(l)

Example 354 (1)
Original English: find all the files in the current folder which do not belong to any user
English: find all file in current folder not belong to any user
Original Command: find . -nouser -ls

Ground truth: find . -nouser -ls
Prediction: find . -nouser
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-nouser)

Example 355 (1)
Original English: list regular file which file name end with '*.c' or '*.sh' in current directory
English: list regular file file name end with "*.c" or "*.sh" in current directory
Original Command: find . -type f \( -name "*.c" -o -name "*.sh" \)

Ground truth: find . -type f \( -name "*.c" -or -name "*.sh" \)
Prediction: find . -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        BINARYLOGICOP(-or)
            FLAG(-name)
                ARGUMENT(UNK)

Example 356 (1)
Original English: list *.bmp and *.txt files under the /home/user/Desktop directory.
English: list _UNK and "*.txt" file under "/home/user/Desktop" directory
Original Command: find /home/user/Desktop -name '*.bmp' -o -name '*.txt'

Ground truth: find /home/user/Desktop \( -name '*.bmp' -or -name '*.txt' \)
Prediction: find /home/user/Desktop -name *.txt
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/home/user/Desktop)
        FLAG(-name)
            ARGUMENT(*.txt)

Example 357 (1)
Original English: Find all files whose names contain the string 'xpilot' which exist within '/usr/local/games'
English: find all file whose name contain string _UNK exist within _UNK
Original Command: find /usr/local/games -name "*xpilot*"

Ground truth: find /usr/local/games -name "*xpilot*"
Prediction: find . -name '*.rb'
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT('*.rb')

Example 358 (1)
Original English: Search for regular files of the grooup 'users' in the file system
English: search for regular file of _UNK _UNK in file system
Original Command: find /  -type f -group users

Ground truth: find / -type f -group users
Prediction: find / -type f -exec grep -H {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-exec::;)
            HEADCOMMAND(grep)
                FLAG(-H)
                ARGUMENT({})

Example 359 (1)
Original English: List files that contain between 1,000 and 10,000 characters
English: list file contain between "_NUM" "_NUM" and "_NUM" "_NUM" character
Original Command: find . -size +1000c -size -10000c -print

Ground truth: find . -size +_NUMc -size -_NUMc -print
Prediction: find . -size UNK -type f -size UNK -exec ls -l {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-size)
            ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-size)
            ARGUMENT(UNK)
        FLAG(-exec::;)
            HEADCOMMAND(ls)
                FLAG(-l)
                ARGUMENT({})

Example 360 (1)
Original English: Find recursively the files named "file" in the current directory ignoring the .git subdirectory
English: find recursively file named "file" in current directory ignoring ".git" subdirectory
Original Command: find . -path ./.git  -prune -o -name file  -print

Ground truth: find . \( -path ./.git -prune -or -name file \) -print
Prediction: find . \( -name file -prune -or -name file -prune \)
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        BINARYLOGICOP(-or)
            UNARYLOGICOP(-prune)
                FLAG(-name)
                    ARGUMENT(file)
            UNARYLOGICOP(-prune)
                FLAG(-name)
                    ARGUMENT(file)

Example 361 (1)
Original English: Search the current directory tree for files last accessed more than 10 days ago
English: search current directory tree for file last accessed more than "_NUM" day ago
Original Command: find . -atime +10

Ground truth: find . -atime +_NUM
Prediction: find ~/ -atime +_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(~/)
        FLAG(-atime)
            ARGUMENT(+_NUM)

r0 splitted into: -r -0 
Error: -r0 is not a flag of xargs
Example 362 (1)
Original English: Find all *.log files under path/ that do not contain "string that should not occur"
English: find all "*.log" file under _UNK not contain _LONG_PATTERN
Original Command: find path/ -name '*.log' -print0 | xargs -r0 grep -L "string that should not occur"

Ground truth: find path/ -name '*.log' -print0 | xargs -r -0 grep -L _LONG_PATTERN
Prediction: find UNK -name "*.log"
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-name)
            ARGUMENT("*.log")

Warning: -exec missing ending ';'
Example 363 (1)
Original English: Find a file by an inode number and rename it.
English: find file by inode number and rename
Original Command: find -inum 16187430 -exec mv {} new-test-file-name \

Ground truth: find -inum _NUM -exec mv {} new-test-file-name \;
Prediction: find -inum _NUM -inum _NUM -exec rm {} \;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-inum)
            ARGUMENT(_NUM)
        FLAG(-inum)
            ARGUMENT(_NUM)
        FLAG(-exec::\;)
            HEADCOMMAND(rm)
                ARGUMENT({})

Example 364 (1)
Original English: Find all hidden regular files under /tmp and below
English: find all hidden regular file under "/tmp" and below
Original Command: find /tmp -type f -name ".*"

Ground truth: find /tmp -type f -name ".*"
Prediction: find /tmp -type f -name ".*"
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/tmp)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-name)
            ARGUMENT(".*")

Example 365 (3)
Original English: search for files which are writable by either their owner or their group
English: search for file writable by either owner or group
Original Command: find . -perm /u+w,g+w

Ground truth: find . -perm /u+w,g+w
Prediction: find . \( -newer UNK -or -perm -_NUM \)
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        BINARYLOGICOP(-or)
            FLAG(-newer)
                ARGUMENT(UNK)
            FLAG(-perm)
                ARGUMENT(-_NUM)

Example 366 (1)
Original English: Remove all files in and below the current directory whose names begin with "not"
English: remove all file in and below current directory whose name begin with _UNK
Original Command: find . -name not\* -print0 | xargs -0 rm

Ground truth: find . -name not* -print0 | xargs -0 rm
Prediction: find . -name UNK -exec rm {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT({})

F/ splitted into: -F -/ 
Error: -F/ is not a flag of awk
Quotation Error: space inside word '{ print $2 }'
Example 367 (1)
Original English: Find all files/directories under current directory and print only 2nd field from output delimited by '/'
English: find all "files/directories" under current directory and print only "_NUMnd" field from output _UNK by "/"
Original Command: find . | awk -F"/" '{ print $2 }'

Ground truth: find . | awk -F"/" -F"/" _LONG_PATTERN
Prediction: find .
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)

Example 368 (1)
Original English: find all the directories in current folder and do not search in sub directories
English: find all directory in current folder and not search in sub directory
Original Command: find . -maxdepth 1 -type d -print0

Ground truth: find . -maxdepth _NUM -type d -print0
Prediction: find -maxdepth _NUM -type d
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-maxdepth)
            ARGUMENT(_NUM)
        FLAG(-type)
            ARGUMENT(d)

Error: -i is not a flag of xargs
Example 369 (1)
Original English: delete all the files in the current folder which have been modified in the last 14*24 hours
English: delete all file in current folder modified in last "_NUM*_NUM" hour
Original Command: find . -mtime -14 -print|xargs -i rm \;

Ground truth: find . -mtime -_NUM -print | xargs -i rm ;
Prediction: find . -mtime -_NUM -exec rm {} \;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-mtime)
            ARGUMENT(-_NUM)
        FLAG(-exec::\;)
            HEADCOMMAND(rm)
                ARGUMENT({})

Example 370 (1)
Original English: find a file in several folders
English: find file in several folder
Original Command: find ./dir1 ./dir2 -name foo.bar -print

Ground truth: find ./dir_NUM ./dir_NUM -name foo.bar -print
Prediction: find /usr -perm -_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/usr)
        FLAG(-perm)
            ARGUMENT(-_NUM)

Iw splitted into: -I -w 
Error: -Iw is not a flag of grep
Example 371 (1)
Original English: Search the current directory for files whose names start with "messages." ignoring SVN files
English: search current directory for file whose name start with "messages." ignoring SVN file
Original Command: find \( -name 'messages.*' ! -path "*/.svn/*" \) -exec grep -Iw uint {} +

Ground truth: find \( -name 'messages.*' -and ! -path "*/.svn/*" \) -exec grep -I -w uint {} +
Prediction: find . -iname '*.txt' -exec rm ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-iname)
            ARGUMENT('*.txt')
        FLAG(-exec::;)
            HEADCOMMAND(rm)

fr splitted into: -f -r 
Error: -fr is not a flag of rm
rf splitted into: -r -f 
Error: -rf is not a flag of rm
rf splitted into: -r -f 
Error: -rf is not a flag of rm
rf splitted into: -r -f 
Error: -rf is not a flag of rm
fr splitted into: -f -r 
Error: -fr is not a flag of rm
rf splitted into: -r -f 
Error: -rf is not a flag of rm
Example 372 (8)
Original English: Delete all .svn files/directories under current directory
English: delete all ".svn" "files/directories" under current directory
Original Command: find . -name .svn -exec rm -v {} \;

Ground truth: find . -name .svn -exec rm -v {} ;
Prediction: find . -name .svn -delete
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(.svn)
        FLAG(-delete)

Example 373 (1)
Original English: Delete all files in the current directory.
English: delete all file in current directory
Original Command: find . -exec /bin/rm {} \;

Ground truth: find . -exec rm {} ;
Prediction: find . -delete
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-delete)

Example 374 (1)
Original English: List all files that are between 10000 and 32000 bytes in size
English: list all file between "_NUM" and "_NUM" byte in size
Original Command: find . -size +10000c -size -32000c -print

Ground truth: find . -size +_NUMc -size -_NUMc -print
Prediction: find /mydir_NUM -size +_NUM -type f -empty
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/mydir_NUM)
        FLAG(-size)
            ARGUMENT(+_NUM)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-empty)

Example 375 (1)
Original English: Search the .sh files in the current directory tree for string "ksh"
English: search ".sh" file in current directory tree for string _UNK
Original Command: find . -name "*.sh" | xargs grep "ksh"

Ground truth: find . -name "*.sh" | xargs grep "ksh"
Prediction: find . -name "*.sh" | xargs rm UNK
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-name)
                ARGUMENT("*.sh")
        HEADCOMMAND(xargs)
            HEADCOMMAND(rm)
                ARGUMENT(UNK)

Example 376 (1)
Original English: Find directories that are directly under $workspace_ts directory (no-subdirectories) and were modified more than 30 days ago
English: find directory directly under _UNK directory ( no-subdirectories ) and modified more than "_NUM" day ago
Original Command: find $workspace_ts -mindepth 1 -maxdepth 1 -type d -mtime +30 -print

Ground truth: find $workspace_ts -mindepth _NUM -maxdepth _NUM -type d -mtime +_NUM -print
Prediction: find -mindepth _NUM -mindepth _NUM -maxdepth _NUM -type d -mtime _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-mindepth)
            ARGUMENT(_NUM)
        FLAG(-mindepth)
            ARGUMENT(_NUM)
        FLAG(-maxdepth)
            ARGUMENT(_NUM)
        FLAG(-type)
            ARGUMENT(d)
        FLAG(-mtime)
            ARGUMENT(_NUM)

Example 377 (2)
Original English: find all files in a folder that have a specific word in their name
English: find all file in folder specific word in name
Original Command: find /usr/local/games -name "*xpilot*"

Ground truth: find /usr/local/games -name "*xpilot*"
Prediction: find /usr/local -name "*blast*"
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/usr/local)
        FLAG(-name)
            ARGUMENT("*blast*")

Example 378 (1)
Original English: find all the files similar to top which have been modified after a file is modified
English: find all file _UNK to top modified after file modified
Original Command: find ~ -name 'top*' -newer /etc/motd

Ground truth: find ~ -name 'top*' -newer /etc/motd
Prediction: find -newer /etc/motd
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-newer)
            ARGUMENT(/etc/motd)

Example 379 (1)
Original English: Find files/directories under /users/tom that matches both the pattern "*.pl" and  "*.pm"
English: find "files/directories" under "/users/tom" match both pattern "*.pl" and _UNK
Original Command: find /users/tom -name "*.pl" -name "*.pm"

Ground truth: find /users/tom -name "*.pl" -name "*.pm"
Prediction: find /users/tom -name '*.p[lm]'
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/users/tom)
        FLAG(-name)
            ARGUMENT('*.p[lm]')

Example 380 (2)
Original English: search for files that are readable for everybody, have at least on write bit set but are not executable for anybody
English: search for file readable for _UNK at least on write bit set but not executable for _UNK
Original Command: find . -perm -444 -perm /222 ! -perm /111

Ground truth: find . -perm -_NUM -perm /_NUM ! -perm /_NUM
Prediction: find / -perm -_NUM -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-perm)
            ARGUMENT(-_NUM)
        FLAG(-print)

Example 381 (1)
Original English: Find all files name passwd in the root directory and all its sub-directories.
English: find all file name passwd in root directory and all sub-directories
Original Command: find / -name passwd

Ground truth: find / -name passwd
Prediction: find / -name foo
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-name)
            ARGUMENT(foo)

Example 382 (1)
Original English: Search for "YOURSTRING" in all files under current directory
English: search for _UNK in all file under current directory
Original Command: grep YOURSTRING `find .`

Ground truth: grep YOURSTRING $( find . )
Prediction: find . -type f -print | xargs grep "text"
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-type)
                ARGUMENT(f)
            FLAG(-print)
        HEADCOMMAND(xargs)
            HEADCOMMAND(grep)
                ARGUMENT("text")

Example 383 (1)
Original English: display all the directories in the current folder which are atleast one level deep
English: display all directory in current folder atleast "_NUM" level deep
Original Command: find . -mindepth 1 -type d -print0

Ground truth: find . -mindepth _NUM -type d -print0
Prediction: find -mindepth _NUM -mindepth _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-mindepth)
            ARGUMENT(_NUM)
        FLAG(-mindepth)
            ARGUMENT(_NUM)

Example 384 (1)
Original English: Find all regular files that reside in the current directory tree and were last modified more than 4 days ago
English: find all regular file reside in current directory tree and last modified more than "_NUM" day ago
Original Command: find . -type f -mtime +4

Ground truth: find . -type f -mtime +_NUM
Prediction: find . -type f -mtime +_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-mtime)
            ARGUMENT(+_NUM)

Example 385 (1)
Original English: Search the /tmp/ directory recursively for files matching regular expression ".*file[0-9]+$"
English: search "/tmp/" directory recursively for file matching regular expression _UNK
Original Command: find /tmp -regex ".*file[0-9]+$"

Ground truth: find /tmp -regex ".*file[_NUM-_NUM]+$"
Prediction: find /tmp -regex UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/tmp)
        FLAG(-regex)
            ARGUMENT(UNK)

Example 386 (1)
Original English: find all the text files in current folder and move all these to another folder appending ".bar" at the end of these files
English: find all text file in current folder and move all to another folder appending ".bar" at end of file
Original Command: find . -name "*.txt" | xargs -I '{}' mv '{}' /foo/'{}'.bar

Ground truth: find . -name "*.txt" | xargs -I '{}' mv '{}' /foo/{}.bar
Prediction: find . -name "*.txt" -type f -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT("*.txt")
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-print)

Example 387 (1)
Original English: renames all ".htm" files to ".html" files
English: _UNK all _UNK file to ".html" file
Original Command: find . -name "*.htm" -exec mv '{}' '{}l' \;

Ground truth: find . -name "*.htm" -exec mv '{}' '{}l' ;
Prediction: find . -name "*.html"
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT("*.html")

Example 388 (1)
Original English: Find all files under /somefolder matching the extended regex '\./(.*\.error.*|second.*log|.*FFPC\.log)$' in their paths
English: find all file under "/somefolder" matching extended regex _LONG_PATTERN in path
Original Command: find -E /somefolder -type f -regex '\./(.*\.error.*|second.*log|.*FFPC\.log)$'

Ground truth: find -E /somefolder -type f -regex '\./(.*\.error.*|second.*log|.*FFPC\.log)$'
Prediction: find /somefolder /somefolder -regex UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/somefolder)
        ARGUMENT(/somefolder)
        FLAG(-regex)
            ARGUMENT(UNK)

Example 389 (1)
Original English: find all files in the current folder which have been modified in the last 24 hours and whose file name is of length 1
English: find all file in current folder modified in last "_NUM" hour and whose file name of length "_NUM"
Original Command: find . -name \? -mtime -1

Ground truth: find . -name ? -mtime -_NUM
Prediction: find . -name ? -exec rm {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(?)
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT({})

Quotation Error: space inside word 'Name: %16f Size: %6s\n'
Example 390 (1)
Original English: display the filenames which do not have begin with dot (.)
English: display filename not begin with dot ( )
Original Command: find . -maxdepth 1 -name '[!.]*' -printf 'Name: %16f Size: %6s\n'

Ground truth: find . -maxdepth _NUM -name '[!.]*' -printf _LONG_PATTERN
Prediction: find . -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)

Example 391 (1)
Original English: Delete all files in the /myDir directory tree that were last modfied more than 7 days ago
English: delete all file in "/myDir" directory tree last modfied more than "_NUM" day ago
Original Command: find /myDir -mindepth 1 -mtime +7 -delete

Ground truth: find /myDir -mindepth _NUM -mtime +_NUM -delete
Prediction: find /myDir -mindepth _NUM -mtime _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/myDir)
        FLAG(-mindepth)
            ARGUMENT(_NUM)
        FLAG(-mtime)
            ARGUMENT(_NUM)

Example 392 (1)
Original English: Find all regular files that reside in the current directory tree and were last modified at least 1 day ago
English: find all regular file reside in current directory tree and last modified at least "_NUM" day ago
Original Command: find . -type f -mtime +0

Ground truth: find . -type f -mtime +_NUM
Prediction: find . -type f -mtime _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-mtime)
            ARGUMENT(_NUM)

Example 393 (1)
Original English: Perform case-insensitive search for file `TeSt123.txt' on the system
English: perform case-insensitive search for file _UNK on system
Original Command: find / -iname TeSt123.txt

Ground truth: find / -iname TeSt_NUM.txt
Prediction: find / -iname UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-iname)
            ARGUMENT(UNK)

Example 394 (1)
Original English: search for a word in the current directory in all files ending with specific word
English: search for word in current directory in all file ending with specific word
Original Command: find . -name '*.[ch]' | xargs grep -E 'expr'

Ground truth: find . -name '*.[ch]' | xargs grep -E 'expr'
Prediction: find . -name '*.rb' -exec grep -H '{}' ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT('*.rb')
        FLAG(-exec::;)
            HEADCOMMAND(grep)
                FLAG(-H)
                ARGUMENT('{}')

Example 395 (2)
Original English: Count the *.html files residing in the /usr/src directory tree and containing string "foo"
English: count "*.html" file residing in "/usr/src" directory tree and containing string "foo"
Original Command: find /usr/src -name "*.html" | xargs grep -l foo | wc -l

Ground truth: find /usr/src -name "*.html" | xargs grep -l foo | wc -l
Prediction: find '{}' | xargs -0 rm
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT('{}')
        HEADCOMMAND(xargs)
            FLAG(-0)
            HEADCOMMAND(rm)

Example 396 (1)
Original English: find all the php files that belong to a specific user that have been modified in the last 1 day
English: find all php file belong to specific user modified in last "_NUM" day
Original Command: find -user takuya -name '*.php' -daystart -mtime -1

Ground truth: find -user takuya -name '*.php' -daystart -mtime -_NUM
Prediction: find . -user UNK -type f -mtime -_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-user)
            ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-mtime)
            ARGUMENT(-_NUM)

Example 397 (1)
Original English: display all directories in a folder
English: display all directory in folder
Original Command: find /etc -type d -print

Ground truth: find /etc -type d -print
Prediction: find UNK -type d
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(d)

Example 398 (1)
Original English: find all text files in a folder and display the number of lines in these files
English: find all text file in folder and display number of line in file
Original Command: find /home/my_dir -name '*.txt' | xargs grep -c ^.*

Ground truth: find /home/my_dir -name '*.txt' | xargs grep -c ^.*
Prediction: find /home/calvin/ -name "*.txt"
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/home/calvin/)
        FLAG(-name)
            ARGUMENT("*.txt")

Example 399 (1)
Original English: Find *.java files in the current directory and replace foo with bar in those files
English: find "*.java" file in current directory and replace foo with bar in file
Original Command: find . -name "*.java" -exec sed -i '' s/foo/bar/g \;

Ground truth: find . -name "*.java" -exec sed -i '' s/foo/bar/g ;
Prediction: find . -name "*.java" -exec sed -i UNK {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT("*.java")
        FLAG(-exec::;)
            HEADCOMMAND(sed)
                FLAG(-i)
                    ARGUMENT(UNK)
                ARGUMENT({})

Quotation Error: space inside word 'END { print $1/(NR-1) }'
Example 400 (1)
Original English: Compute the mean average of the word count of *.txt files in the home directory
English: _UNK _UNK _UNK of word count of "*.txt" file in home directory
Original Command: find ~/ -name '*.txt' -print0 | xargs -0 wc -w | awk 'END { print $1/(NR-1) }'

Ground truth: find ~/ -name '*.txt' -print0 | xargs -0 wc -w | awk _LONG_PATTERN
Prediction: find -a -w -name '*.txt' | wc -l
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            FLAG(-a)
            FLAG(-w)
            FLAG(-name)
                ARGUMENT('*.txt')
        HEADCOMMAND(wc)
            FLAG(-l)

Example 401 (1)
Original English: Search for files which are writable by somebody
English: search for file writable by _UNK
Original Command: find . -perm /222

Ground truth: find . -perm /_NUM
Prediction: find . -perm +_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-perm)
            ARGUMENT(+_NUM)

Quotation Error: space inside word '*.pl| *.pm'
Example 402 (1)
Original English: Find all files/directories under /usr/tom which matches the extended regex '*.pl| *.pm'  in their names
English: find all "files/directories" under _UNK match extended regex _LONG_PATTERN in name
Original Command: find /usr/tom | egrep '*.pl| *.pm'

Ground truth: find /usr/tom | egrep _LONG_PATTERN
Prediction: find UNK -regex UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-regex)
            ARGUMENT(UNK)

Example 403 (1)
Original English: Find all regular files that reside in the current directory tree and were last modified more than 1 day ago
English: find all regular file reside in current directory tree and last modified more than "_NUM" day ago
Original Command: find . -type f -mtime +1

Ground truth: find . -type f -mtime +_NUM
Prediction: find . -type f -mtime +_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-mtime)
            ARGUMENT(+_NUM)

Example 404 (1)
Original English: find .bmp or .txt files
English: find _UNK or ".txt" file
Original Command: find /home/user/Desktop -name '*.bmp' -o -name '*.txt'

Ground truth: find /home/user/Desktop \( -name '*.bmp' -or -name '*.txt' \)
Prediction: find . -name "*.txt"
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        BINARYLOGICOP(-or)
            FLAG(-name)
                ARGUMENT("*.txt")

Quotation Error: space inside word '*[+{;"\\=?~()<>&*|$ ]*'
Example 405 (1)
Original English: remove all the files in the present directory which have special characters in their name and do not search in the sub directories of the current folder.
English: remove all file in present directory _UNK character in name and not search in sub directory of current folder
Original Command: find . -name '*[+{;"\\=?~()<>&*|$ ]*' -maxdepth 0 -exec rm -f '{}' \;

Ground truth: find . -name _LONG_PATTERN -maxdepth _NUM -exec rm -f '{}' ;
Prediction: find -maxdepth _NUM -type d
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-maxdepth)
            ARGUMENT(_NUM)
        FLAG(-type)
            ARGUMENT(d)

Quotation Error: space inside word 's/.*/& &/'
Example 406 (1)
Original English: display all the files in current directory with each file name displayed twice in the same row
English: display all file in current directory with each file name _UNK _UNK in same _UNK
Original Command: find . | sed 's/.*/& &/'

Ground truth: find . | sed _LONG_PATTERN
Prediction: find . -wholename UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-wholename)
            ARGUMENT(UNK)

Example 407 (1)
Original English: search through only the /usr and /home directories for any file named Chapter1.txt
English: search through only "/usr" and "/home" directory for any file named _UNK
Original Command: find /usr /home -name Chapter1.txt -type f

Ground truth: find /usr /home -name Chapter_NUM.txt -type f
Prediction: find /usr -name foo
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/usr)
        FLAG(-name)
            ARGUMENT(foo)

rf splitted into: -r -f 
Error: -rf is not a flag of rm
Example 408 (1)
Original English: Find all 100MB files in entire file system and delete them
English: find all "_NUMMB" file in entire file system and delete
Original Command: find / -size +100M -exec rm -rf {} \;

Ground truth: find / -size +_NUMM -exec rm -r -f {} ;
Prediction: find / -size _NUMM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-size)
            ARGUMENT(_NUMM)

Example 409 (1)
Original English: Find all files/directories under current directory that match the case insensitive extended regex .*/(EA|FS)_.*
English: find all "files/directories" under current directory match case insensitive extended regex _UNK _UNK ")_.*"
Original Command: find -E . -iregex '.*/(EA|FS)_.*'

Ground truth: find -E . -iregex '.*/(EA|FS)_.*'
Prediction: find . -iregex UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-iregex)
            ARGUMENT(UNK)

Example 410 (2)
Original English: Display all files in a folder
English: display all file in folder
Original Command: find man5 -print

Ground truth: find man_NUM -print
Prediction: find a
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(a)

Example 411 (1)
Original English: Delete files "*doc copoy" in directory tree /mnt/zip
English: delete file _LONG_PATTERN in directory tree "/mnt/zip"
Original Command: find /mnt/zip -name "*doc copy" -execdir rm "{}" \;

Ground truth: find /mnt/zip -name _LONG_PATTERN -execdir rm "{}" ;
Prediction: find _LONG_PATTERN -name _LONG_PATTERN
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(_LONG_PATTERN)
        FLAG(-name)
            ARGUMENT(_LONG_PATTERN)

Example 412 (1)
Original English: Find all build* directories under current directory and reverse sort them
English: find all _UNK directory under current directory and reverse sort
Original Command: find . -type d -name "build*" | sort -r

Ground truth: find . -type d -name "build*" | sort -r
Prediction: find -type d -depth -r -type d | sort -r
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            FLAG(-type)
                ARGUMENT(d)
            FLAG(-depth)
                FLAG(-r)
            FLAG(-type)
                ARGUMENT(d)
        HEADCOMMAND(sort)
            FLAG(-r)

Error: --target-directory=destDir is not a flag of mv
Error: -t is not a flag of mv
Example 413 (2)
Original English: Move all directories from the `sourceDir' directory tree to the `destDir' directory
English: move all directory from "sourceDir" directory tree to _UNK directory
Original Command: find sourceDir -mindepth 1 -type d  -print0 | xargs -0 mv --target-directory=destDir

Ground truth: find sourceDir -mindepth _NUM -type d -print0 | xargs -0 mv --target-directory=destDir
Prediction: find sourceDir -mindepth _NUM -name UNK -exec rm {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(sourceDir)
        FLAG(-mindepth)
            ARGUMENT(_NUM)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT({})

Example 414 (3)
Original English: List the current directory recursively ignoring the "dir1" subdirectory
English: list current directory recursively ignoring "dir_NUM" subdirectory
Original Command: find . -path ./dir1\*  -prune -o -print

Ground truth: find . \( -path ./dir_NUM* -prune -or -print \)
Prediction: find . -iname dir
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-iname)
            ARGUMENT(dir)

Warning: -exec missing ending ';'
Example 415 (1)
Original English: delete all the files in the current folder  which do not belong to any user
English: delete all file in current folder not belong to any user
Original Command: find / -nouser -exec rm {}\;

Ground truth: find / -nouser -exec rm {}; \;
Prediction: find . -nouser
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-nouser)

Warning: to_ast unrecognized argument attachment point UNARYLOGICOP_-not.
Example 416 (1)
Original English: To find all files except a specific pattern i.e. invert the search with -not or !.
English: to find all file except specific pattern "i.e" _UNK search with _UNK or _UNK
Original Command: find /dir/to/search/ -not -name "*.c" -print

Ground truth: find /dir/to/search/ -not -name "*.c" -print
Prediction: find . -not UNK -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        UNARYLOGICOP(-not)
            ARGUMENT(UNK)
        FLAG(-print)

Example 417 (1)
Original English: Delete all files/directories older than 48 hours in /path/to/files* paths
English: delete all "files/directories" older than "_NUM" hour in _UNK path
Original Command: find /path/to/files* -mtime +2 -delete

Ground truth: find /path/to/files* -mtime +_NUM -delete
Prediction: find -delete
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-delete)

Example 418 (1)
Original English: find all regular files exclude .o and exclude *.swp and output line number of soc_attach if it has
English: find all regular file exclude ".o" and exclude "*.swp" and output line number of _UNK if ha
Original Command: find .  \( ! -path "./output/*" \) -a \( -type f \) -a \( ! -name '*.o' \) -a \( ! -name '*.swp' \) | xargs grep -n soc_attach

Ground truth: find . \( ! -path "./output/*" -and -type f -and ! -name '*.o' -and ! -name '*.swp' \) | xargs grep -n soc_attach
Prediction: find . -type f -name UNK -exec rm {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT({})

Example 419 (1)
Original English: Count line numbers on files and record each count along with individual file name.
English: count line number on file and _UNK each count along with _UNK file name
Original Command: find /home/my_dir -name '*.txt' | xargs grep -c ^.*

Ground truth: find /home/my_dir -name '*.txt' | xargs grep -c ^.*
Prediction: find . -name UNK -type f -exec rm {} ; | awk UNK
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-name)
                ARGUMENT(UNK)
            FLAG(-type)
                ARGUMENT(f)
            FLAG(-exec::;)
                HEADCOMMAND(rm)
                    ARGUMENT({})
        HEADCOMMAND(awk)
            ARGUMENT(UNK)

rf splitted into: -r -f 
Error: -rf is not a flag of rm
Example 420 (1)
Original English: Search  all files & directoy from root directory which  are greater then 100M and delete them .
English: search all file "&" _UNK from root directory greater "_NUMM" and delete
Original Command: find /  -size +100M -exec rm -rf {} \;

Ground truth: find / -size +_NUMM -exec rm -r -f {} ;
Prediction: find / -user root -type f -delete
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-user)
            ARGUMENT(root)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-delete)

Example 421 (1)
Original English: Find all files/directories in entire file system for which owner has at least read/write permissions, or the group has at least read permission, or others have at least read permission
English: find all "files/directories" in entire file system for owner ha at least _UNK permission or group ha at least read permission or others at least read permission
Original Command: find / -perm /u+rw,g+r,o+r

Ground truth: find / -perm /u+rw,g+r,o+r
Prediction: find / -perm /_NUM -perm /_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-perm)
            ARGUMENT(/_NUM)
            FLAG(-perm)
                ARGUMENT(/_NUM)

m1 splitted into: -m -1 
Error: -m1 is not a flag of grep
Example 422 (1)
Original English: Search for first match of the case insensitive regex 're' in all *.coffee files under current directory
English: search for first match of case insensitive regex _UNK in all "*.coffee" file under current directory
Original Command: find . -name \*.coffee -exec grep -m1 -i 're' {} \;

Ground truth: find . -name *.coffee -exec grep -m -1 -i 're' {} ;
Prediction: find . -name '*.rb' -exec grep -i -H -i {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT('*.rb')
        FLAG(-exec::;)
            HEADCOMMAND(grep)
                FLAG(-i)
                FLAG(-H)
                FLAG(-i)
                ARGUMENT({})

Example 423 (1)
Original English: find all the files in the current folder that are modified after the modification date of a file
English: find all file in current folder modified after modification date of file
Original Command: find . -newer document -print

Ground truth: find . -newer document -print
Prediction: find . -newer /etc/motd
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-newer)
            ARGUMENT(/etc/motd)

Example 424 (3)
Original English: find all the png files in current folder which are present in the pattern list file "search.txt"
English: find all png file in current folder present in pattern list file _UNK
Original Command: find . -name '*.png' | grep -f <(sed s?^?/[0-9]_[0-9]_[0-9]_? search.txt)

Ground truth: find . -name '*.png' | grep -f <( sed s?^?/[_NUM-_NUM]_[_NUM-_NUM]_[_NUM-_NUM]_? search.txt )
Prediction: find . -name '*.png'
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT('*.png')

Example 425 (1)
Original English: find all the files which have been changed after the modification of a file.
English: find all file changed after modification of file
Original Command: find -cnewer /etc/fstab

Ground truth: find -cnewer /etc/fstab
Prediction: find / -newer /etc/motd
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-newer)
            ARGUMENT(/etc/motd)

Example 426 (1)
Original English: Search for all *.conf files in entire file system
English: search for all "*.conf" file in entire file system
Original Command: find / -type f -name "*.conf"

Ground truth: find / -type f -name "*.conf"
Prediction: find / -name "*.conf"
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-name)
            ARGUMENT("*.conf")

Example 427 (1)
Original English: Find recursively all files in a directory that contain a colon in the filename
English: find recursively all file in directory contain colon in filename
Original Command: find . -name \*\:\*

Ground truth: find . -name *:*
Prediction: find . -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)

Example 428 (1)
Original English: Remove all vmware-*.log files under current directory ensuring white space safety in filename
English: remove all _UNK file under current directory ensuring white space safety in filename
Original Command: find . -name vmware-*.log -print0 | xargs -0 rm

Ground truth: find . -name vmware-*.log -print0 | xargs -0 rm
Prediction: find . -name UNK -type f | xargs rm -f
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-name)
                ARGUMENT(UNK)
            FLAG(-type)
                ARGUMENT(f)
        HEADCOMMAND(xargs)
            HEADCOMMAND(rm)
                FLAG(-f)

Example 429 (1)
Original English: find all files in a folder which have not been modified in the last 366 days and delete them
English: find all file in folder not modified in last "_NUM" day and delete
Original Command: find $INTRANETDESTINATION/monthly -mtime +366 -exec rm {} \;

Ground truth: find $INTRANETDESTINATION/monthly -mtime +_NUM -exec rm {} ;
Prediction: find /tmp/test/* -daystart -type f -mtime +_NUM -exec rm {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/tmp/test/*)
        FLAG(-daystart)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-mtime)
            ARGUMENT(+_NUM)
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT({})

Example 430 (1)
Original English: Find all files with extension .aac in the /home directory tree
English: find all file with extension _UNK in "/home" directory tree
Original Command: find /home -type f -name '*.aac'

Ground truth: find /home -type f -name '*.aac'
Prediction: find /home -name '*.gz'
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/home)
        FLAG(-name)
            ARGUMENT('*.gz')

Example 431 (1)
Original English: Finding files which contain "some string" using find  and grep
English: finding file contain _LONG_PATTERN using find and grep
Original Command: find . -type f -print | xargs grep "some string"

Ground truth: find . -type f -print | xargs grep _LONG_PATTERN
Prediction: find . -regextype sed -regex UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-regextype)
        ARGUMENT(sed)
        FLAG(-regex)
            ARGUMENT(UNK)

Example 432 (1)
Original English: find all files having certain word in its name in the current folder
English: find all file having certain word in name in current folder
Original Command: find . -name "*bsd*" -print

Ground truth: find . -name "*bsd*" -print
Prediction: find . -name foo
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(foo)

Example 433 (1)
Original English: Forcefully delete all files in the current directory that begin with spam-
English: _UNK delete all file in current directory begin with _UNK
Original Command: find . -name 'spam-*' | xargs rm

Ground truth: find . -name 'spam-*' | xargs rm
Prediction: find . -name "*.bam" -delete
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT("*.bam")
        FLAG(-delete)

Example 434 (1)
Original English: delete all the mp4 files in the folder /home which are bigger than 10MB
English: delete all "mp_NUM" file in folder "/home" bigger than "_NUMMB"
Original Command: find /home -type f -name *.mp4 -size +10M -exec rm {} \;

Ground truth: find /home -type f -name *.mp_NUM -size +_NUMM -exec rm {} ;
Prediction: find /home -name '*.ogg' -type f -size +_NUMM -delete
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/home)
        FLAG(-name)
            ARGUMENT('*.ogg')
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-size)
            ARGUMENT(+_NUMM)
        FLAG(-delete)

Example 435 (1)
Original English: print the files in the current directory and two levels down to the current directory
English: print file in current directory and "_NUM" level down to current directory
Original Command: find -maxdepth 3 -name "sum.java"

Ground truth: find -maxdepth _NUM -name "sum.java"
Prediction: find -maxdepth _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-maxdepth)
            ARGUMENT(_NUM)

Example 436 (1)
Original English: find all files in the home folder which have been modified between 72 and 96 hours before
English: find all file in home folder modified between "_NUM" and "_NUM" hour before
Original Command: find ~ -mtime 2 -mtime -4 -daystart

Ground truth: find ~ -mtime _NUM -mtime -_NUM -daystart
Prediction: find $HOME -mtime +_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT($HOME)
        FLAG(-mtime)
            ARGUMENT(+_NUM)

Example 437 (1)
Original English: Search the current directory recursively for directories with the execute permission set for everybody
English: search current directory recursively for directory with execute permission set for _UNK
Original Command: find -type d ! -perm -111

Ground truth: find -type d ! -perm -_NUM
Prediction: find . -type d -perm "$permissions"
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(d)
        FLAG(-perm)
            ARGUMENT("$permissions")

Example 438 (1)
Original English: Search directory /tmp/foo for files containing "/tmp/foo/bar" in their full names
English: search directory "/tmp/foo" for file containing "/tmp/foo/bar" in full name
Original Command: find /tmp/foo -path /tmp/foo/bar -print

Ground truth: find /tmp/foo -path /tmp/foo/bar -print
Prediction: find /tmp/foo/bar -path /tmp/foo/bar -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/tmp/foo/bar)
        FLAG(-path)
            ARGUMENT(/tmp/foo/bar)
        FLAG(-print)

sl splitted into: -s -l 
Error: -sl is not a flag of grep
Warning: to_ast unrecognized argument attachment point BINARYLOGICOP_-or.
Example 439 (1)
Original English: Find all .rb and .yml files in the /some/path directory tree and replace "some_phrase" with "replacement_phrase" in them
English: find all ".rb" and _UNK file in "/some/path" directory tree and replace _UNK with _UNK in
Original Command: find /some/path -name "*rb" -o -name "*yml" | xargs grep -sl "some_phrase" | xargs sed -i -e 's/some_phrase/replacement_phrase/g'

Ground truth: find /some/path \( -name "*rb" -or -name "*yml" \) | xargs grep -s -l "some_phrase" | xargs sed -i -e 's/some_phrase/replacement_phrase/g'
Prediction: find /opt \( -name '*.rb' -or UNK \)
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/opt)
        BINARYLOGICOP(-or)
            FLAG(-name)
                ARGUMENT('*.rb')
            ARGUMENT(UNK)

Example 440 (1)
Original English: find all directories that names are 'project.images' and display details
English: find all directory name _UNK and display detail
Original Command: find  / -type d -name "project.images" -ls

Ground truth: find / -type d -name "project.images" -ls
Prediction: find . -type d -name Cookbook -type d
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(d)
        FLAG(-name)
            ARGUMENT(Cookbook)
        FLAG(-type)
            ARGUMENT(d)

Example 441 (1)
Original English: Find *.avi and *.flv files in /path/to/your/directory and below and copy them to /path/to/specific/folder
English: find _UNK and _UNK file in _UNK and below and copy to _UNK
Original Command: find /path/to/your/directory -regex '.*\.\(avi\|flv\)' -exec cp {} /path/to/specific/folder \;

Ground truth: find /path/to/your/directory -regex '.*\.\(avi\|flv\)' -exec cp {} /path/to/specific/folder ;
Prediction: find UNK -type f -name UNK -exec cp UNK UNK ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-exec::;)
            HEADCOMMAND(cp)
                ARGUMENT(UNK)
                ARGUMENT(UNK)

Example 442 (1)
Original English: Find files newer than start.txt but not newer than end.txt
English: find file newer than _UNK but not newer than _UNK
Original Command: find ./ -newer start.txt -and ! -newer end.txt

Ground truth: find ./ \( -newer start.txt -and ! -newer end.txt \)
Prediction: find / -newer /etc/motd -newer UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-newer)
            ARGUMENT(/etc/motd)
        FLAG(-newer)
            ARGUMENT(UNK)

Example 443 (1)
Original English: Find all files whose permission are 777
English: find all file whose permission "_NUM"
Original Command: find / -type f -perm 777

Ground truth: find / -type f -perm _NUM
Prediction: find / -perm _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-perm)
            ARGUMENT(_NUM)

n1 splitted into: -n -1 
Error: -n1 is not a flag of xargs
Example 444 (1)
Original English: Copy a file xyz.c to all the directories below the current one whose names begin with "temp"
English: copy file "xyz.c" to all directory below current "_NUM" whose name begin with "temp"
Original Command: find . -type d -name "temp*" | xargs -n1 cp xyz.c

Ground truth: find . -type d -name "temp*" | xargs -n -1 cp xyz.c
Prediction: find . -name UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)

Example 445 (1)
Original English: Search the 'tmp' directory for .mp3 files
English: search "tmp" directory for ".mp_NUM" file
Original Command: find tmp -maxdepth 1 -name '*.mp3'

Ground truth: find tmp -maxdepth _NUM -name '*.mp_NUM'
Prediction: find / -name '*.mp_NUM'
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-name)
            ARGUMENT('*.mp_NUM')

Example 446 (1)
Original English: find all the regular/normal files in a directory which are atleast N levels ddep
English: find all "regular/normal" file in directory atleast _UNK level _UNK
Original Command: find dir1 -mindepth N -type f

Ground truth: find dir_NUM -mindepth N -type f
Prediction: find UNK -mindepth _NUM -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-mindepth)
            ARGUMENT(_NUM)
        FLAG(-type)
            ARGUMENT(f)

Example 447 (1)
Original English: print the files in the current directory and one level down to the current directory
English: print file in current directory and "_NUM" level down to current directory
Original Command: find -maxdepth 2 -name "sum.java"

Ground truth: find -maxdepth _NUM -name "sum.java"
Prediction: find -maxdepth _NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-maxdepth)
            ARGUMENT(_NUM)

Example 448 (1)
Original English: Search the filesystem (begin at root) for manpage directories.
English: search filesystem ( begin at root ) for _UNK directory
Original Command: find / -type d -name 'man*' -print

Ground truth: find / -type d -name 'man*' -print
Prediction: find / \( -nouser -or -name /etc \) -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        BINARYLOGICOP(-or)
            FLAG(-nouser)
            FLAG(-name)
                ARGUMENT(/etc)
        FLAG(-print)

Example 449 (1)
Original English: display in a list of all the files that are bigger than 10KB in current folder
English: display in list of all file bigger than "_NUMKB" in current folder
Original Command: find . -size +10k -ls

Ground truth: find . -size +_NUMk -ls
Prediction: find . -xdev -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-xdev)
        FLAG(-print)

Example 450 (1)
Original English: Find all regular files that reside in the current directory tree and were last modified more than 7 days ago
English: find all regular file reside in current directory tree and last modified more than "_NUM" day ago
Original Command: find . -type f -mtime +7

Ground truth: find . -type f -mtime +_NUM
Prediction: find . -type f -mtime +_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-mtime)
            ARGUMENT(+_NUM)

Example 451 (1)
Original English: Search for .zip files that are larger than 100M found anywhere in the file system and delete those files.
English: search for ".zip" file larger than "_NUMM" found anywhere in file system and delete file
Original Command: find / -type f -name *.zip -size +100M -exec rm -i {} \;

Ground truth: find / -type f -name *.zip -size +_NUMM -exec rm -i {} ;
Prediction: find / -type f -name "$a" -exec rm {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-name)
            ARGUMENT("$a")
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT({})

Error: --target-directory=destDir is not a flag of mv
Error: --target-directory=destDir is not a flag of mv
Example 452 (2)
Original English: Move all files from the `sourceDir' directory tree to the `destDir' directory
English: move all file from "sourceDir" directory tree to _UNK directory
Original Command: find sourceDir -mindepth 1 -print0 | xargs -0 mv --target-directory=destDir

Ground truth: find sourceDir -mindepth _NUM -print0 | xargs -0 mv --target-directory=destDir
Prediction: find sourceDir | xargs -I _NUM mv {}
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(sourceDir)
        HEADCOMMAND(xargs)
            FLAG(-I)
                ARGUMENT(_NUM)
            HEADCOMMAND(mv)
                ARGUMENT({})

Example 453 (1)
Original English: Find '.git' directories in directory tree /home/madhu/release/workspace
English: find ".git" directory in directory tree _UNK
Original Command: find /home/madhu/release/workspace -type d -name '.git'

Ground truth: find /home/madhu/release/workspace -type d -name '.git'
Prediction: find A -type d -name mydir
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(A)
        FLAG(-type)
            ARGUMENT(d)
        FLAG(-name)
            ARGUMENT(mydir)

Error: -xdev is not a flag of find
Example 454 (1)
Original English: Find regular files under / that contain "stringtofind" and clear out their contents
English: find regular file under "/" contain "stringtofind" and _UNK out content
Original Command: find / -maxdepth 1 -xdev -type f -exec grep -i "stringtofind" -l {} \; -exec sed -i '/./d' {} \;

Ground truth: find / -maxdepth _NUM -xdev -type f -exec grep -i "stringtofind" -l {} ; -exec sed -i '/./d' {} ;
Prediction: find / -type f -perm UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-perm)
            ARGUMENT(UNK)

Example 455 (1)
Original English: Find all files under the current directory whose filenames are not "file.txt", ignoring the case
English: find all file under current directory whose filename not "file.txt" ignoring case
Original Command: find . -maxdepth 1 -not -iname file.txt

Ground truth: find . -maxdepth _NUM -not -iname file.txt
Prediction: find -maxdepth _NUM -iname 'MyFile*'
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-maxdepth)
            ARGUMENT(_NUM)
        FLAG(-iname)
            ARGUMENT('MyFile*')

Example 456 (1)
Original English: search for a file in a folder ( case insensitive search )
English: search for file in folder ( case insensitive search )
Original Command: find /usr/share/doc -iname readme\*

Ground truth: find /usr/share/doc -iname readme*
Prediction: find /usr/local -iname "*blast*"
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/usr/local)
        FLAG(-iname)
            ARGUMENT("*blast*")

Example 457 (3)
Original English: Remove all vmware-*.log files under current directory
English: remove all _UNK file under current directory
Original Command: find . -name vmware-*.log -delete

Ground truth: find . -name vmware-*.log -delete
Prediction: find . -name '*.rb' -exec rm {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT('*.rb')
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT({})

Example 458 (1)
Original English: search for all the files in the current directory which have size greater than 10KB (approx) and less than 32KB(approx).
English: search for all file in current directory size greater than "_NUMKB" ( _UNK ) and le than _UNK _UNK )
Original Command: find . -size +10000c -size -32000c -print

Ground truth: find . -size +_NUMc -size -_NUMc -print
Prediction: find . -size -_NUMc
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-size)
            ARGUMENT(-_NUMc)

Example 459 (1)
Original English: find all the files in a folder which have been modified in the last one day
English: find all file in folder modified in last "_NUM" day
Original Command: find /tmp/test/* -daystart -mtime -1

Ground truth: find /tmp/test/* -daystart -mtime -_NUM
Prediction: find $dir -daystart -ctime -_NUM -daystart -ctime -_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT($dir)
        FLAG(-daystart)
        FLAG(-ctime)
            ARGUMENT(-_NUM)
        FLAG(-daystart)
        FLAG(-ctime)
            ARGUMENT(-_NUM)

Example 460 (1)
Original English: find all fonts which belong to a specific user
English: find all _UNK belong to specific user
Original Command: find /usr/local/fonts -user warwick

Ground truth: find /usr/local/fonts -user warwick
Prediction: find -user UNK -user UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-user)
            ARGUMENT(UNK)
        FLAG(-user)
            ARGUMENT(UNK)

Example 461 (1)
Original English: Identify files that do not have a listing in the /etc/passwd or /etc/group file
English: identify file not listing in "/etc/passwd" or _UNK file
Original Command: find / -nouser -o  -nogroup

Ground truth: find / \( -nouser -or -nogroup \)
Prediction: find . -name '*.png'
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        BINARYLOGICOP(-or)
            FLAG(-name)
                ARGUMENT('*.png')

Example 462 (1)
Original English: find all html or cgi files in current folder
English: find all html or cgi file in current folder
Original Command: find ./ -type f -iregex ".*\.html$" -or -iregex ".*\.cgi$"

Ground truth: find ./ -type f \( -iregex ".*\.html$" -or -iregex ".*\.cgi$" \)
Prediction: find . -name '*.html'
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT('*.html')

Example 463 (1)
Original English: Find all files under and below the current working directory with the word California in the file (case insensitive), and count the number of lines in the output
English: find all file under and below current working directory with word california in file ( case insensitive ) and count number of line in output
Original Command: find . -type f -exec grep -i California {} \; -print | wc -l

Ground truth: find . -type f -exec grep -i California {} ; -print | wc -l
Prediction: find . -type f -exec grep California {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-exec::;)
            HEADCOMMAND(grep)
                ARGUMENT(California)
                ARGUMENT({})

Quotation Error: space inside word 'iText that gets prepended (dont remove the i)'
Example 464 (1)
Original English: find all the text files in the current folder starting with "somefiles-"  and prepend the first line
English: find all text file in current folder starting with _UNK and _UNK first line
Original Command: find . -name "somefiles-*-.txt" -type f -exec sed -i 'iText that gets prepended (dont remove the i)' -- '{}' \;

Ground truth: find . -name "somefiles-*-.txt" -type f -exec sed -i _LONG_PATTERN '{}' ;
Prediction: find . -name UNK -type f -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-print)

Error: -regextype is not a flag of find
Error: -fprint is not a flag of find
Example 465 (1)
Original English: find all files in a directory using regular expressions and save the file list to the file specified in the variable $FILE_LIST
English: find all file in directory using regular expression and save file list to file specified in variable _UNK
Original Command: find $TARGET_DIR -regextype posix-extended -regex \".*/$now.*\" -fprint $FILE_LIST

Ground truth: find $TARGET_DIR -regextype posix-extended -regex \".*/$now.*\" -fprint $FILE_LIST
Prediction: find UNK -regextype sed -regex UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-regextype)
        ARGUMENT(sed)
        FLAG(-regex)
            ARGUMENT(UNK)

Example 466 (1)
Original English: Finding files which contain a certain string using find and grep
English: finding file contain certain string using find and grep
Original Command: find . -type f -print | xargs grep "some string"

Ground truth: find . -type f -print | xargs grep _LONG_PATTERN
Prediction: find . -type f -exec grep -l {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-exec::;)
            HEADCOMMAND(grep)
                FLAG(-l)
                ARGUMENT({})

Example 467 (1)
Original English: Find files that are 100k
English: find file "_NUMk"
Original Command: find -size 100k

Ground truth: find -size _NUMk
Prediction: find / -type f
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-type)
            ARGUMENT(f)

Example 468 (1)
Original English: search for the word "damian" in all the regular/normal files in the /etc folder and display only the matched file name
English: search for word _UNK in all "regular/normal" file in "/etc" folder and display only matched file name
Original Command: find /etc -type f | xargs grep -l -i "damian"

Ground truth: find /etc -type f | xargs grep -l -i "damian"
Prediction: find /etc -type f -exec grep -H '{}' /dev/null {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/etc)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-exec::;)
            HEADCOMMAND(grep)
                FLAG(-H)
                ARGUMENT('{}')
                ARGUMENT(/dev/null)
                ARGUMENT({})

Example 469 (1)
Original English: Find all files named 'file' in 1 level down the current directory whose status were changed more than 1 day ago
English: find all file named "file" in "_NUM" level down current directory whose status changed more than "_NUM" day ago
Original Command: find . -maxdepth 1 -ctime +1 -name file

Ground truth: find . -maxdepth _NUM -ctime +_NUM -name file
Prediction: find -maxdepth _NUM -ctime +_NUM -ctime +_NUM
AST: 
ROOT(root)
    HEADCOMMAND(find)
        FLAG(-maxdepth)
            ARGUMENT(_NUM)
        FLAG(-ctime)
            ARGUMENT(+_NUM)
        FLAG(-ctime)
            ARGUMENT(+_NUM)

Example 470 (1)
Original English: Find the top 5 small files
English: find top "_NUM" small file
Original Command: find . -type f -exec ls -s {} \; | sort -n  | head -5

Ground truth: find . -type f -exec ls -s {} ; | sort -n | head -_NUM
Prediction: find . -type f | head
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-type)
                ARGUMENT(f)
        HEADCOMMAND(head)

Example 471 (1)
Original English: Delete all files under /path/to/files that are not newer than dummyfile
English: delete all file under _UNK not newer than _UNK
Original Command: find /path/to/files -type f ! -newer dummyfile -delete

Ground truth: find /path/to/files -type f ! -newer dummyfile -delete
Prediction: find UNK -newer UNK
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(UNK)
        FLAG(-newer)
            ARGUMENT(UNK)

Quotation Error: space inside word '%p %s\n'
Quotation Error: space inside word '{sum+=$NF}END{print sum}'
Quotation Error: space inside word '%p %s\n'
Quotation Error: space inside word '{ sum+=$2}; END { print sum}'
Quotation Error: space inside word '{sum += $1} END {print sum}'
Example 472 (3)
Original English: Get the total sizes of all files under current directory
English: get total size of all file under current directory
Original Command: find . -type f -printf '%p %s\n'  | awk '{sum+=$NF}END{print sum}'

Ground truth: find . -type f -printf _LONG_PATTERN | awk _LONG_PATTERN
Prediction: find . -type f | awk "%s\n"
AST: 
ROOT(root)
    PIPELINE()
        HEADCOMMAND(find)
            ARGUMENT(.)
            FLAG(-type)
                ARGUMENT(f)
        HEADCOMMAND(awk)
            ARGUMENT("%s\n")

Example 473 (1)
Original English: Find all pdf files under /dir/containing/unsigned with null character as the delimiter
English: find all pdf file under _UNK with null character delimiter
Original Command: find /dir/containing/unsigned -name '*.pdf' -print0

Ground truth: find /dir/containing/unsigned -name '*.pdf' -print0
Prediction: find ./polkadots -name UNK -print0
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(./polkadots)
        FLAG(-name)
            ARGUMENT(UNK)
        FLAG(-print0)

Error: -writable is not a flag of find
Example 474 (1)
Original English: find all the files in the current folder which are writable
English: find all file in current folder writable
Original Command: find . -writable

Ground truth: find . -writable
Prediction: find . -depth -name -print
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(.)
        FLAG(-depth)
            ARGUMENT(-name)
        FLAG(-print)

rf splitted into: -r -f 
Error: -rf is not a flag of rm
Example 475 (1)
Original English: Find all 100MB files in file system and delete them using rm command
English: find all "_NUMMB" file in file system and delete using rm command
Original Command: find / -size +100M -exec rm -rf {} \;

Ground truth: find / -size +_NUMM -exec rm -r -f {} ;
Prediction: find / -size +_NUMM -type f -exec rm {} ;
AST: 
ROOT(root)
    HEADCOMMAND(find)
        ARGUMENT(/)
        FLAG(-size)
            ARGUMENT(+_NUMM)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-exec::;)
            HEADCOMMAND(rm)
                ARGUMENT({})

475 examples evaluated
Percentage of Template Match = 0.17
Percentage of String Match = 0.05

