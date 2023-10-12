grammar wenyan;
program                     : statement* ;
statement                   : declare_statement
                            | define_statement
                            | print_statement 
                            | for_statement
                            | function_statement
                            | if_statement
                            | return_statement
                            | math_statement
                            | assign_statement
                            | import_statement
                            | object_statement
                            | reference_statement
                            | array_statement
                            | flush_statement 
                            | BREAK
                            | comment;

reference_statement         : '��' data ('֮' (STRING_LITERAL|INT_NUM|'���N'|IDENTIFIER|'�L'))? name_single_statement? ;


array_statement             : array_cat_statement|array_push_statement ;
array_cat_statement         : '�' (IDENTIFIER|'��') (PREPOSITION_RIGHT IDENTIFIER)+ name_single_statement?;
array_push_statement        : '��' (IDENTIFIER|'��') (PREPOSITION_RIGHT data)+ name_single_statement?;


function_statement          : function_define_statement|(function_call_statement (name_single_statement)?) ;
function_call_statement     : function_pre_call|function_post_call ;
function_pre_call           : ('ʩ' IDENTIFIER (preposition data)*)|('ʩ��' (preposition data)*) ;
function_post_call          : ('ȡ' INT_NUM '��ʩ' IDENTIFIER)+ ;
function_define_statement   : '����' INT_NUM '�g' name_single_statement ('�������g' '���ȵ�' (INT_NUM TYPE ('Ի' IDENTIFIER)+)+)? ('���gԻ'|'�������gԻ') statement* '���^' IDENTIFIER '֮�gҲ' ;


if_statement                : IF if_expression '��' statement+ (ELSE statement+)? FOR_IF_END ;
if_expression               : unary_if_expression|binary_if_expression ;
unary_if_expression         : data|(IDENTIFIER '֮'('�L'|STRING_LITERAL|IDENTIFIER))|'��' ;
binary_if_expression        : unary_if_expression IF_LOGIC_OP unary_if_expression ;


declare_statement           : ('����'|'����') INT_NUM TYPE ('Ի' data)*;
define_statement            : (declare_statement name_multi_statement)|init_define_statement ;


name_multi_statement        : '��֮' ('Ի' IDENTIFIER)+ ;
name_single_statement       : '��֮' ('Ի' IDENTIFIER) ;
init_define_statement       : '��' TYPE data (name_single_statement)? ;


for_statement               : for_arr_statement
                            | for_enum_statement
                            | for_while_statement ;
for_arr_statement           : FOR_START_ARR   IDENTIFIER            FOR_MID_ARR  IDENTIFIER statement* FOR_IF_END ; 
for_enum_statement          : FOR_START_ENUM  (INT_NUM|IDENTIFIER)  FOR_MID_ENUM statement* FOR_IF_END ;
for_while_statement         : FOR_START_WHILE statement*            FOR_IF_END ;


math_statement              : (arith_math_statement|boolean_algebra_statement|mod_math_statement) (name_multi_statement)? ;
arith_math_statement        : arith_binary_math|arith_unary_math ;
arith_binary_math           : ARITH_BINARY_OP (data|'��') preposition (data|'��') ;
arith_unary_math            : UNARY_OP (IDENTIFIER|'��') ;
mod_math_statement          : '��' (INT_NUM|FLOAT_NUM|IDENTIFIER|'��') preposition (INT_NUM|FLOAT_NUM|IDENTIFIER) POST_MOD_MATH_OP? ;
boolean_algebra_statement   : '��' IDENTIFIER IDENTIFIER LOGIC_BINARY_OP ;


assign_statement            : '��֮' IDENTIFIER ('֮' (INT_NUM|STRING_LITERAL|IDENTIFIER))? '��' (('��' ((data ('֮' INT_NUM)?)|'��') '����')|'�񲻏ʹ���') ;


return_statement            : '�˵�' (data|'��')|'�˚w�՟o'|'�˵���' ;


import_statement            : '��L�^' STRING_LITERAL '֮��' ('����' IDENTIFIER+ '֮�x')? ;


object_statement            : '����' INT_NUM '��' name_multi_statement (object_define_statement)? ;
object_define_statement     : '��������' ('��֮' STRING_LITERAL '��' TYPE 'Ի' data)+ '���^' IDENTIFIER '֮��Ҳ' ;


data                        : STRING_LITERAL|BOOL_VALUE|IDENTIFIER|INT_NUM|FLOAT_NUM ;

STRING_LITERAL              : '����' ( ~('��') )* '����' ;
IDENTIFIER                  : '��' ( ~('��') )+ '��' ;

ARITH_BINARY_OP             : '��'|'�p'|'��' ;
LOGIC_BINARY_OP             : '����ꖺ�'|'�Пoꎺ�' ;
POST_MOD_MATH_OP            : '���N�׺�' ;
UNARY_OP                    : '׃' ;

preposition                 : PREPOSITION_LEFT|PREPOSITION_RIGHT ;
PREPOSITION_LEFT            : '�' ;
PREPOSITION_RIGHT           : '��' ;

IF                          : '��' ;
ELSE                        : '����' ;
IF_LOGIC_OP                 : '���'|'�����'|'�����'|'��С�'|'���'|'С�' ;

FOR_START_ARR               : '��' ;
FOR_START_ENUM              : '����' ;
FOR_START_WHILE             : '�a����' ;
FOR_MID_ARR                 : '��֮' ;
FOR_MID_ENUM                : '��' ;
FOR_IF_END                  : '����'|'Ҳ' ;

FLOAT_NUM                   : INT_NUM '��' (INT_NUM FLOAT_NUM_KEYWORDS)+ ;
FLOAT_NUM_KEYWORDS          : '��'|'�'|'��'|'�z'|'��'|'΢'|'�m'|'��'|'��'|'Į' ;
INT_NUM                     : INT_NUM_KEYWORDS+ ;

INT_NUM_KEYWORDS            : '��'|'һ'|'��'|'��'|'��'|'��'|'��'|'��'|'��'|'��'|'ʮ'|'��'|'ǧ'|'�f'|'�|'|'��'|'��'|'��'|'��'|'�y'|'��'|'��'|'��'|'�d'|'�O' ;
TYPE                        : '��'|'��'|'��'|'س' ;
BOOL_VALUE                  : '�'|'�' ;
print_statement             : '��֮' ;

WS                          : ([ \t\r\n]|'��'|'��')+ -> skip ;
comment                     : ('עԻ'|'��Ի'|'��Ի') STRING_LITERAL ;
flush_statement             : '��' ;

BREAK                       : '��ֹ' ;
