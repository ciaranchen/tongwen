from TongWenParserVisitor import TongWenParserVisitor
from TongWenParser import TongWenParser
from TongWenLexer import TongWenLexer
from antlr4 import *
from collections import defaultdict, namedtuple

Variable = namedtuple('variable', ['type', 'value'])


class TongWenParserVisitorInterpreter(TongWenParserVisitor):
    def __init__(self) -> None:
        self.vars = defaultdict(None, **{
            '加': Variable(type='Function', value=lambda x, y: x + y)
        })
        super().__init__()

    def get_id(self, name):
        return None if not self.vars[name] else self.vars[name].value

    def visitProgram(self, ctx: TongWenParser.ProgramContext):
        data = None
        for stmt in ctx.children:
            data = self.visitStatement(stmt)
        return data

    def visitStatement(self, ctx: TongWenParser.StatementContext):
        return self.visitExpr(ctx.expr())

    def visitExpr(self, ctx: TongWenParser.ExprContext):
        if ctx.nature_math_expr():
            return self.visitNature_math_expr(ctx.nature_math_expr())
        if ctx.declare_statement():
            return self.visitDeclare_statement(ctx.declare_statement())
        if ctx.function_call_expr():
            return self.visitFunction_call_expr(ctx.function_call_expr())
        return None

    def visitNature_math_expr(self, ctx: TongWenParser.Nature_math_exprContext):
        operator = ctx.MathOperator().getText()
        print(operator)
        operator_funcs = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
        }
        return operator_funcs[operator](self.visitData(ctx.data(0)), self.visitData(ctx.data(1)))

    def visitData(self, ctx: TongWenParser.DataContext):
        if ctx.NUMBER():
            return float(ctx.getText())
        elif ctx.STRING_LITERAL():
            return ctx.getText()
        elif ctx.IDENTIFIER():
            return self.get_id(ctx.IDENTIFIER().getText())
        # TODO: Id;

    def visitDeclare_statement(self, ctx: TongWenParser.Declare_statementContext):
        ids = ctx.declare_identifier()
        for _id in ids:
            obj_name, obj_value = self.visitDeclare_identifier(_id)
            # save id obj;
            self.vars[obj_name] = obj_value
        return None

    def visitDeclare_identifier(self, ctx: TongWenParser.Declare_identifierContext):
        var_name = ctx.IDENTIFIER().getText()
        value = self.visitData(ctx.data()) if ctx.data() else None
        # TODO: 类型推断。
        _type = self.visitData(ctx.type_()) if ctx.type_() else None
        return var_name, Variable(type=_type, value=value)

    def visitFunction_call_expr(self, ctx: TongWenParser.Function_call_exprContext):
        if ctx.function_call_pre_expr():
            return self.visitFunction_call_pre_expr(ctx.function_call_pre_expr())
        if ctx.function_call_mid_expr():
            return self.visitFunction_call_mid_expr(ctx.function_call_mid_expr())
        if ctx.function_call_post_expr():
            return self.visitFunction_call_post_expr(ctx.function_call_post_expr())
        return None

    def visitFunction_call_mid_expr(self, ctx: TongWenParser.Function_call_pre_exprContext):
        function = ctx.function_name().getText()
        func_var = self.vars[function].value
        data1, data2 = self.visitData(ctx.data(0)), self.visitData(ctx.data(1))
        return func_var(data1, data2)


def main():
    # input_expression = input("> ")
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
