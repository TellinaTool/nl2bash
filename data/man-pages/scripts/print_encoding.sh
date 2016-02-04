#!/bin/sh
#
# print_encoding.sh
#
# Print man pages with encoding other than us-ascii, together with
# their encoding by file utility and by the first line in the man page.
#
# Example usage:
#
#    cd man-pages-x.yy
#    sh print_encoding.sh man?/*
#
######################################################################
#
# (C) Copyright 2013, Peter Schiffer <pschiffe@redhat.com>
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

if [[ $# -lt 1 ]]; then
    echo "Usage: ${0} man?/*" 1>&2
    exit 1
fi

printf "\n   %-23s%-19s%s\n\n" "Man Page" "Encoding by file" "Encoding by first line"

for f in "$@"; do
    if [[ ! -f "$f" ]]; then
        continue
    fi

    enc=$(file -bi "$f" | cut -d = -f 2)
    if [[ $enc != "us-ascii" ]]; then
        lenc=$(head -n 1 "$f" | sed -n "s/.*coding: \([^ ]*\).*/\1/p")
        printf " * %-23s%-19s%s\n" "$f" "$enc" "$lenc"
    fi
done

exit 0
