import unittest
from snowman.tests import Testcase, _
from snowman.nodes import *

class ImportStatementTestcase(Testcase):
    def test_absolute_import(self):
        self.assert_generates_ast('''
            import foobar
            import blah
        ''',
        [
            ImportStatement('foobar'),
            ImportStatement('blah')
        ])

    def test_relative_import(self):
        self.assert_generates_ast('''
        import ./blah
        import ./foo/bar/blah
        ''',
        [
            ImportStatement('./blah'),
            ImportStatement('./foo/bar/blah')
        ])

class AtomicIncrDecrTestcase(Testcase):
    def test_atomic_increment(self):
        self.assert_generates_ast('''
            i++
            ++j
        ''',
        [
            AtomicIncrement(_('i'), True),
            AtomicIncrement(_('j'), False)
        ])

    def test_atomic_decrement(self):
        self.assert_generates_ast('''
            k--
            --l
        ''',
        [
            AtomicDecrement(_('k'), True),
            AtomicDecrement(_('l'), False)
        ])

if __name__ == '__main__':
    unittest.main()
