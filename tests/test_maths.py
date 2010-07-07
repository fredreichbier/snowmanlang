import unittest
from test import Testcase, _, OP
from nodes import *

class MathsTestCase(Testcase):
    def test_multiple(self):
        self.assert_generates_ast('''
            a as Int = 5 * 8
            b as Float = 10 * 3.14
            b = 10 / 5.678
            b = 5 * 5 + 1
            b = 5 * 3 + (2 * 7)
            7 + (3 ^ (2 + 1) / 5 ** 7 * (8/9)) - 9 * (5 - 3)
        ''',
        [
            Definition(
                Declaration(_('a'), _('Int')),
                MathExpression(Integer(5), OP.MULTIPLY, Integer(8)),
            ),
            Definition(
                Declaration(_('b'), _('Float')),
                MathExpression(Integer(10), OP.MULTIPLY, Float(3.14))
            ),
            Assignment(_('b'),
                MathExpression(Integer(10), OP.DIVIDE, Float(5.678))
            ),
            Assignment(_('b'),
                MathExpression(Integer(5), OP.MULTIPLY, Integer(5), OP.ADD, Integer(1))
            ),
            Assignment(_('b'),
                MathExpression(
                    Integer(5),
                    OP.MULTIPLY,
                    Integer(3),
                    OP.ADD,
                    ExpressionContainer(
                        MathExpression(
                            Integer(2), OP.MULTIPLY, Integer(7)
                        )
                    )
                )
            ),
            MathExpression(
                Integer(7),
                OP.ADD,
                ExpressionContainer(
                    MathExpression(
                        Integer(3),
                        OP.POW,
                        ExpressionContainer(
                            MathExpression(Integer(2), OP.ADD, Integer(1))
                        ),
                        OP.DIVIDE,
                        Integer(5),
                        OP.POW,
                        Integer(7),
                        OP.MULTIPLY,
                        ExpressionContainer(
                            MathExpression(Integer(8), OP.DIVIDE, Integer(9))
                        ),
                    )
                ),
                OP.SUBTRACT,
                Integer(9),
                OP.MULTIPLY,
                ExpressionContainer(
                    MathExpression(Integer(5), OP.SUBTRACT, Integer(3))
                )
            )
        ])

    def test_with_vars_and_calls(self):
        self.assert_generates_ast('''
            a as Int = 5 ** 0.7
            b as Float = 0.2 * sqrt(2) * a / blah(a*sqrt(2))
            ''',
            [
                Definition(
                    Declaration(_('a'), _('Int')),
                    MathExpression(Integer(5), OP.POW, Float(0.7))
                ),
                Definition(
                    Declaration(_('b'), _('Float')),
                    MathExpression(
                        Float(0.2),
                        OP.MULTIPLY,
                        Call(_('sqrt'), [Integer(2)]),
                        OP.MULTIPLY,
                        _('a'),
                        OP.DIVIDE,
                        Call(_('blah'),
                             [MathExpression(
                                 _('a'),
                                 OP.MULTIPLY,
                                Call(_('sqrt'), [Integer(2)])
                             )]
                        )
                    )
                )
            ])


if __name__ == '__main__':
    unittest.main()
