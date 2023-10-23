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


class TongWenLanguageBase(TongWenDataVisitor):
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

        def primitive_func_decorator(func):
            return lambda ctx, *x: func(*x)

        def map_decorator(funcs):
            return {k: Variable(type=v.type, value=primitive_func_decorator(v.value)) for k, v in funcs.items()}

        self.vars = defaultdict(None,
                                **map_decorator(base_math_funcs),
                                **map_decorator(base_logic_funcs),
                                **map_decorator(base_comp_funcs))

    def get_id(self, name):
        var = self.vars.get(name)
        return var.value if var else None

    def get_literal(self, ctx: TongWenParser.LiteralContext):
        if ctx.NUMBER():
            return float(ctx.getText())
        elif ctx.STRING_LITERAL():
            return ctx.getText()
        elif ctx.BOOL_LITERAL():
            return ctx.BOOL_LITERAL().getText() == "阳"
        return None

    def function_call(self, function, *args):
        result = function(self.vars, *args)
        return result


class TongWenLambdaVisitor(TongWenDataVisitor):
    def __init__(self, args: List[FunctionArg]) -> None:
        super().__init__()
        self.func_nums = 0
        self._inner_funcs = []
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
        if var_name in [a.name for a in self.args]:
            return ast.Name(id=var_name, ctx=ast.Load())
        return ast.Attribute( # _context.get(var_name).value
            value=ast.Call(
                func=ast.Attribute(
                    ast.Name(id='_context', ctx=ast.Load()), attr='get', ctx=ast.Load(), lineno=1),
                args=[ast.Str(s=var_name, lineno=1)], keywords=[]),
            attr='value', ctx=ast.Load()
        )

    def function_call(self, func_var, *param):
        return ast.Call(func=func_var,
                        args=[ast.Name(id='_context', ctx=ast.Load()), *param],
                        keywords=[], lineno=1)

    def visitProgram(self, ctx: TongWenParser.ProgramContext):
        res = []
        for child in ctx.children:
            stmt = self.visitStatement(child)
            if len(self._inner_funcs) != 0:
                res += self._inner_funcs
                self.func_nums += len(self._inner_funcs)
                self._inner_funcs.clear()
            res.append(stmt)
        return res

    def visitStatement(self, ctx: TongWenParser.StatementContext):
        if ctx.function_return_statement():
            return self.visitFunction_return_statement(ctx.function_return_statement())
        if ctx.expr():
            return self.visitExpr(ctx.expr())
        if ctx.data():
            return self.visitData(ctx.data())
        return None

    def visitExpr(self, ctx: TongWenParser.ExprContext):
        if ctx.function_call_expr():
            return self.visitFunction_call_expr(ctx.function_call_expr())
        if ctx.lambda_expr():
            return self.visitLambda_expr(ctx.lambda_expr())
        return None

    def visitFunction_return_statement(self, ctx: TongWenParser.Function_return_statementContext):
        return_value = self.visitData(ctx.data()) if ctx.data() else None
        return ast.Return(value=return_value, lineno=1)

    def visitLambda_expr(self, ctx: TongWenParser.Lambda_exprContext):
        args = ctx.arg_assignment()
        args_define = [self.visitArg_assignment(arg) for arg in args]
        # 加上此FuncDefine中的args
        lambda_parser = TongWenLambdaVisitor(args_define + self.args)
        body_stmt = lambda_parser.visitProgram(ctx.body_statement().program())

        inner_func_name = f'_lambda_{self.func_nums + len(self._inner_funcs)}'
        func = ast.FunctionDef(
            name=inner_func_name,
            args=ast.arguments(
                args=[
                    ast.arg(arg='_context', annotation=None),
                    *[ast.arg(arg=arg.name, annotation=None) for arg in args_define]
                ],
                vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None,
                defaults=[], lineno=1),
            body=body_stmt,
            decorator_list=[]
        )
        self._inner_funcs.append(func)
        return ast.Name(inner_func_name, ctx=ast.Load())

    def visitArg_assignment(self, ctx: TongWenParser.Arg_assignmentContext):
        arg_name = ctx.IDENTIFIER().getText()
        arg_default_value = self.visitData(ctx.data()) if ctx.data() else None
        # TODO: type infer
        arg_type = self.visitType(ctx.type_()) if ctx.type_() else None
        return FunctionArg(arg_name, arg_type, arg_default_value)

    def visitFunction_call_expr(self, ctx: TongWenParser.Function_call_exprContext):
        sub_expr = None
        if ctx.function_call_pre_expr():
            sub_expr = ctx.function_call_pre_expr()
        elif ctx.function_call_mid_expr():
            sub_expr = ctx.function_call_mid_expr()
        elif ctx.function_call_post_expr():
            sub_expr = ctx.function_call_post_expr()
        func_var = self.visitFunction_name(sub_expr.function_name())
        all_data = sub_expr.data()
        values = [self.visitData(data) for data in all_data]
        return self.function_call(func_var, *values)

    def visitFunction_name(self, ctx: TongWenParser.Function_nameContext):
        if ctx.p_data():
            return self.visitP_data(ctx.p_data())
        else:
            return self.get_id(ctx.getText())
