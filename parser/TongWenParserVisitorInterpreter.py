import ast

from TongWenParser import TongWenParser
from TongWenLexer import TongWenLexer
from TongWenLanguageBase import TongWenLanguageBase, Variable, FunctionArg, TongWenLambdaVisitor
from antlr4 import *


class TongWenParserVisitorInterpreter(TongWenLanguageBase):
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
        if ctx.function_define_expr():
            return self.visitFunction_define_expr(ctx.function_define_expr())
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
        return self.function_call(operator_func, self.visitP_data(ctx.p_data(0)), self.visitP_data(ctx.p_data(1)))

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
        _type = self.visitType(ctx.type_()) if ctx.type_() else None
        return var_name, Variable(type=_type, value=value)

    def visitFunction_define_expr(self, ctx: TongWenParser.Function_define_exprContext):
        args = ctx.arg_assignment()
        args_define = [self.visitArg_assignment(arg) for arg in args]
        lambda_parser = TongWenLambdaVisitor(args_define)
        body_stmt = lambda_parser.visitProgram(ctx.body_statement().program())
        func_def = ast.FunctionDef(
            name="result",
            args=ast.arguments(args=[ast.arg(arg='_context'), *[ast.arg(arg=arg.name) for arg in args_define]],
                               vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None,
                               defaults=[]),
            body=body_stmt,
            decorator_list=[]
        )
        ast_tree = ast.Module(body=[func_def])
        ast.fix_missing_locations(ast_tree)
        namespace = {}
        # print(ast.dump(ast_tree))
        exec(compile(ast_tree, filename='', mode='exec'), namespace)
        result = namespace['result']
        return result

    def visitArg_assignment(self, ctx: TongWenParser.Arg_assignmentContext):
        arg_name = ctx.IDENTIFIER().getText()
        arg_default_value = self.visitData(ctx.data()) if ctx.data() else None
        # TODO: type infer
        arg_type = self.visitType(ctx.type_()) if ctx.type_() else None
        return FunctionArg(arg_name, arg_type, arg_default_value)

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
        return self.function_call(func_var, *values)

    def visitFunction_call_mid_expr(self, ctx: TongWenParser.Function_call_pre_exprContext):
        function = ctx.function_name().getText()
        func_var = self.vars.get(function, None).value
        data1, data2 = self.visitData(ctx.data(0)), self.visitData(ctx.data(1))
        return self.function_call(func_var, data1, data2)

    def visitFunction_call_post_expr(self, ctx: TongWenParser.Function_call_post_exprContext):
        function = ctx.function_name().getText()
        func_var = self.vars.get(function, None).value
        all_data = ctx.data()
        values = [self.visitData(data) for data in all_data]
        return self.function_call(func_var, *values)


def main():
    # input_expression = input("> ")
    with open('../书同文.同文', encoding='utf-8') as fp:
        input_expression = fp.read()
#     input_expression = """有 术 者 由（数 者 谓 乙，言 者 谓 丙，言 者 谓 丁）求 数 {
#     得 乙；
# } 为 首个参数；"""
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
