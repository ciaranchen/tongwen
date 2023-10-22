import ast
from collections import namedtuple, defaultdict
from typing import List

from TongWenParser import TongWenParser
from TongWenParserVisitor import TongWenParserVisitor

Variable = namedtuple('variable', ['type', 'value'])
FunctionArg = namedtuple('FunctionArg', ['name', 'type', 'value'])


class TongWenDataVisitor(TongWenParserVisitor):

    def visitP_data(self, ctx: TongWenParser.P_dataContext):
        if ctx.literal():
            return self.get_literal(ctx.literal())
        elif ctx.IDENTIFIER():
            return self.get_id(ctx.IDENTIFIER().getText())
        elif ctx.data():
            return self.visitData(ctx.data())
        return None

    def visitData(self, ctx: TongWenParser.DataContext):
        if ctx.literal():
            return self.get_literal(ctx.literal())
        elif ctx.IDENTIFIER():
            return self.get_id(ctx.IDENTIFIER().getText())
        elif ctx.p_data():
            return self.visitP_data(ctx.p_data())
        elif ctx.expr():
            return self.visitExpr(ctx.expr())
        return None

    def get_literal(self, param):
        raise NotImplementedError

    def get_id(self, param):
        raise NotImplementedError


class TongWenLanguageBase:
    def __init__(self) -> None:
        base_math_funcs = {
            '加': Variable(type='PrimitiveFunction', value=lambda x, y: x + y),
            '减': Variable(type='PrimitiveFunction', value=lambda x, y: x - y),
            '乘': Variable(type='PrimitiveFunction', value=lambda x, y: x * y),
            '除': Variable(type='PrimitiveFunction', value=lambda x, y: x / y),
            '求和': Variable(type='PrimitiveFunction', value=lambda *x: sum(x)),
        }
        base_logic_funcs = {
            '非': Variable(type='PrimitiveFunction', value=lambda x: not x),
            '或': Variable(type='PrimitiveFunction', value=lambda x, y: x or y),
            '且': Variable(type='PrimitiveFunction', value=lambda x, y: x and y),
        }
        base_comp_funcs = {
            '等': Variable(type='PrimitiveFunction', value=lambda x, y: x == y),
            '同': Variable(type='PrimitiveFunction', value=lambda x, y: x is y),
            '大': Variable(type='PrimitiveFunction', value=lambda x, y: x > y),
            '小': Variable(type='PrimitiveFunction', value=lambda x, y: x < y),
            '大或等': Variable(type='PrimitiveFunction', value=lambda x, y: x >= y),
            '小或等': Variable(type='PrimitiveFunction', value=lambda x, y: x <= y),
        }
        self.vars = defaultdict(None, **base_math_funcs, **base_logic_funcs, **base_comp_funcs)

    def get_id(self, name):
        var = self.vars.get(name)
        return var.value if var else None

    @staticmethod
    def get_literal(ctx: TongWenParser.LiteralContext):
        if ctx.NUMBER():
            return float(ctx.getText())
        elif ctx.STRING_LITERAL():
            return ctx.getText()
        elif ctx.BOOL_LITERAL():
            return ctx.BOOL_LITERAL().getText() == "阳"
        return None

    def function_call(self, function, args):
        return


class TongWenLambdaVisitor(TongWenDataVisitor):
    def __init__(self, args: List[FunctionArg]) -> None:
        super().__init__()
        self.args = args

    def get_literal(self, ctx: TongWenParser.LiteralContext):
        if ctx.NUMBER():
            return ast.Num(n=float(ctx.NUMBER().getText()))
        elif ctx.STRING_LITERAL():
            return ast.Str(s=ctx.STRING_LITERAL().getText)
        elif ctx.BOOL_LITERAL():
            return ast.NameConstant(value=ctx.BOOL_LITERAL().getText() == "阳")
        return None

    def get_id(self, var_name):
        return ast.Call(func=ast.Attribute(ast.Name(id='_context'), 'get'), args=[ast.Str(s=var_name)])

    def visitProgram(self, ctx: TongWenParser.ProgramContext):
        stmts = [self.visitStatement(stmt) for stmt in ctx.children]
        return stmts

    def visitStatement(self, ctx: TongWenParser.StatementContext):
        if ctx.function_return_statement():
            return self.visitFunction_return_statement(ctx.function_return_statement())

    def visitFunction_return_statement(self, ctx: TongWenParser.Function_return_statementContext):
        return_value = self.visitData(ctx.data()) if ctx.data() else None
        return ast.Return(return_value)
