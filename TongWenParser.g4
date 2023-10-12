parser grammar TongWenParser;
options { tokenVocab=TongWenLexer; }


program                     : statement* ;
statement                   : (expr SEMICOLON)
                            | if_statement
                            | for_statement;

expr                        : declare_statement
                            | assign_statement
                            | body_statement
                            | function_define_expr
                            | function_call_expr
                            | function_return_statement;


condition_statement         : LP data RP;
body_statement              : LB program RB;


declare_statement           : DECLARE ((type TYPE_POSTFIX)? (data ASSIGN)? IDENTIFIER)+;
assign_statement            : assign_pre_statement | assign_post_statement | delete_assign_statement;
assign_pre_statement        : LET_PRE (data ASSIGN IDENTIFIER)+;
assign_post_statement       : LET_POST (IDENTIFIER ASSIGN data)+;
delete_assign_statement     : IDENTIFIER NO_MORE;

if_statement                : IF condition_statement body_statement (ELSEIF condition_statement body_statement)? (ELSE body_statement)?;

for_statement               : for_arr_statement | for_while_statement;
for_arr_statement           : FOR loop_condition_statement body_statement;
loop_condition_statement    : LP data ((IN|OF) ASSIGN IDENTIFIER)? RP;
for_while_statement         : WHILE condition_statement body_statement;

i_assign_expr                : (type TYPE_POSTFIX)? (data ASSIGN)? IDENTIFIER;

function_define_expr        : FUNCTION_DECLARE LP ((i_assign_expr COMMA)* i_assign_expr)? RP body_statement;
function_call_expr          : function_call_pre_expr | function_call_mid_expr | function_call_post_expr;
function_call_pre_expr      : CALL_PRE_ARG (data COMMA)* data (NUMBER CALL_PRE_NUMBER_HINT)? function_name CALL_PRE_IT;
function_call_mid_expr      : CALL_MID_BRANCKET data function_name CALL_MID_TO data;
function_call_post_expr     : function_name LP ((data COMMA)* data)? RP;
function_return_statement   : RETURN data;


data                        : STRING_LITERAL | IDENTIFIER | expr;
type                        : INNER_TYPE | IDENTIFIER;
function_name               : IDENTIFIER;