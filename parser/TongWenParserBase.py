from antlr4 import *


class TongWenParserBase(Parser):
    literalNames = []

    def isKeyword(self, text):
        # print(self._ctx)
        print(text)
        if text.startswith("以"):
            self.exitRule()
        return True
