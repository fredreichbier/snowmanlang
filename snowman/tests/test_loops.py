import unittest
from snowman.tests import Testcase, _, _op, _t
from snowman.nodes import *

class ForLoopTestcase(Testcase):
    def test_simple(self):
        self.assert_generates_ast('''
            for i as Int from 0 to 10:
                printf("Hi! %d\\n", i)
        ''',
        [
            ForLoop(
                Declaration(_('i'), _t('Int')),
                Integer(0),
                Integer(10),
                AtomicIncrement(
                    Declaration(_('i'), _t('Int')),
                    return_new_value=False
                )
            )
        ])

    def test_with_step(self):
        self.assert_generates_ast('''
            for i as Int from 0 to 10 step 2:
                printf("Hi! %d\\n", i)
        ''',
        [
        #    ForLoop(
        #    )
        ])


class WhileLoopTestcase(Testcase):
    def test_basic(self):
        self.assert_generates_ast('''
            while a < b:
                do_something()
        ''',
        [
            WhileLoop(
                Condition([_('a'), _op('<'), _('b')]),
                Block([
                    Call(_('do_something'), [])
                ])
            )
        ])

if __name__ == '__main__':
    unittest.main()
