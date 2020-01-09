import enum

parser = enum.Enum('parserflags', [
    'CASEPAT', # in a case pattern list
    'ALEXPNEXT', # expand next word for aliases
    'ALLOWOPNBRC', # allow open brace for function def
    'NEEDCLOSBRC', # need close brace
    'DBLPAREN', # double-paren parsing
    'SUBSHELL', # ( ... ) subshell
    'CMDSUBST', # $( ... ) command substitution
    'CASESTMT', # parsing a case statement
    'CONDCMD', # parsing a [[...]] command
    'CONDEXPR', # parsing the guts of [[...]]
    'ARITHFOR', # parsing an arithmetic for command - unused
    'ALEXPAND', # OK to expand aliases - unused
    'EXTPAT', # parsing an extended shell pattern
    'COMPASSIGN', # parsing x=(...) compound assignment
    'ASSIGNOK', # assignment statement ok in this context
    'EOFTOKEN', # yylex checks against shell_eof_token
    'REGEXP', # parsing an ERE/BRE as a single word
    'HEREDOC', # reading body of here-document
    'REPARSE', # re-parsing in parse_string_to_word_list
    'REDIRLIST', # parsing a list of redirections preceding a simple command name
    ])

word = enum.Enum('wordflags', [
    'QUOTED', # Some form of quote character is present
    'DQUOTE', # word should be treated as if double-quoted
    'HASQUOTEDNULL', # word contains a quoted null character

    'SPLITSPACE', # Split this word on " " regardless of IFS
    'NOSPLIT', # Do not perform word splitting on this word because ifs is empty string
    'NOSPLIT2', # Don't split word except for $@ expansion (using spaces) because context does not allow it

    'TILDEEXP', # Tilde expand this assignment word
    'ITILDE', # Internal flag for word expansion

    'HASDOLLAR', # Dollar sign present
    'DOLLARAT', # $@ and its special handling
    'DOLLARSTAR', # $* and its special handling

    'NOCOMSUB', # Don't perform command substitution on this word
    'NOPROCSUB', # don't perform process substitution

    'NOTILDE', # Don't perform tilde expansion on this word
    'NOEXPAND', # Don't expand at all -- do quote removal
    'NOBRACE', # Don't perform brace expansion
    'NOGLOB', # Do not perform globbing on this word

    'ASSIGNMENT', # This word is a variable assignment
    'ASSNBLTIN', # word is a builtin command that takes assignments
    'ASSIGNRHS', # Word is rhs of an assignment statement
    'ASSIGNARG', # word is assignment argument to command
    'ASSIGNASSOC', # word looks like associative array assignment
    'ASSIGNARRAY', # word looks like a compound indexed array assignment
    'ASSNGLOBAL', # word is a global assignment to declare (declare/typeset -g)
    'ASSIGNINT', # word is an integer assignment to declare
    'COMPASSIGN', # Compound assignment

    'HASCTLESC', # word contains literal CTLESC characters
    'ARRAYIND', # word is an array index being expanded
    ])
