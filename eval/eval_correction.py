#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Some manual evaluation correction.
"""

correct_temp_pairs = [
    (
        "search for a specific word in all the hidden files in the entire file system and display the file name along "
        "with the matched line\n",
        "find -exec grep -H Pattern {} \; -name Pattern File"
    ),
    (
        "create a tar ball of all pdf files in current folder\n",
        "find -name Pattern -print File | xargs -I {} tar -f File -r -v {}"
    ),
    (
        "start from current directory, skip the directory src/emacs and print it then skip all files and directories "
        "under it, and print the names of the other files found\n",
        "find \( -path File -prune -or -type f \) -print File"
    ),
    (
        "find all files in a folder that have a specific word in their name\n",
        "find -name Pattern -print File"
    ),
    (
        "Remove files in the current directory tree modified more than 31 days ago recursively\n",
        "find -exec rm {} \; -mtime Time File"
    ),
    (
        "dispaly a long listig of all the files in the current folder which are bigger than 100KB\n",
        "find -exec ls -l {} \; -size Size File"
    ),
    (
        "display all the files in the kat folder\n",
        "find File"
    ),
    (
        "display all sqlite files in the current directory along with their timestamp\n",
        "find -printf Pattern File"
    ),
    (
        "display all the regular/normal files in the folder /path/ which have not been modified today ( from day "
        "start ie, 00:00 )\n",
        "find -mtime Time -type f File"
    ),
    (
        "find the largest file in the current directory and sub directories\n",
        "find -maxdepth Number -printf Pattern -type f File | sort -n -r | head -n Number"
    ),
    (
        "find all occurences of a file in the file system which belong to the user root\n",
        "find -print -user Pattern File"
    ),
    (
        "Remove all broken symbolic links in /usr/ports/packages\n",
        "find -type l -xtype l File | xargs -I {} rm {}"
    ),
    (
        "Remove all broken symlinks from the /usr/ports/packages directory tree\n",
        "find -type l -xtype l File | xargs -I {} rm {}"
    ),
    (
        "Return a list of files newer than file poop\n",
        "find -exec ls -l {} \; -newer File File"
    ),
    (
        "Find files that are 0 bytes in size in the current directory and remove them\n",
        "find -exec rm {} \; -size Size File"
    ),
    (
        "Find files that are 0 bytes in size in the current directory and remove them\n",
        "find -print -size Size File | xargs -I {} rm {}"
    ),
    (
        "Find all *.texi files in /usr/local/doc\n",
        "find -iname Pattern -type f File"
    ),
    (
        "Delete files containing whitespaces without recursion\n",
        "find -exec rm -f {} \; -name Pattern -type f File"
    ),
    (
        "Remove files in the current directory tree modified more than 31 days ago recursively\n",
        "find -exec rm {} \; -mtime Time File"
    ),
    (
        "Remove all broken symlinks from the /usr/ports/packages directory tree\n",
        "find -exec rm {} \; -xtype l File"
    ),
    (
        "Remove all broken symlinks from the /usr/ports/packages directory tree\n",
        "find -exec rm {} \; -type l -xtype l File"
    ),
    (
        "Remove all broken symlinks from the /usr/ports/packages directory tree\n",
        "find -print0 -xtype l File | xargs -0 -I {} rm {}"
    ),
    (
        "Archive all *html files using tar.\n",
        "find -name Pattern -print0 File | xargs -0 -I {} tar -f File -u {}"
    ),
    (
        "create a tar ball of all pdf files in current folder\n",
        "find -name Pattern -print0 File | xargs -0 -I {} tar -f File -u {}"
    ),
    (
        "create a tar ball of all pdf files in current folder\n",
        "find -name Pattern -print0 File | xargs -0 -I {} tar -f File -r -v {}"
    )]

error_temp_pairs = [
    (
        "find  file which case-insensitive name is too in currect directory\n",
        "find -name Pattern File"
    ),
    (
        "Search directory foo for files containing \"foo/bar\" in their full names\n",
        "find foo -type f -iname foo | grep foo"
    ),
    (
        "display all sqlite files in the current directory along with their timestamp\n",
        "find -name Pattern File"
    ),
    (
        "Find all *.tex regular files under current directory\n",
        "find -type Unknown File"
    ),
    (
        "List root's regular files with permissions 4000\n",
        "find -exec ls -l {} \; -perm Permission -type Unknown File"
    ),
    (
        "list regular file which file name end with 'cache' 'xml' or 'html' in current directory\n",
        "find -name Pattern -type Unknown File"
    ),
    (
        "search for a specific word in all the hidden files in the entire file system and display "
        "the file name along with the matched line\n",
        "find -name Pattern File | xargs grep Pattern"
    ),
    (
        "find all '*.c' files under $HOME directory which context contains sprintf\n",
        "find -exec grep -H File Pattern {} \; -name Pattern -type f File"
    ),
    (
        "change the ownership of all directories in the current folder\n",
        "find -exec chmod Unknown {} \; -type d File"
    ),
    (
        "find foo, Foo, FOo, FOO, etc.\n",
        "find -iname Pattern -type f File File"
    ),
    (
        "Delete all files in the \"${S}/bundled-libs\" folder except \"libbass.so\"\n",
        "find -delete \( -name Pattern -or -name Pattern -or -name Pattern \) -type f File"
    ),
    (
        "Find files that are 0 bytes in size in the current directory and remove them\n",
        "find -exec rm {} \; -size Size File"
    ),
    (
        "force delete all the directories in a folder which  have a specific name\n",
        "find -exec rm -f {} \; -name Pattern -type d File"
    ),
    (
        "copy the file header.shtml to each directory under dir1, dir2, dir3, or dir4\n",
        "find -exec cp File {} \; -name Pattern -type f File"
    ),
    (
        "Find PHP files with abstract classes\n",
        "find -iname Pattern File"
    ),
    (
        "display all the regular files in the folder \"$(FOLDER)\" which are modified "
        "in the last $(RETENTION)*24 hours and excluding hidden files\n",
        "find ! -path File -mtime Time -type f File"
    ),
    (
        "search for a specific word in all the hidden files in the entire file system and display "
        "the file name along with the matched line\n",
        "find -name Pattern -type f File | xargs -I {} grep Pattern {}"
    ),
    (
        "Find all files and directories in the current directory tree with \"linkin park\" in " \
        "their names and copy them to /Users/tommye/Desktop/LP\n",
        "find -name Pattern -print0 File | xargs -0 -I {} cp File {}"
    ),
    (
        "display the top 20 biggest files in the current folder which are present in the same partition as that of "
        "the current folder\n",
        "find -printf Pattern -type f File | sort -n -r | head -n Number"
    ),
    (
        "Find all *.tex regular files in maximum 2 levels down the current directory\n",
        "find -maxdepth Number -type f File"
    ),
    (
        "display all the regular files in the current folder which dont not have the permission 777\n",
        "find -perm Permission -type f File"
    ),
    (
        "find any files in the current directory that begin with a number\n",
        "find -name Pattern File"
    ),
    (
        "find file which case-insensitive name is foo in current directory.\n",
        "find -name Pattern File"
    ),
    (
        "Remove all \"work\" directories residing in /usr/ports and below\n",
        "find -exec rm {} \; -name Pattern -type d File"
    ),
    (
        "List root's regular files with permissions 4000\n",
        "find -exec ls -l {} \; -perm Permission -print -type f File"
    ),
    (
        "display all sqlite files in the current directory along with their timestamp\n",
        "find -printf Pattern File"
    ),
    (
        "Find .gif and .png image files in ~/Desktop and move them to the ~/Pictures directory.\n",
        "find -exec mv File {} \; -name Pattern File"
    ),
    (
        "display all the files in the current directory excluding the paths \"targert\", \"tools\", \"git\"\n",
        "find \( -path File -prune -or -print \) File"
    ),
    (
        "Delete all .svn files/directories under current directory\n",
        "find -exec rm {} \; -name Pattern File"
    ),
    (
        "Copy file header.shtml to directories dir1, dir2, dir3, and dir4\n",
        "find -exec cp File {} \; -name Pattern File"
    )]

correct_str_pairs = [
    (
        "List all empty files in the current directory tree\n",
        "find . -empty"
    )]

error_str_pairs = [
    (
        "find  file which case-insensitive name is too in currect directory\n",
        "find . -iname \"filename\""
    ),
    (
        "search for files with the name \"temp\" in the /usr folder\n",
        "find /usr -name '*.sh'"
    ),
    (
        "Find all the files called FindCommandExamples.txt of owner root\n",
        "find / -user root -name tecmint.txt"
    ),
    (
        "Find all .c and .h files in the current directory tree and search them for \"expr\"\n",
        "find . -name '*.[ch]' | xargs grep -E 'expr'"
    ),
    (
        "Find all *.py files under and below the current directory and search them for \"xrange\"\n",
        "find . -name *.py | xargs grep some_function"
    ),
    (
        "Find all .c and .h files in the current directory tree and search them for \"expr\"\n",
        "find . -name \"*.c\" | xargs grep -E 'expr'"
    ),
    (
        "find all the swap files (files ending with ~) in the current folder and delete them\n",
        "find . -name \"*.sh\" -exec rm -r -f {} \;"
    ),
    (
        "display all files in the current directory excluding those that are present in the directories whose name starts with \"efence\" and do not search in the sub directories\n",
        "find \( -name Pattern -prune -or -name Pattern \) -print File"
    )]
