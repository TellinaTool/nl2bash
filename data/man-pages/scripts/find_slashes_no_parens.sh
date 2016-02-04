#!/bin/sh
#
# find_slashes_no_parens.sh
#
# Look for function names inside \f[BI]...\f[PB] that aren't
# followed by "()".
#
# This script is designed to help with "by hand" tidy-ups after
# the automated changes made by add_parens_for_own_funcs.sh.
#
# The first argument to this script names a manual page directory where 
# 'man2' and 'man3' subdirectories can be found.  The pages names in 
# these directories are used to generate a series of regular expressions 
# that can be used to search the manual page files that are named in 
# the remaining command-line arguments.
#
# Example usage: 
#
#    cd man-pages-x.yy
#    sh find_slashes_no_parens.sh . man?/*.? > matches.log
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

if test $# -lt 2; then
    echo "Usage: $0 man-page-root-dir file file..." 1>&2
    exit 1
fi

dir=$1

if ! test -d $dir/man2 || ! test -d $dir/man3; then
    echo "Can't find man2 and man3 under $dir" 1>&2
    exit 1
fi

shift 1

echo "This will probably take a few minutes..." 1>&2

regexp_file=tmp.$0.regexp
rm -f $regexp_file

# We grep out a few page names that are likely to generate false 
# positives...

for page in $(

	find $dir/man2/* $dir/man3/* -type f -name '*.[23]' | 
	egrep -v '/(stderr|stdin|stdout|errno|termios|string)\..$'); do
    
    base=$(basename $page | sed -e 's/\.[23]$//')

    echo "\\\\f[BI]$base\\\\f[PB][^(]" >> $regexp_file
    echo "\\\\f[BI]$base\\\\f[PB]\$" >> $regexp_file
done

sort -o $regexp_file $regexp_file	# Not really needed

echo "Built regexp file; now about to grep..." 1>&2

grep -f $regexp_file $*

rm -f $regexp_file
exit 0
