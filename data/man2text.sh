#!/bin/bash

manfolder=$1

FILES=/usr/share/man/$manfolder/*
#f=./man/man1/find.1
for f in $FILES
do
    # take action on each file. $f store current file name
    utility=$( cut -d '.' -f 1 <<< $(basename "$f") )
    
    echo "Extracting man page $f into plain-man/"$utility".txt"
    # groff -t -e -mandoc -Tascii $f | col -bx > "plain-man/$manfolder/$utility.txt"
    man $utility > "plain-man/$manfolder/$utility.txt"
done
