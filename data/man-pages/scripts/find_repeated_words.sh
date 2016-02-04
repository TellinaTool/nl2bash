#!/bin/sh
#
# find_repeated_words.sh
#
# A simple script for finding instances of repeated consecutive words
# in manual pages -- human inspection can then determine if these
# are real errors in the text.
#
# Usage: sh find_repeated_words.sh [file...]
#
######################################################################
#
# (C) Copyright 2007 & 2013, Michael Kerrisk
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

for file in "$@" ; do 
   # Do not process files that are redirects.
   grep -qE "^\.so man.*" "$file"
   if test $? -ne 0; then
    words=$(MANWIDTH=2000 man -l "$file" 2> /dev/null | col -b | \
	tr ' \008' '\012' | sed -e '/^$/d' | \
	sed 's/ *$//' | 
	awk 'BEGIN {p=""} {if (p==$0) print p; p=$0}' | \
	grep '[a-zA-Z]' | tr '\012' ' ')
    if test -n "$words"; then
        echo "$file: $words"
    fi
   fi
done
