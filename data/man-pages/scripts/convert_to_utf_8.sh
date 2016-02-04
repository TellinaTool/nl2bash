#!/bin/sh
#
# convert_to_utf_8.sh
#
# Find man pages with encoding other than us-ascii, and convert them
# to the utf-8 encoding.
#
# Example usage:
#
#    cd man-pages-x.yy
#    sh convert_to_utf_8.sh <output_dir> man?/*
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

if [[ $# -lt 2 ]]; then
    echo "Usage: ${0} <output_dir> man?/*" 1>&2
    exit 1
fi

out_dir="$1"
shift

enc_line="'\\\" t -*- coding: UTF-8 -*-"

for f in "$@"; do
    enc=$(file -bi "$f" | cut -d = -f 2)
    if [[ $enc != "us-ascii" ]]; then
        dirn=$(dirname "$f")
        basen=$(basename "$f")
        new_dir="${out_dir}/${dirn}"
        if [[ ! -e "$new_dir" ]]; then
            mkdir -p "$new_dir"
        fi
        case "$basen" in
            armscii-8.7 | cp1251.7 | iso_8859-*.7 | koi8-?.7)

	        # iconv does not understand some encoding names that
	    	# start "iso_", but does understand the corresponding
	        # forms that start with "iso-"

                from_enc="$(echo $basen | sed 's/\.7$//;s/iso_/iso-/')"
                ;;
            *)
	        echo "NULL TRANSFORM: $f"
                from_enc=$enc
                ;;
        esac
        printf "Converting %-23s from %s\n" "$f" "$from_enc"
        echo "$enc_line" > "${new_dir}/${basen}"
        iconv -f "$from_enc" -t utf-8 "$f" \
            | sed "/.*-\*- coding:.*/d;/.\\\" t$/d" >> "${new_dir}/${basen}"
    fi
done

exit 0
