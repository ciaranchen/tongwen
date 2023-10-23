parser grammar TongWenParser;
options {
    tokenVocab  = TongWenLexer;
    language    = Python3;
    superClass  = TongWenParserBase;
}


program                     : statement* ;
statement                   : (expr SEMICOLON)
                            | (data SEMICOLON)
                            | declare_statement
                            | assign_statement
                            | if_statement
                            | for_statement
                            | body_statement
                            | function_return_statement
                            | struct_define_expr;

expr                        : nature_math_expr
                            | lambda_expr
                            | function_call_expr
                            | dot_expr;


condition_statement         : LP data RP;
body_statement              : LB program RB;


declare_statement           : CONST? DECLARE declare_left_statement (COMMA declare_left_statement)*? SEMICOLON;
declare_left_statement      : (type TYPE_POSTFIX)? (data)? DECLARE_ASSIGN IDENTIFIER;
assign_statement            : (assign_pre_statement | assign_post_statement | delete_assign_statement)  SEMICOLON;
assign_pre_statement        : ASSIGN_PRE assign_left_statement (COMMA assign_left_statement)*?;
assign_post_statement       : ASSIGN_POST assign_right_statement (COMMA assign_right_statement)*?;
delete_assign_statement     : IDENTIFIER NO_MORE;
assign_left_statement       : (type TYPE_POSTFIX)? (data) ASSIGN IDENTIFIER;
assign_right_statement      : IDENTIFIER ASSIGN (type TYPE_POSTFIX)? (data);


if_statement                : IF condition_statement body_statement (ELSEIF condition_statement body_statement)? (ELSE body_statement)?;

for_statement               : for_arr_statement | for_while_statement;
for_arr_statement           : FOR loop_condition_statement body_statement;
loop_condition_statement    : LP data ((IN|OF) ASSIGN IDENTIFIER)? RP;
for_while_statement         : WHILE condition_statement body_statement;

arg_assignment              : (type TYPE_POSTFIX)? (data)? FUNCTION_ARG_ASSIGN IDENTIFIER;
lambda_expr                 : LAMBDA_DECLARE LP ((arg_assignment COMMA)* arg_assignment)? RP (FUNCTION_RET_HINT type)? body_statement;
function_call_expr          : function_call_pre_expr | function_call_mid_expr | function_call_post_expr;
function_call_pre_expr      : CALL_PRE_ARG (data COMMA)* data (INT_PRE_KEYWORDS CALL_PRE_NUMBER_HINT)? function_name;
function_call_mid_expr      : CALL_MID_ARG data function_name CALL_MID_TO (data | (LP ((data COMMA)* data)? RP));
function_call_post_expr     : function_name LP ((data COMMA)* data)? RP;
nature_math_expr            : p_data MathOperator p_data;
function_return_statement   : RETURN data SEMICOLON;

struct_define_expr          : STRUCT_DECLARE LB ((type TYPE_POSTFIX)? ((data | expr) ASSIGN)? IDENTIFIER COMMA?)*? RB ASSIGN IDENTIFIER;
dot_expr                    : p_data DOT IDENTIFIER;

literal                     : STRING_LITERAL | NUMBER | IDENTIFIER | BOOL_LITERAL;
p_data                      : IDENTIFIER | literal | LP data RP; // P_data 指在该位置的值若包含表达式应有括号
data                        : IDENTIFIER | literal | p_data | expr;
type                        : INNER_TYPE | IDENTIFIER;
function_name               : MathFunction | IDENTIFIER | p_data;
