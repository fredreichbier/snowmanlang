from itertools import count

class _OP(object):
    def __init__(self):
        self._symbols = dict()

    def __getattr__(self, symbol_):
        symbol = self._symbols.get(symbol_)
        if symbol is None:
            self._symbols[symbol_] = symbol = self._make_symbol(symbol_)
        return symbol

    def _make_symbol(self, symbol):
        class _symbol(object):
            def __repr__(self):
                return symbol
        return _symbol()
OP = _OP()

OPERATORS = {
    'not' : OP.NOT,
    'or'  : OP.OR,
    'and' : OP.AND,
    'is'  : OP.EQUAL,
    '<'   : OP.SMALLER,
    '>'   : OP.BIGGER,
    '<='  : OP.SMALLER_EQUAL,
    '>='  : OP.BIGGER_EQUAL,
    '&'   : OP.BINARY_AND,
    '|'   : OP.BINARY_OR,
    'xor' : OP.XOR
}

def for_symbol(symbol):
    return OPERATORS[symbol]
