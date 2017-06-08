#!/bin/bash
FILES=/usr/share/man/*
#f=./man/man1/find.1
for f in $FILES
do
    echo "Extracting man page $f into plain-man/"$filename".txt"
    # take action on each file. $f store current file name
    filename=$(basename "$f")
    groff -t -e -mandoc -Tascii $f | col -bx > "plain-man/$filename.txt"
done
