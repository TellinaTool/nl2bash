grammar Commands;

command : mv;

mv : 'mv' mv_options path path
    | 'mv' mv_options path+ path;

mv_options : (mv_op1)* (mv_op2)*;

mv_op1 : '-f' | '-c' | '-n';
mv_op2 : '-v';

path : STRING;

STRING : ( 'a' .. 'z' | 'A' .. 'Z' | '0' .. '9' | '.' | '_' | '/' ) * ;

WS : [ \t\n\r] + -> skip;