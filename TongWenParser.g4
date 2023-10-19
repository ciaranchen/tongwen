parser grammar TongWenParser;
options {
    tokenVocab  = TongWenLexer;
    language    = Python3;
    superClass  = TongWenParserBase;
}


program                     : statement* ;
statement                   : (expr SEMICOLON)
                            | if_statement
                            | for_statement
                            | body_statement
                            | struct_define_expr;

expr                        : nature_math_expr
                            | declare_statement
                            | assign_statement
                            | function_define_expr
                            | function_call_expr
                            | function_return_statement
                            | dot_expr
                            | data;


wrapped_expr                : LP expr RP;
condition_statement         : LP data | expr RP;
body_statement              : LB program RB;


declare_statement           : DECLARE declare_identifier (COMMA declare_identifier)*?;
declare_identifier          : (type TYPE_POSTFIX)? ((data | expr) ASSIGN)? IDENTIFIER;
assign_statement            : assign_pre_statement | assign_post_statement | delete_assign_statement;
assign_pre_statement        : LET_PRE (data ASSIGN identifier)+;
assign_post_statement       : LET_POST (identifier ASSIGN data)+;
delete_assign_statement     : identifier NO_MORE;

if_statement                : IF condition_statement body_statement (ELSEIF condition_statement body_statement)? (ELSE body_statement)?;

for_statement               : for_arr_statement | for_while_statement;
for_arr_statement           : FOR loop_condition_statement body_statement;
loop_condition_statement    : LP data ((IN|OF) ASSIGN IDENTIFIER)? RP;
for_while_statement         : WHILE condition_statement body_statement;

i_assign_expr                : (type TYPE_POSTFIX)? (data ASSIGN)? IDENTIFIER;

function_define_expr        : FUNCTION_DECLARE LP ((i_assign_expr COMMA)* i_assign_expr)? RP (FUNCTION_RET_HINT type)? body_statement;
function_call_expr          : function_call_pre_expr | function_call_mid_expr | function_call_post_expr;
function_call_pre_expr      : CALL_PRE_ARG (data COMMA)* data (INT_PRE_KEYWORDS CALL_PRE_NUMBER_HINT)? function_name;
function_call_mid_expr      : CALL_MID_ARG data function_name CALL_MID_TO (data | (LP ((data COMMA)* data)? RP));
function_call_post_expr     : function_name LP ((data COMMA)* data)? RP;
nature_math_expr            : data MathOperator data;
function_return_statement   : RETURN data;

struct_define_expr          : STRUCT_DECLARE LB ((type TYPE_POSTFIX)? ((data | expr) ASSIGN)? IDENTIFIER COMMA?)*? RB ASSIGN IDENTIFIER;
dot_expr                    : data DOT identifier;

data                        : STRING_LITERAL | NUMBER | wrapped_expr | IDENTIFIER | BOOL_LITERAL | LP data RP;
type                        : INNER_TYPE | IDENTIFIER;
function_name               : MathFunction | IDENTIFIER;

identifier                  : IDENTIFIER;

