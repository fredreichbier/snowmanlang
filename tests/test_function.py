import unittest
from test import Testcase, _, _op
from nodes import *

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
            ''',
            [Function(
                _('foo'),
                FunctionHeader(
                    _('String'),
                    [
                        Declaration(_('a'), _('Int')),
                        Declaration(_('b'), _('Float')),
                        Declaration(_('c'), _('Bool')),
                        Declaration(_('d'), _('Bool')),
                        Declaration(_('e'), _('Bool')),
                        Declaration(_('f'), _('Bool'))
                    ]
                ),
                Block([
                    If(
                        Condition(_('a')),
                        Block([Return(_('a'))])
                    ),
                    If(
                        Condition(
                            _('c'), _op('and'),
                            _('e'), _op('and'),
                            ExpressionContainer(Condition(_('d'), _op('or'), _('e'))),
                            _op('or'),
                            ExpressionContainer(_('f'))
                        ),
                        Block([Return(_('a'))]),
                        Block([Return(_('b'))])
                    )
                ])
            )]
        )

    def test_recursion(self):
        self.assert_generates_ast('''
            bear as Function(emma as Heifer, bertram as Bull) -> Calf:
                return new(Calf)

            bear_n as Function(n as Int, emma as Heifer, bertram as Bull):
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
                    _('Calf'),
                    [
                        Declaration(_('emma'), _('Heifer')),
                        Declaration(_('bertram'), _('Bull'))
                    ],
                ),
                Block([Return(Call(_('new'), [_('Calf')]))])
            ),
            Function(
                _('bear_n'),
                FunctionHeader(
                    None,
                        [
                            Declaration(_('n'), _('Int')),
                            Declaration(_('emma'), _('Heifer')),
                            Declaration(_('bertram'), _('Bull'))
                        ],
                    ),
                    Block([
                        If(
                            Condition(_op('not'), _('n')),
                            Block([Return(None)]),
                            Block([
                                Call(_('bear'), [_('eve'), _('adam')]),
                                Return(
                                    Call(
                                        _('bear_n'),
                                        [MathExpression(_('n'), _op('-'), Integer(1))]
                                    )
                                )
                            ])
                        )
                    ])
            )
        ])


if __name__ == '__main__':
    unittest.main()
