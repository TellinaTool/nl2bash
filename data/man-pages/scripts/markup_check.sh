#!/bin/sh

LOG=/tmp/markup_check.$$
rm -f $LOG $LOG.full

if test $# -eq 0; then
    echo 1>&2 "Usage: $0 filename-or-dirname ... $#"
    exit 1
fi

file_list=$(find $* -type f | grep '\.[1-9][a-zA-Z]*$')

pagename_pattern='[a-z_A-Z][^ ]*'

(
    echo ""
    echo "Checking for page xref without space before left parenthesis:"
    pattern='^\.BR  *'"$pagename_pattern"'([1-8][^1-9]'
    echo "    Pattern: '$pattern'"
    grep "$pattern" $file_list | sed 's/^/        /' | tee -a $LOG

    echo ""
    echo "Checking for .IR xrefs that should be .BR"
    pattern='^\.IR  *'"$pagename_pattern"'  *([1-8][^1-9]'
    echo "    Pattern: '$pattern'"
    grep "$pattern" $file_list | sed 's/^/        /' | tee -a $LOG

    echo ""
    echo "Checking for misformatted punctuation in .BR xrefs"
    pattern='^\.BR  *'"$pagename_pattern"'  *([1-8a-zA-Z]*) [^ ]'
    echo "    Pattern: '$pattern'"
    grep "$pattern" $file_list | sed 's/^/        /' | tee -a $LOG

    echo ""
    echo "Checking for .B xrefs that should be .BR"
    pattern='^\.B '"$pagename_pattern"'  *([1-8a-zA-Z]*)'
    echo "    Pattern: '$pattern'"
    grep "$pattern" $file_list | sed 's/^/        /' | tee -a $LOG
) > $LOG.full

if test $(cat $LOG | wc -l) -gt 0; then
    echo ""
    echo "MARKUP ERRORS!!!!!"
    cat $LOG.full
    exit 1
fi

exit 0
