#!/bin/sh
#
# add_parens_for_own_funcs.sh
#
# This script is designed to fix inconsistencies in the use of
# parentheses after function names in the manual pages.
# It changes manual pages to add these parentheses.
# The problem is how to determine what is a "function name".
# The approach this script takes is the following:
#
#   For each manual page named in the command line that contains 
#           more than one line (i.e., skip man-page link files)
#       Create a set of names taken from the .SH section of the
#               page and from grepping all pages for names that 
#               have .so links to this page
#       For each name obtained above
#           If we can find something that looks like a prototype on 
#                   the page, then
#               Try to substitute instances of that name on the page.
#                   (instances are considered to be words formatted
#		    using ^.[BI] or \f[BI]...\f[PR] -- this script
#		    ignores unformatted instances of function names.)
#           fi
#       done
#   done
#
# The rationale of the above is that the most likely function names
# that appear on a page are those that the manual page is describing.
# It doesn't fix everything, but it catches many instances.
# The rest will have to be done manually.
#
# This script is rather verbose because it provides a computer-assisted
# solution, rather than one that is fully automated.  When running it,
# pipe the output through
#
#            ...  2>&1 | less
#
# and take a good look at the output.  In particular, you can scan
# the output for *possible* problems by looking for the pattern: /^%%%/
# The script's output should be enough to help you determine if the 
# problem is real or not.
#
# Suggested usage (in this case to fix pages in Section 2):
#
#     cd man2
#     sh add_parens_for_own_funcs.sh *.2 2>&1 | tee changes.log | less
#
# Use the "-n" option for a dry run, in order to see what would be
# done, without actually doing it.
#
# (And, yes, there are many ways that this script could probably be 
# made to work faster...)
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
# 

file_base="tmp.$(basename $0)"

work_dst_file="$file_base.dst"
work_src_file="$file_base.src"

matches_for_all_names="$file_base.all_match"
matches_for_this_name="$file_base.this_match"

all_files="$work_dst_file $work_src_file $matches_for_all_names \
	   $matches_for_this_name"

rm -f $all_files

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

    echo ">>>>>>>>>>>>>>>>>>>>>>>>>" $page "<<<<<<<<<<<<<<<<<<<<<<<<<"
    echo ">>>>>>>>>>>>>>>>>>>>>>>>>" $page "<<<<<<<<<<<<<<<<<<<<<<<<<" 1>&2

    # Extract names that follow the ".SH NAME" directive -- these will
    # be our guesses about function names to look for

    sh_nlist=$(cat $page | \
        awk 'BEGIN { p = 0 } 
             /^\.SH NAME/     { p = NR } 
	     /^.SH/ && NR > p { p = 0 }	    # Stop at the next .SH directive
	     p > 0 && NR > p  { print $0 }  # These are the lines between
					    # the two .SH directives
	    ')
    sh_nlist=$(echo $sh_nlist | sed -e 's/ *\\-.*//' -e 's/, */ /g')
    echo "### .SH name list:" $sh_nlist

    # Some pages like msgop.2 don't actually list the function names in 
    # the .SH section -- but we can try using link pages to give us 
    # another guess at the right function names to look for

    so_nlist=$(grep -l "^\\.so.*/$(echo $page| \
	     sed -e 's/\.[1-8]$//')\\." $* | \
	     sed -e 's/\.[1-8]$//g')

    echo "### .so name list:" $so_nlist

    # Combine the two lists, eliminate duplicates
    
    nlist=$(echo $sh_nlist $so_nlist | tr ' ' '\012' | sort -u)

    maybechanged=0
    
    cp $page $work_dst_file
    rm -f $matches_for_all_names; # touch $matches_for_all_names

    for rname in $nlist; do	# try each name from out list for this page

        # A very few names in .SH sections contain regexp characters!

	name=$(echo $rname | sed -e 's/\*/\\*/g' -e 's/\./\\./g' \
		-e 's/\[/\\[/g' -e 's/\+/\\+/g')

        echo "########## trying $rname ##########"

	rm -f $matches_for_this_name
	
        grep "^.BR* $name *$" $page | \
	    >> $matches_for_this_name
        grep "^.BR $name [^(\"]$" $page | \
	    >> $matches_for_this_name
        grep '\\fB'"$name"'\\f[PR][ .,;:]' $page | \
	    >> $matches_for_this_name
        grep '\\fB'"$name"'\\f[PR]$' $page | \
	    >> $matches_for_this_name
	
	cat $matches_for_this_name | sed -e 's/^/### MATCH: /'
	cat $matches_for_this_name >> $matches_for_all_names

	# Only process a page if we can see something that looks
	# like a function prototype for this name in the page

        if grep -q "$name *(" $page || \
	    grep -q "$name\\\\f.[\\ ]*(" $page; then 

	    # '.B name$'
	    # '.BR name [^("]*$      
	    # (The use of [^"] in the above eliminates lines
	    # like: .BR func " and " func
	    # Those lines better be done manually.)
	    cp $work_dst_file $work_src_file
            cat $work_src_file | \
		sed \
		-e "s/^.BR* $name *\$/.BR $name ()/" \
		-e "/^.BR *$name [^(\"]*\$/s/^.BR *$name /.BR $name ()/" \
		> $work_dst_file

	    # '\fBname\fP[ .,;:]'
	    # '\fBname\fP$'
	    cp $work_dst_file $work_src_file
            cat $work_src_file | \
		sed \
		-e 's/\\fB'$name'\\fP /\\fB'$name'\\fP() /g' \
		-e 's/\\fB'$name'\\fP\./\\fB'$name'\\fP()./g' \
		-e 's/\\fB'$name'\\fP,/\\fB'$name'\\fP(),/g' \
		-e 's/\\fB'$name'\\fP;/\\fB'$name'\\fP();/g' \
		-e 's/\\fB'$name'\\fP:/\\fB'$name'\\fP():/g' \
		-e 's/\\fB'$name'\\fP$/\\fB'$name'\\fP()/g' \
		> $work_dst_file

	    # '\fBname\fR[ .,;:]'
	    # '\fBname\fR$'
	    cp $work_dst_file $work_src_file
            cat $work_src_file | \
		sed \
		-e 's/\\fB'$name'\\fR /\\fB'$name'\\fR() /g' \
		-e 's/\\fB'$name'\\fR\./\\fB'$name'\\fR()./g' \
		-e 's/\\fB'$name'\\fR,/\\fB'$name'\\fR(),/g' \
		-e 's/\\fB'$name'\\fR;/\\fB'$name'\\fR();/g' \
		-e 's/\\fB'$name'\\fR:/\\fB'$name'\\fR():/g' \
		-e 's/\\fB'$name'\\fR$/\\fB'$name'\\fR()/g' \
		> $work_dst_file

	    maybechanged=1
        else
            echo "%%%%%%%%%% WARNING: NO PROTOTYPE MATCHES FOR: $name"
        fi
    done

    # If the file was changed, then:
    # show "diff -U" output to user;
    # and count number of changed lines and compare it with what 
    # we expected, displaying a warning if it wasn't what was expected

    if test $maybechanged -ne 0 && ! cmp -s $page $work_dst_file; then
        diff -u $page $work_dst_file

        made_matches=$(diff -U 0 $page $work_dst_file | grep '^\+[^+]' | \
		wc -l | awk '{print $1}')

	# The following line makes the changes -- comment it out if you 
        # just want to do a dry run to see what changes would be made.

	if test $really_do_it -ne 0; then
            cat $work_dst_file > $page
	fi

    else
        echo "### NOTHING CHANGED"
	made_matches=0
    fi

    min_match=$(cat $matches_for_all_names | \
	    sort -u | wc -l | awk '{print $1}')

    echo "### Expected matches >= $min_match"
    echo "### Made matches $made_matches"

    if test $made_matches -lt $min_match; then
        echo "%%%%%%%%%% WARNING: NOT ENOUGH MATCHES: " \
	    "$made_matches < $min_match"
    fi
    
done 

# clean up

rm -f $all_files
exit 0
