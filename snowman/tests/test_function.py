import unittest
from snowman.tests import Testcase, _, _op, _t
from snowman.nodes import *

class FunctionTestcase(Testcase):
    def test_definition(self):
        self.assert_generates_ast('''
            foo as Function(a as Int, b as Float, c as Bool, d as Bool, e as Bool, f as Bool) -> String:
                if a:
                    return a
                if c and e and (d or e) or (f):
                    return a
                else:
                    return b

            foo2 as Function():
                return 0
            ''',
            [
                Function(
                    _('foo'),
                    FunctionHeader(
                        _t('String'),
                        [
                            Declaration(_('a'), _t('Int')),
                            Declaration(_('b'), _t('Float')),
                            Declaration(_('c'), _t('Bool')),
                            Declaration(_('d'), _t('Bool')),
                            Declaration(_('e'), _t('Bool')),
                            Declaration(_('f'), _t('Bool'))
                        ]
                    ),
                    Block([
                        If(
                            Condition([_('a')]),
                            Block([Return(_('a'))])
                        ),
                        If(
                            Condition([
                                _('c'), _op('and'),
                                _('e'), _op('and'),
                                ExpressionContainer([Condition([_('d'), _op('or'), _('e')])]),
                                _op('or'),
                                ExpressionContainer([_('f')])
                            ]),
                            Block([Return(_('a'))]),
                            Block([Return(_('b'))])
                        )
                    ])
                ),
                Function(
                    _('foo2'),
                    FunctionHeader(None, []),
                    Block([Return(Integer(0))])
                )
            ])

    def test_recursion(self):
        self.assert_generates_ast('''
            bear as Function(emma as Heifer*, bertram as Bull*) -> Calf*:
                return malloc(sizeof(Calf))

            bear_n as Function(n as Int, emma as Heifer*, bertram as Bull*):
                if not n:
                    return
                else:
                    bear(eve, adam)
                    return bear_n(n-1)
        ''',
        [
            Function(
                _('bear'),
                FunctionHeader(
                    _t('Calf', True),
                    [
                        Declaration(_('emma'), _t('Heifer', True)),
                        Declaration(_('bertram'), _t('Bull', True))
                    ],
                ),
                Block([Return(Call(_('malloc'), [Call(_('sizeof'), [_('Calf')])]))])
            ),
            Function(
                _('bear_n'),
                FunctionHeader(
                    None,
                        [
                            Declaration(_('n'), _t('Int')),
                            Declaration(_('emma'), _t('Heifer', True)),
                            Declaration(_('bertram'), _t('Bull', True))
                        ],
                    ),
                    Block([
                        If(
                            Condition([_op('not'), _('n')]),
                            Block([Return(None)]),
                            Block([
                                Call(_('bear'), [_('eve'), _('adam')]),
                                Return(
                                    Call(
                                        _('bear_n'),
                                        [MathExpression([_('n'), _op('-'), Integer(1)])]
                                    )
                                )
                            ])
                        )
                    ])
            )
        ])


if __name__ == '__main__':
    unittest.main()
