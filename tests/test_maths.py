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
            7 + (3 * (2 + 1) / 5 * 7 * (8/9)) - 9 * (5 - 3)
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
                        OP.MULTIPLY,
                        ExpressionContainer(
                            MathExpression(Integer(2), OP.ADD, Integer(1))
                        ),
                        OP.DIVIDE,
                        Integer(5),
                        OP.MULTIPLY,
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



if __name__ == '__main__':
    import sys
    if '-v' in sys.argv:
        import cProfile as prof
        prof.run('unittest.main()')
    else:
        unittest.main()
