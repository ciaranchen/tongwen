lexer grammar TongWenLexer;

DECLARE                     : '有';
LET_PRE                     : '以';
LET_POST                    : '设';
ASSIGN                      : '为';
NO_MORE                     : '不复';
TYPE_POSTFIX                : '者';

IF                          : '若';
ELSEIF                      : '另若';
ELSE                        : '否则';
FOR                         : '凡';
IN                          : 'in' | '内';
OF                          : 'of' | '中';
WHILE                       : '当';

FUNCTION_DECLARE            : '由';
CALL_PRE_ARG                : '取';
CALL_PRE_IT                 : '之';
CALL_PRE_NUMBER_HINT        : '值';
CALL_MID_BRANCKET           : '·' | '`' ;
CALL_MID_TO                 : '于';
RETURN                      : '得';


STRING_LITERAL              : '"' (' '..'~')* '"' | '“' (~'”')* '”';
TRUE                        : '阳' | ('True');
FALSE                       : '阴' | ('False');

LP                          : '(' | '（';
RP                          : ')' | '）';
LB                          : '{';
RB                          : '}';

INNER_TYPE                  : '数' | '言' | '列' | '图' | '集' | '术';

COMMA                       : ',' | '，';
SEMICOLON                   : ';' | '；';

WS                      : [ \t\r\n]+ -> skip;






IDENTIFIER              : ID_START ID_CONTINUE*;

// TODO: ANTLR seems lack of some Unicode property support...
//$ curl https://www.unicode.org/Public/13.0.0/ucd/PropList.txt | grep Other_ID_
//1885..1886    ; Other_ID_Start # Mn   [2] MONGOLIAN LETTER ALI GALI BALUDA..MONGOLIAN LETTER ALI GALI THREE BALUDA
//2118          ; Other_ID_Start # Sm       SCRIPT CAPITAL P
//212E          ; Other_ID_Start # So       ESTIMATED SYMBOL
//309B..309C    ; Other_ID_Start # Sk   [2] KATAKANA-HIRAGANA VOICED SOUND MARK..KATAKANA-HIRAGANA SEMI-VOICED SOUND MARK
//00B7          ; Other_ID_Continue # Po       MIDDLE DOT
//0387          ; Other_ID_Continue # Po       GREEK ANO TELEIA
//1369..1371    ; Other_ID_Continue # No   [9] ETHIOPIC DIGIT ONE..ETHIOPIC DIGIT NINE
//19DA          ; Other_ID_Continue # No       NEW TAI LUE THAM DIGIT ONE

fragment UNICODE_OIDS
 : '\u1885'..'\u1886'
 | '\u2118'
 | '\u212e'
 | '\u309b'..'\u309c'
 ;

fragment UNICODE_OIDC
 : '\u00b7'
 | '\u0387'
 | '\u1369'..'\u1371'
 | '\u19da'
 ;

/// id_start     ::=  <all characters in general categories Lu, Ll, Lt, Lm, Lo, Nl, the underscore, and characters with the Other_ID_Start property>
fragment ID_START
 : '_'
 | [\p{L}]
 | [\p{Nl}]
 //| [\p{Other_ID_Start}]
 | UNICODE_OIDS
 ;

/// id_continue  ::=  <all characters in id_start, plus characters in the categories Mn, Mc, Nd, Pc and others with the Other_ID_Continue property>
fragment ID_CONTINUE
 : ID_START
 | [\p{Mn}]
 | [\p{Mc}]
 | [\p{Nd}]
 | [\p{Pc}]
 //| [\p{Other_ID_Continue}]
 | UNICODE_OIDC
 ;