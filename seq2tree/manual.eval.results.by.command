Example 1 (1)
English: Look for *log files in directories at most three levels down the directory tree
GT Command 1: find / -maxdepth 3  -name "*log"
Prediction: find -mindepth _NUM -type f -name CVS
WW

Example 2 (1)
English: Find all files in  /mydir  and replace every occurrences of <string1> with <string2> in those files invoking sed as few times as possible
GT Command 1: find /mydir -type f -exec sed -i 's/<string1>/<string2>/g' {} +
Prediction: find /usr -type f -print
WW

Example 3 (1)
English: Find and the 5 largest regular files in the Downloads folder of tecmint's home directory and output the file sizes in bytes.
GT Command 1: find /home/tecmint/Downloads/ -type f -printf "%s %p\n" | sort -rn | head -n 5
Prediction: find UNK -type f | sort
WW

Example 4 (1)
English: Find out all *.sh owned by user vivek
GT Command 1: find / -user vivek -name "*.sh"
Prediction: find / -user UNK
WW

Example 5 (1)
English: show all the ".acc" files in the folder /home
GT Command 1: find /home -type f -name '*.aac'
Prediction: find /home -name UNK
CW

Example 6 (1)
English: find all the files similar to top which have been modified after a file is modified
GT Command 1: find ~ -name 'top*' -newer /etc/motd
Prediction: find -newer /etc/motd
WW

Example 7 (1)
English: find all files in home folder that begin with a specific word
GT Command 1: find ~ -iname "screen*"
Prediction: find $HOME -name UNK
CW

Example 8 (1)
English: delete all the files in the current folder which have been modified in the last 14*24 hours
GT Command 1: find . -mtime -14 -print|xargs -i rm \;
Prediction: find . -mtime -_NUM -exec rm {} \;
CW

Example 9 (1)
English: Find all the files without permission 777
GT Command 1: find / -type f ! -perm 777
Prediction: find . -type f -perm _NUM
WW

Example 10 (1)
English: Search the current directory recursively for regular files last accessed more than 2 days ago
GT Command 1: find . type -f -atime +2
Prediction: find . type -type f
WW

Example 11 (1)
English: Search for file names with "bad" characters in the current directory and delete the files.
GT Command 1: find . -name '*[+{;"\\=?~()<>&*|$ ]*' -maxdepth 0 -exec rm -f '{}' \;
Prediction: find . -name UNK -delete
CW

Example 12 (1)
English: Find files/directories under current directory that matches 'projects/insanewebproject' in their paths
GT Command 1: find -ipath 'projects/insanewebproject'
Prediction: find . -wholename UNK | grep -q UNK
WW

Example 13 (1)
English: save the list of the files in the current directory to a file “foo”
GT Command 1: find . -fprint foo
Prediction: find . -name '*.rb' -exec rm {} ;
WW

Example 14 (1)
English: Search for "YOURSTRING" in all files under current directory
GT Command 1: grep YOURSTRING `find .`
Prediction: find . -type f -print | xargs grep "text"
CW

Example 15 (2)
English: search for files that are readable for everybody, have at least on write bit set but are not executable for anybody
GT Command 1: find . -perm -444 -perm /222 ! -perm /111
GT Command 2: find . -perm -a+r -perm /a+w ! -perm /a+x
Prediction: find / -perm -_NUM -print
WW

Example 16 (1)
English: Search the current directory tree for executable files and searchable directories
GT Command 1: find -executable
Prediction: find . -perm /etc
WW

Example 17 (1)
English: print the files in the current directory and one level down to the current directory
GT Command 1: find -maxdepth 2 -name "sum.java"
Prediction: find -maxdepth _NUM
CW

Example 18 (1)
English: Print a sorted list of all .jpg files in the current directory and below
GT Command 1: find -name '*.jpg' | sort -n
Prediction: find . -name UNK | sort
CW

Example 19 (1)
English: find not case sensitive all directories that names are 'project.images'
GT Command 1: find  / -type d -iname "project.images" -ls
Prediction: find / -type d -iname "apt"
CW

Example 20 (1)
English: display in a list of all the files that are bigger than 10KB in current folder
GT Command 1: find . -size +10k -ls
Prediction: find . -xdev -print
WW

Example 21 (1)
English: Search for file "file" between level 2 and 3 of the directory tree
GT Command 1: find -mindepth 2 -maxdepth 3 -name file
Prediction: find -mindepth _NUM -mindepth _NUM -name -mindepth _NUM
WW

Example 22 (1)
English: find all files in home folder which have been modified exactly 1 day before
GT Command 1: find ~ -mtime 1 -daystart
Prediction: find $HOME -mtime _NUM
CW

Example 23 (1)
English: Copy all regular files whose names end in "~" from the /path directory tree to ~/backups/
GT Command 1: find /path -type f -name '*~' -print0 | xargs -0 -I % cp -a % ~/backups
Prediction: find /path -name "*blast*" -exec cp '{}' ;
WW

Example 24 (1)
English: Delete all MP3 files under /tmp
GT Command 1: find /tmp -iname '*.mp3' -print0 | xargs -0 rm
Prediction: find /tmp -name '.*' -delete
CW

Example 25 (1)
English: display all the files in current directory with each file name displayed twice in the same row
GT Command 1: find . | sed 's/.*/& &/'
Prediction: find . -wholename UNK
WW

Example 26 (1)
English: Search the current directory recursively for files last modified within the past 24 hours ignoring paths ./es* and ./en*
GT Command 1: find . -mtime 0 | grep -v '^\./en' | grep -v '^\./es'
Prediction: find . -not -name UNK -not -name UNK
WW

Example 27 (1)
English: Find all *.txt files under current directory and copy them to ./tmp
GT Command 1: find . -type f -name '*.txt' | sed 's/'"'"'/\'"'"'/g' | sed 's/.*/"&"/'  | xargs -I{} cp -v {} ./tmp/
Prediction: find . -name "*.txt" -type f | xargs cp -f UNK
WW

Example 28 (3)
English: Get the total sizes of all files under current directory
GT Command 1: find . -type f -printf '%p %s\n'  | awk '{sum+=$NF}END{print sum}'
GT Command 2: find . -type f -printf '%p %s\n' | awk '{ sum+=$2}; END { print sum}'
GT Command 3: find path -type f -printf '%s\n' | awk '{sum += $1} END {print sum}'
Prediction: find . -type f | awk "%s\n"
WW

Example 29 (1)
English: Search the "your/dir" directory for empty subdirectories
GT Command 1: find your/dir -mindepth 1 -prune -empty
Prediction: find -prune -mindepth _NUM -type d -empty
WW

Example 30 (1)
English: find all the files in the entire filesystem which belong to the group root and display the ten files.
GT Command 1: find / -group root | head
Prediction: find / -group
WW


30 examples evaluated
Percentage of Template Match = 0.33
Percentage of String Match = 0.00

