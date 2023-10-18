from antlr4 import *


class TongWenParserBase(Lexer):
    literalNames = []

    def isKeyword(self, text):
        # print(self._ctx)
        print(text)
        if text.startswith("以"):
            return False
        return True
