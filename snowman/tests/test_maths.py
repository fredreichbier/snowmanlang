import unittest
from snowman.tests import Testcase, _, _op, _t
from snowman.nodes import *

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
                Declaration(_('a'), _t('Int')),
                MathExpression(Integer(5), _op('*'), Integer(8)),
            ),
            Definition(
                Declaration(_('b'), _t('Float')),
                MathExpression(Integer(10), _op('*'), Float(3.14))
            ),
            Assignment(_('b'),
                MathExpression(Integer(10), _op('/'), Float(5.678))
            ),
            Assignment(_('b'),
                MathExpression(Integer(5), _op('*'), Integer(5), _op('+'), Integer(1))
            ),
            Assignment(_('b'),
                MathExpression(
                    Integer(5),
                    _op('*'),
                    Integer(3),
                    _op('+'),
                    ExpressionContainer(
                        MathExpression(
                            Integer(2), _op('*'), Integer(7)
                        )
                    )
                )
            ),
            MathExpression(
                Integer(7),
                _op('+'),
                ExpressionContainer(
                    MathExpression(
                        Integer(3),
                        _op('**'),
                        ExpressionContainer(
                            MathExpression(Integer(2), _op('+'), Integer(1))
                        ),
                        _op('/'),
                        Integer(5),
                        _op('^'),
                        Integer(7),
                        _op('*'),
                        ExpressionContainer(
                            MathExpression(Integer(8), _op('/'), Integer(9))
                        ),
                    )
                ),
                _op('-'),
                Integer(9),
                _op('*'),
                ExpressionContainer(
                    MathExpression(Integer(5), _op('-'), Integer(3))
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
                    Declaration(_('a'), _t('Int')),
                    MathExpression(Integer(5), _op('**'), Float(0.7))
                ),
                Definition(
                    Declaration(_('b'), _t('Float')),
                    MathExpression(
                        Float(0.2),
                        _op('*'),
                        Call(_('sqrt'), [Integer(2)]),
                        _op('*'),
                        _('a'),
                        _op('/'),
                        Call(_('blah'),
                             [MathExpression(
                                 _('a'),
                                 _op('*'),
                                Call(_('sqrt'), [Integer(2)])
                             )]
                        )
                    )
                )
            ])


if __name__ == '__main__':
    unittest.main()
