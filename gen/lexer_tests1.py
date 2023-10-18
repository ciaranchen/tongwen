from antlr4 import *
from ChineseProgrammingLanguageLexer import ChineseProgrammingLanguageLexer
from ChineseProgrammingLanguageParser import ChineseProgrammingLanguageParser


if __name__ == '__main__':
    lexer = ChineseProgrammingLanguageLexer(InputStream('中加中'))
    parser = ChineseProgrammingLanguageParser(CommonTokenStream(lexer))
    parse_tree = parser.expr()
    print(parse_tree.toStringTree(recog=parser))
