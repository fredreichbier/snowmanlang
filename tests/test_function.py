import unittest
from test import Testcase

from nodes import *
from operators import OP

_ = Identifier

class FunctionTestcase(Testcase):
    def test_definition(self):
        self.assert_generates_ast('''
            foo as Function <- String(a as Int, b as Float, c as Bool, d as Bool, e as Bool, f as Bool):
                if c and e and (d or e) or f:
                    return a
                else:
                    return b
            ''',
            [Definition(
                Declaration(_('foo'), _('Function')),
                Function(
                    _('String'),
                    [
                        Declaration(_('a'), _('Int')),
                        Declaration(_('b'), _('Float')),
                        Declaration(_('c'), _('Bool')),
                        Declaration(_('d'), _('Bool')),
                        Declaration(_('e'), _('Bool')),
                        Declaration(_('f'), _('Bool'))
                    ],
                    Block([
                        If(
                            LogicalExpression([
                                _('c'),
                                OP.AND,
                                LogicalExpression([_('d'), OP.OR, _('e')]),
                                OP.OR,
                                _('f')
                            ]),
                            Block([Return(_('a'))]),
                            Block([Return(_('b'))])
                        )
                    ])
                )
            )]
        )

if __name__ == '__main__':
    unittest.main()
