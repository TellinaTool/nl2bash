#!/bin/sh
#
# FIXME_list.sh
#
# Display FIXME segments from man-pages source files
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
######################################################################
#
# (C) Copyright 2006 & 2013, Michael Kerrisk
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

show_all="n"
while getopts "a" optname; do
    case "$optname" in

    a)  # "all"
        # Even show FIXMEs that aren't generally interesting.  (Typically
	# these FIXMEs are notes to the maintainer to reverify something
	# at a future date.)
    
    	show_all="y"    
        ;;
    
    *)  echo "Unknown option: $OPTARG"
	exit 1
	;;

    esac
done

shift $(( $OPTIND - 1 ))

if test $# -eq 0; then
    echo "Usage: $0 [-a] pathname..." 1>&2
    exit 1;
fi

for dir in "$@"; do
    for page in $(find "$dir" -type f -name '*.[1-9]' \
			-exec grep -l FIXME {} \; | sort)
    do
        cat "$page" | awk -v SHOW_ALL=$show_all -v PAGE_NAME="$page" \
	    '
            BEGIN { 
	        page_FIXME_cnt = 0; 
	    }
    	    
	    /FIXME/ { 
    
                # /.\" FIXME . / ==> do not display this FIXME, unless
                # -a command-line option was supplied
	        
		if ($0 ~ /^\.\\\" FIXME \./ )
		    FIXME_type = "hidden"
		else if ($0 ~ /^\.\\\" FIXME *\?/ )
		    FIXME_type = "question"
		else
		    FIXME_type = "normal";
	        if (FIXME_type == "normal" || SHOW_ALL == "y") {
	            if (page_FIXME_cnt == 0) {
		        print "==========";
		        print PAGE_NAME;
	            }
	            page_FIXME_cnt++;
		    
	            finished = 0; 
	            do { 
	                print $0; 
		        
		        # Implicit end of FIXME is end-of-file or a line 
		        # that is not a comment
    
	                if (getline == 0)
		            finished = 1;
    
	                if (!($0 ~ /^.\\\"/)) 
		            finished = 1;
        
                        # /.\" .$/ ==> Explicit end of FIXME
        
	                if ($0 ~ /^.\\\" \.$/) 
		            finished = 1;
	            } while (!finished);
    
	            print "";
                }
    	    }
            '
    done | sed -e 's/^\.\\"/    /' | sed -e 's/ *$//' | cat -s
done
