grammar tongwen;
program                     : statement* ;
statement                   : declare_statement
                            | assign_statement
                            | delete_assign_statement
                            | for_statement
                            | body_statement

condition_statement         : LP data RP;
body_statement              : LB statement+ RB;

declare_statement           : '有' (TYPE '者')? (data '为')? IDENTIFIER)+;
assign_statement            : '以' (data '为' IDENTIFIER)+;
delete_assign_statement     : IDENTIFIER '不复也';

for_statement: for_arr_statement | for_while_statement;
for_arr_statement           : '凡' loop_condition_statement body_statement;
loop_condition_statement    : LP data (('中'|'内') '为' IDENTIFIER)? RB;
for_while_statement         : '当' condition_statement body_statement;


LP                          : '(' | '（';
RP                          : ')' | '）';
LB                          : '{';
RB                          : '}';

true                        : '阳' | 'True';
false                       : '阴' | 'False';
