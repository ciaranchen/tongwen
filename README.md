# 同文

一个中文编程语言。

- 给出一个基础的、可拓展的基于ANTLR的中文编程语法规范。
- 给出一个Python实现的解释器样例。

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