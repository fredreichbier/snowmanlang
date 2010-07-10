from itertools import count

class _OP(dict):
    class _str(str): pass
    __missing__ = lambda self, key: self._str(key)
    __getattr__ = dict.__getitem__

OP = _OP()

OPERATORS = {
    'is'  : OP.EQUAL,
    'not' : OP.NOT,
    'or'  : OP.OR,
    'and' : OP.AND,
    '<'   : OP.SMALLER,
    '>'   : OP.BIGGER,
    '<='  : OP.SMALLER_EQUAL,
    '>='  : OP.BIGGER_EQUAL,
    '&'   : OP.BINARY_AND,
    '|'   : OP.BINARY_OR,
    'xor' : OP.XOR,
    '<<'  : OP.SHIFT_LEFT,
    '>>'  : OP.SHIFT_RIGHT,
    '+'   : OP.ADD,
    '-'   : OP.SUBTRACT,
    '*'   : OP.MULTIPLY,
    '/'   : OP.DIVIDE,
    '^'   : OP.POW,
    '**'  : OP.POW
}

for symbol, op in OPERATORS.iteritems():
    op.symbol = symbol
del symbol, op

def for_symbol(symbol):
    return OPERATORS[symbol]
