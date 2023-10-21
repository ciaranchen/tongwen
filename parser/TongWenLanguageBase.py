from collections import namedtuple, defaultdict

Variable = namedtuple('variable', ['type', 'value'])


class TongWenLanguageBase:
    def __init__(self) -> None:
        base_math_funcs = {
            '加': Variable(type='Function', value=lambda x, y: x + y),
            '减': Variable(type='Function', value=lambda x, y: x - y),
            '乘': Variable(type='Function', value=lambda x, y: x * y),
            '除': Variable(type='Function', value=lambda x, y: x / y),
            '求和': Variable(type='Function', value=lambda *x: sum(x)),
        }
        base_logic_funcs = {
            '非': Variable(type='Function', value=lambda x: not x),
            '或': Variable(type='Function', value=lambda x, y: x or y),
            '且': Variable(type='Function', value=lambda x, y: x and y),
        }
        base_comp_funcs = {
            '等': Variable(type='Function', value=lambda x, y: x == y),
            '同': Variable(type='Function', value=lambda x, y: x is y),
            '大': Variable(type='Function', value=lambda x, y: x > y),
            '小': Variable(type='Function', value=lambda x, y: x < y),
            '大或等': Variable(type='Function', value=lambda x, y: x >= y),
            '小或等': Variable(type='Function', value=lambda x, y: x <= y),
        }
        self.vars = defaultdict(None, **base_math_funcs, **base_logic_funcs, **base_comp_funcs)
