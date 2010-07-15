import unittest
from snowman.tests import Testcase
from snowman.nodes import Char, String, Integer, Float

class CharTypeTestcase(Testcase):
    def test_char(self):
        self.assert_generates_ast('''
            'a'
            'b'
        ''',
        [
            Char('a'),
            Char('b')
        ])

class StringTypeTestcase(Testcase):
    def test_simple_string(self):
        self.assert_generates_ast('''
            "hello snowman"
            "wuzzup?"
        ''',
        [
            String("hello snowman"),
            String("wuzzup?")
        ])

    def test_multiline(self):
        self.assert_generates_ast('''
            "hello
            snowman
                what's
            up?"
        ''',
        [
            String("hello\nsnowman\n    what's\nup?")
        ])


class NumberTypeTestcase(Testcase):
    def test_integer(self):
        self.assert_generates_ast('''
            5
            7
            10_000_000_000
        ''',
        [
            Integer(5),
            Integer(7),
            Integer(10000000000)
        ])

    def test_float(self):
        self.assert_generates_ast('''
            3.1_45
            9.0000_0_09
            1.23_45
        ''',
        [
            Float(3.145),
            Float(9.0000009),
            Float(1.2345)
        ])

if __name__ == '__main__':
    unittest.main()
