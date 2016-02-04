#!/bin/sh
#
# remove_COLOPHON.sh
#
# Remove the COLOPHON section from the man pages provided as
# command-line arguments.  (This is useful to remove the COLOPHON
# sections from all of the man pages in two different release trees
# in order to do a "diff -ruN" to see the "real" differences between
# the trees.)
#
######################################################################
#
# (C) Copyright 2008 & 2013, Michael Kerrisk
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
for f in "$@"; do
    sed -i '/^\.SH COLOPHON/,$d' "$f"
done
