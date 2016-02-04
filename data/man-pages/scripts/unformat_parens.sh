#!/bin/sh
#
# unformat_parens.sh
#
# The manual pages before 2.10 format parentheses
# inconsistently.  In some cases they are like:
#
#       .B name()
#
# while in others they are like:
#
#       .BR name ()
#
# This script changes instances to the latter format.
# It does not fix all such instances: some will have to be 
# done manually.
#
# Use the "-n" option for a dry run, in order to see what would be
# done, without actually doing it.
#
######################################################################
#
# (C) Copyright 2005 & 2013, Michael Kerrisk
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details
# (http://www.gnu.org/licenses/gpl-2.0.html).
#
#

file_base="tmp.$(basename $0)"

work_dst_file="$file_base.dst"
work_src_file="$file_base.src"

all_files="$work_dst_file $work_src_file"

# Command-line option processing

really_do_it=1
while getopts "n" optname; do
    case "$optname" in
    n)	really_do_it=0;
    	;;
    *)  echo "Unknown option: $OPTARG"
        exit 1
	;;
    esac
done

shift $(( $OPTIND - 1 ))

# Only process files with > 1 line -- single-line files are link files 

for page in $(wc "$@" 2> /dev/null | awk '$1 > 1 {print $4}'| \
    grep -v '^total'); do

    cp $page $work_dst_file

    echo ">>>>>>>>>>>>>>>>>>>>>>>>>" $page "<<<<<<<<<<<<<<<<<<<<<<<<<"

    if false; then
    grep '^\.I *[a-z0-9_][a-z0-9_]*()$' $page
    grep '^\.B *[a-z0-9_][a-z0-9_]*()$' $page
    echo '###'
    grep '^\.[BIR][BIR] *[a-z0-9_][a-z0-9_]*()$' $page
    echo '###'
    grep '^\.[BIR][BIR] *[a-z0-9_][a-z0-9_]*() [^"]*$' $page
    echo '###'
    grep '()\\f[PR]' $page
    echo '###'
    fi

    cp $work_dst_file $work_src_file
    cat $work_src_file | \
	sed \
	-e '/^\.B *[a-z0-9_][a-z0-9_]*() *$/s/^\.B/.BR/' \
	-e '/^\.I *[a-z0-9_][a-z0-9_]*() *$/s/^\.I/.IR/' \
	> $work_dst_file

    cp $work_dst_file $work_src_file
    cat $work_src_file | \
	sed \
	-e '/^\.[BIR][BIR] *[a-z0-9_][a-z0-9_]*()$/s/()/ ()/' \
	> $work_dst_file

    cp $work_dst_file $work_src_file
    cat $work_src_file | \
	sed \
	-e '/^\.[BIR][BIR] *[a-z0-9_][a-z0-9_]*() [^"]*$/s/() / ()/' \
	> $work_dst_file

    cp $work_dst_file $work_src_file
    cat $work_src_file | \
	sed \
	-e '/()\\fP/s/()\\fP/\\fP()/g' \
	-e '/()\\fR/s/()\\fR/\\fR()/g' \
	> $work_dst_file

    if ! cmp -s $page $work_dst_file; then
        diff -u $page $work_dst_file

	if test $really_do_it -ne 0; then
            cat $work_dst_file > $page
	fi

    else
        echo "### NOTHING CHANGED"
    fi
done

# clean up

rm -f $all_files
exit 0
