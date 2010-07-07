import unittest
import pprint
from itertools import izip

from nodes import Node, Identifier as _
from parser import parse
from operators import OP

def is_same_ast(ast1, ast2):
    if isinstance(ast1, Node):
        if not isinstance(ast2, type(ast1)):
            # not the same node types
            return False
        else:
            return ast1 == ast2
    for ast1_item, ast2_item in izip(ast1, ast2):
        if not is_same_ast(ast1_item, ast2_item):
            return False
    return True

class Testcase(unittest.TestCase, object):
    setup = unittest.TestCase.setUp
    assert_equal = unittest.TestCase.assertEqual

    def assert_generates_ast(self, code, ast_):
        def _prettyasts(_cache=[]):
            if not _cache:
                _cache.extend(map(pprint.pformat, (generated_ast, ast_)))
            return _cache

        generated_ast = self.parse(code)
        self.assert_(
            is_same_ast(generated_ast, ast_),
            'The parser generated\n\n%s\n\nbut you told me it should be\n\n%s' \
                % tuple(_prettyasts())
        )
        return ast_

    def parse(self, code):
        if code[0] == '\n':
            code = code[1:]
        lines = code.split('\n')
        i = 0
        while lines[0][i] == ' ':
            i += 1
        return parse('\n'.join(line[i:] for line in lines))
