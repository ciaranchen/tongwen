import ast

from TongWenParser import TongWenParser
from TongWenLexer import TongWenLexer
from TongWenLanguageBase import TongWenLanguageBase, Variable, FunctionArg, TongWenLambdaVisitor
from antlr4 import *


class TongWenParserVisitorInterpreter(TongWenLanguageBase):
    # Basic Parser Function
    def visitIf_statement(self, ctx: TongWenParser.If_statementContext):
        condition_stmts = ctx.condition_statement()
        body_stmts = ctx.body_statement()
        for cond, body in condition_stmts, body_stmts:
            condition = self.visitCondition_statement(cond)
            if condition:
                self.visitBody_statement(body)
                break
        if len(condition_stmts) != len(body_stmts):
            self.visitBody_statement(body_stmts[-1])

    def visitFor_arr_statement(self, ctx: TongWenParser.For_arr_statementContext):
        raise NotImplementedError

    def visitFor_while_statement(self, ctx: TongWenParser.For_while_statementContext):
        while True:
            cond = self.visitCondition_statement(ctx.condition_statement())
            if cond:
                # TODO: 实现break语句
                isBreak = self.visitBody_statement(ctx.body_statement())
                if isBreak:  # 检测到 break 语句
                    break
            else:  # 不满足循环条件退出
                break

    def visitBody_statement(self, ctx: TongWenParser.Body_statementContext):
        return self.visitProgram(ctx.program())

    def visitDelete_assign_statement(self, ctx: TongWenParser.Delete_assign_statementContext):
        # TODO: handle dot expr
        name = ctx.IDENTIFIER().getText()
        del self.vars[name]

    def visit_assign_helper(self, ctx):
        # TODO: handle dot expr
        data = self.visitData(ctx.data())
        # TODO: type infer
        type_ = self.visitType(ctx.type_()) if ctx.type_() else None
        name = ctx.IDENTIFIER().getText()
        self.vars[name] = Variable(type=type_, value=data)

    def visitAssign_left_statement(self, ctx: TongWenParser.Assign_left_statementContext):
        return self.visit_assign_helper(ctx)

    def visitAssign_right_statement(self, ctx: TongWenParser.Assign_right_statementContext):
        return self.visit_assign_helper(ctx)

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

    def visitLambda_expr(self, ctx: TongWenParser.Lambda_exprContext):
        args = ctx.arg_assignment()
        args_define = [self.visitArg_assignment(arg) for arg in args]
        lambda_parser = TongWenLambdaVisitor(args_define)
        body_stmt = lambda_parser.visitProgram(ctx.body_statement().program())
        func_def = ast.FunctionDef(
            name="result",
            args=ast.arguments(
                args=[
                    ast.arg(arg='_context', annotation=None),
                    *[ast.arg(arg=arg.name, annotation=None) for arg in args_define]],
                vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, posonlyargs=[], defaults=[]),
            body=body_stmt,
            decorator_list=[],
        )
        ast_tree = ast.Module(body=[func_def], type_ignores=[])
        ast.fix_missing_locations(ast_tree)
        namespace = {}
        print(ast.dump(ast_tree))
        exec(compile(ast_tree, filename='', mode='exec'), namespace)
        result = namespace['result']
        return result

    def visitArg_assignment(self, ctx: TongWenParser.Arg_assignmentContext):
        arg_name = ctx.IDENTIFIER().getText()
        arg_default_value = self.visitData(ctx.data()) if ctx.data() else None
        # TODO: type infer
        arg_type = self.visitType(ctx.type_()) if ctx.type_() else None
        return FunctionArg(arg_name, arg_type, arg_default_value)

    def visit_func_call_helper(self, ctx):
        func_var = self.visitFunction_name(ctx.function_name())
        all_data = ctx.data()
        values = [self.visitData(data) for data in all_data]
        return self.function_call(func_var, *values)

    def visitFunction_call_pre_expr(self, ctx: TongWenParser.Function_call_pre_exprContext):
        return self.visit_func_call_helper(ctx)

    def visitFunction_call_mid_expr(self, ctx: TongWenParser.Function_call_mid_exprContext):
        return self.visit_func_call_helper(ctx)

    def visitFunction_call_post_expr(self, ctx: TongWenParser.Function_call_post_exprContext):
        return self.visit_func_call_helper(ctx)

    def visitFunction_name(self, ctx: TongWenParser.Function_nameContext):
        if ctx.p_data():
            return self.visitP_data(ctx.p_data())
        else:
            # TODO: fix thi
            return self.get_id(ctx.getText())


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
