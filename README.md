# 同文

一个中文编程语言。

- 给出一个基础的、可拓展的基于ANTLR的中文编程语法规范。
- 给出一个Python实现的解释器样例。

其中`书同文.同文` 是一个语法示例文件。

## 如何使用

```shell
# 生成Lexer Parser 和 Visitor
pip install antlr4-tools
antlr4 -o parser -visitor -encoding UTF-8 -Dlanguage=Python3 -lib . ./TongWenParser.g4 ./TongWenLexer.g4
```

```commandline
pip install -r requirements.txt
python parser/TongWenInterpreter.py
```

## 语法对照表

中文编程项目当前做得最突出最有特色的非[文言lang](https://github.com/wenyan-lang/wenyan)莫属。文言lang提供了其语言规范文件，其中statement部分的表述如下，我打算在它的基础上进行拓展。

```g4
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
```

我希望实现的同文语言在语法上应该相比文言lang有以下特点：

1. 关键字的字数尽量少一些，表意清楚即可。

2. 不使用中英文切换，即尽可能使用中文符号。

接下来将列出我预想的实现方式和文言的句法之间的对比。

| Statement                     | 文言g4                                                                                                                                                                                                             | 文言语法                                                       | TypeScript                                | 新语法                                                        |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | ----------------------------------------- | ---------------------------------------------------------- |
| declare_statement             | `('吾有'\|'今有') INT_NUM TYPE ('曰' data)*;`                                                                                                                                                                         | `吾有一數。`<br />`今有一數曰三。`                                     |                                           |                                                            |
| define_statement              | `(declare_statement name_multi_statement)\| '有' TYPE data (name_single_statement)?;`                                                                                                                             | `吾有一數曰三。名之曰「甲」`<br />`有數三名之曰「甲」`                           | `let a = 3;`                              | `有数者3名甲；`<br />`有以3名甲；`<br />`有数者名甲；`<br />`有名甲；`          |
| assign_statement              | `'昔之' IDENTIFIER ('之' (INT_NUM\|STRING_LITERAL\|IDENTIFIER))? '者' (('今' ((data ('之' INT_NUM)?)\|'其') '是矣')\|'今不復存矣') ;`                                                                                          | `昔之「甲」者。今「大衍」是矣。`                                          | `a = dayan;`                              | `以 大衍 为 甲；`<br />`甲 不复；`                                   |
| print_statement               | `'書之'`                                                                                                                                                                                                           | `書之`                                                       | `console.log`                             | `输出` （未实现）                                                 |
| if_statement                  | `IF if_expression '者' statement+ (ELSE statement+)? FOR_IF_END ;`                                                                                                                                                | `若三大於二者。乃得「「想當然耳」」也。`                                      | `if (3>2){ return "of course"; }`         | `若 （夫 3 大于 2） {得 “确实”；}`                                   |
| for_arr_statement             | `FOR_START_ARR   IDENTIFIER            FOR_MID_ARR  IDENTIFIER statement* FOR_IF_END ;`                                                                                                                          | `凡「天地」中之「人」。⋯⋯ 云云。`                                        | `for (var human of world){ ... }`         | `凡（天地 中为 人）{...}`                                          |
| for_enum_statement            | `FOR_START_ENUM (INT_NUM\|IDENTIFIER) FOR_MID_ENUM statement* FOR_IF_END ; `                                                                                                                                     | `為是百遍。⋯⋯ 云云。`                                              | `for (var i = 0; i < 100; i++){ ... }`    | `凡（1至100 中为 甲）{...}`（未实现）                                  |
| for_while_statement           | `FOR_START_WHILE statement* FOR_IF_END ;`                                                                                                                                                                        | `恆為是。⋯⋯ 云云。`                                               | `while (true) { ... }`                    | `当 （阳） {...} `                                             |
| function_define_statement     | `'吾有' INT_NUM '術' name_single_statement ('欲行是術' '必先得' (INT_NUM TYPE ('曰' IDENTIFIER)+)+)? ('是術曰'\|'乃行是術曰') statement* '是謂' IDENTIFIER '之術也' ;`                                                                   | `吾有一術。名之曰「甲」。欲行是術。必先得一數曰「乙」。二言。曰「丙」。曰「丁」`                  | `function a(float b, string c, string d)` | `由（数 类 谓 乙，言 类 谓 丙）求 数 {得 乙；}`<br/>（实现了部分lambda语法，函数定义未实现） |
| function_pre_call_statement   | `('施' IDENTIFIER (preposition data)*)\|('施其' (preposition data)*) ;`                                                                                                                                             | `施「翻倍」於「大衍」。`                                              | `double(dayan);`                          | `倍（大衍）；`                                                   |
| function_post_call            | `('取' INT_NUM '以施' IDENTIFIER)+ ;`                                                                                                                                                                               | `夫「甲」。夫「乙」。取二以施「丙」。`                                       | `c(b,a)`                                  | `使 甲、乙 求和 之。`<br />`使 甲、乙、丙 二者 求和；`（"者" 未实现）               |
| function_mid_call             | -                                                                                                                                                                                                                | -                                                          | `a `add` b`(Haskell)                      | `夫 甲 加 于 乙；`                                               |
| return_statement              | `return_statement            : '乃得' (data\|'其')\|'乃歸空無'\|'乃得矣' ;`                                                                                                                                                | `乃得「乙」。`                                                   | `return b;`                               | `得 乙；`<br />`得 空；`<br />`丙。`（句号语法糖未实现）                     |
| object_statement              | `object_statement            : '吾有' INT_NUM '物' name_multi_statement (object_define_statement)? ;` <br />`object_define_statement     : '其物如是' ('物之' STRING_LITERAL '者' TYPE '曰' data)+ '是謂' IDENTIFIER '之物也' ;` | `吾有一物。名之曰「甲」。其物如是。物之「「乙」」者。數曰三。物之「「丙」」者。言曰「「丁」」。是謂「甲」之物也。` | `var a = {b:3, c:"d"}`                    | `合 甲 有{数类3名乙，“丁”名丙}。`                                      |
| DOT_expr（reference_statement） | `'夫' data ('之' (STRING_LITERAL\|INT_NUM\|'其餘'\|IDENTIFIER\|'長'))? name_single_statement? ;`                                                                                                                      |                                                            |                                           | `甲 之 乙`                                                    |
| COMMENT                       | `('注曰'\|'疏曰'\|'批曰') STRING_LITERAL ;`                                                                                                                                                                            |                                                            |                                           | `# 注释`                                                     |
| import_statement              |                                                                                                                                                                                                                  |                                                            |                                           | （未实现）                                                      |

## TODO

1. 补全上面未实现的语法

2. 实现面向对象的语法

3. 去除语法间的空格

4. 基于LLVM实现编译器或解释器
