from TongWenParser import TongWenParser
from TongWenLexer import TongWenLexer
from TongWenParserVisitor import TongWenParserVisitor
from TongWenLanguageBase import TongWenLanguageBase, Variable
from antlr4 import *


class TongWenParserVisitorInterpreter(TongWenParserVisitor, TongWenLanguageBase):
    # Basic Variable
    def get_id(self, name):
        var = self.vars.get(name)
        return var.value if var else None

    # Basic Parser Function
    def visitProgram(self, ctx: TongWenParser.ProgramContext):
        data = None
        for stmt in ctx.children:
            data = self.visitStatement(stmt)
            # print(data)
        return data

    def visitStatement(self, ctx: TongWenParser.StatementContext):
        if ctx.expr():
            return self.visitExpr(ctx.expr())
        if ctx.data():
            return self.visitData(ctx.data())
        if ctx.declare_statement():
            return self.visitDeclare_statement(ctx.declare_statement())

    def visitExpr(self, ctx: TongWenParser.ExprContext):
        if ctx.nature_math_expr():
            return self.visitNature_math_expr(ctx.nature_math_expr())
        if ctx.function_call_expr():
            return self.visitFunction_call_expr(ctx.function_call_expr())
        return None

    def visitP_data(self, ctx: TongWenParser.P_dataContext):
        if ctx.literal():
            return self.visitLiteral(ctx.literal())
        elif ctx.IDENTIFIER():
            return self.get_id(ctx.IDENTIFIER().getText())
        elif ctx.data():
            return self.visitData(ctx.data())
        return None

    def visitData(self, ctx: TongWenParser.DataContext):
        if ctx.literal():
            return self.visitLiteral(ctx.literal())
        elif ctx.IDENTIFIER():
            return self.get_id(ctx.IDENTIFIER().getText())
        elif ctx.p_data():
            return self.visitP_data(ctx.p_data())
        elif ctx.expr():
            return self.visitExpr(ctx.expr())
        return None

    def visitLiteral(self, ctx: TongWenParser.LiteralContext):
        if ctx.NUMBER():
            return float(ctx.getText())
        elif ctx.STRING_LITERAL():
            return ctx.getText()
        elif ctx.BOOL_LITERAL():
            return ctx.BOOL_LITERAL().getText() == "阳"
        return None

    def visitNature_math_expr(self, ctx: TongWenParser.Nature_math_exprContext):
        def get_function(function_name):
            return self.vars.get(function_name).value

        operator = ctx.MathOperator().getText()
        operator_func = {
            '+': get_function('加'),
            '-': get_function('减'),
            '*': get_function('乘'),
            '/': get_function('除'),
        }[operator]
        return operator_func(self.visitData(ctx.p_data(0)), self.visitData(ctx.p_data(1)))

    def visitDeclare_statement(self, ctx: TongWenParser.Declare_statementContext):
        ids = ctx.declare_left_statement()
        for _id in ids:
            obj_name, obj_value = self.visitDeclare_left_statement(_id)
            # save id obj;
            self.vars[obj_name] = obj_value
        return None

    def visitDeclare_left_statement(self, ctx: TongWenParser.Declare_left_statementContext):
        var_name = ctx.IDENTIFIER().getText()
        value = self.visitData(ctx.data()) if ctx.data() else None
        # TODO: 类型推断。
        _type = self.visitData(ctx.type_()) if ctx.type_() else None
        return var_name, Variable(type=_type, value=value)

    def visitFunction_define_expr(self, ctx: TongWenParser.Function_define_exprContext):
        pass

    def visitFunction_call_expr(self, ctx: TongWenParser.Function_call_exprContext):
        if ctx.function_call_pre_expr():
            return self.visitFunction_call_pre_expr(ctx.function_call_pre_expr())
        if ctx.function_call_mid_expr():
            return self.visitFunction_call_mid_expr(ctx.function_call_mid_expr())
        if ctx.function_call_post_expr():
            return self.visitFunction_call_post_expr(ctx.function_call_post_expr())
        return None

    def visitFunction_call_pre_expr(self, ctx: TongWenParser.Function_call_pre_exprContext):
        function = ctx.function_name().getText()
        func_var = self.vars.get(function, None).value
        all_data = ctx.data()
        values = [self.visitData(data) for data in all_data]
        return func_var(*values)

    def visitFunction_call_mid_expr(self, ctx: TongWenParser.Function_call_pre_exprContext):
        function = ctx.function_name().getText()
        func_var = self.vars.get(function, None).value
        data1, data2 = self.visitData(ctx.data(0)), self.visitData(ctx.data(1))
        return func_var(data1, data2)

    def visitFunction_call_post_expr(self, ctx: TongWenParser.Function_call_post_exprContext):
        function = ctx.function_name().getText()
        func_var = self.vars.get(function, None).value
        all_data = ctx.data()
        values = [self.visitData(data) for data in all_data]
        return func_var(*values)


def main():
    # input_expression = input("> ")
    # with open('../书同文.同文', encoding='utf-8') as fp:
    #     input_expression = fp.read()
    input_expression = "有 3 为 乙, 4 为 甲；其 甲 加 于 乙；"
    input_stream = InputStream(input_expression)
    lexer = TongWenLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = TongWenParser(tokens)
    tree = parser.program()
    print(tree.toStringTree(recog=parser))

    visitor = TongWenParserVisitorInterpreter()
    result = visitor.visit(tree)
    print(result)


if __name__ == '__main__':
    main()
