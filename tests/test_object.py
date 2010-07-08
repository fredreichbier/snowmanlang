import unittest
from test import Testcase, _
from nodes import *

class ObjectTestcase(Testcase):
    def test_declaration(self):
        self.assert_generates_ast('''
            Foo <- Object:
                a as Int
                b as Float
                foo as Foo
            ''',
            [
                ObjectTypeDeclaration(
                    _('Foo'),
                    _('Object'),
                    DeclarationBlock([
                        Declaration(_('a'), _('Int')),
                        Declaration(_('b'), _('Float')),
                        Declaration(_('foo'), _('Foo'))
                    ])
                )
            ])

    def test_inheritance(self):
        ast = self.assert_generates_ast('''
            Parent <- Object:
                a as Int
                b as Parent
            Child1 <- Parent:
                c as Parent
                d as Float
            Child2 <- Parent:
                e as Int
            Child1_1 <- Child1:
                f as Child2
        ''',
        [
            ObjectTypeDeclaration(
                _('Parent'),
                _('Object'),
                DeclarationBlock([
                    Declaration(_('a'), _('Int')),
                    Declaration(_('b'), _('Parent'))
                ])
            ),
            ObjectTypeDeclaration(
                _('Child1'),
                _('Parent'),
                DeclarationBlock([
                    Declaration(_('c'), _('Parent')),
                    Declaration(_('d'), _('Float'))
                ])
            ),
            ObjectTypeDeclaration(
                _('Child2'),
                _('Parent'),
                DeclarationBlock([
                    Declaration(_('e'), _('Int'))
                ])
            ),
            ObjectTypeDeclaration(
                _('Child1_1'),
                _('Child1'),
                DeclarationBlock([
                    Declaration(_('f'), _('Child2'))
                ])
            )
        ])
        Parent, Child1, Child2, Child1_1 = ast
        self.assert_equal(Parent.children['parent_type'], _('Object'))
        self.assert_equal(Child1.children['parent_type'], _('Parent'))
        self.assert_equal(Child2.children['parent_type'], _('Parent'))
        self.assert_equal(Child1_1.children['parent_type'], _('Child1'))

    def test_malloc(self):
        self.assert_generates_ast('''
            Blah <- Object:
                a as Int
            fizz as Blah = malloc(sizeof(Blah))
        ''',
        [
            ObjectTypeDeclaration(
                _('Blah'),
                _('Object'),
                DeclarationBlock([
                    Declaration(_('a'), _('Int'))
                ])
            ),
            Definition(
                Declaration(_('fizz'), _('Blah')),
                Call(_('malloc'), [Call(_('sizeof'), [_('Blah')])])
            )
        ])

    def test_read_member(self):
        self.assert_generates_ast('''
            foo.attr
            blah.attr2
        ''',
        [
            ObjectMember(_('foo'), _('attr')),
            ObjectMember(_('blah'), _('attr2'))
        ])

    def test_set_member(self):
        self.assert_generates_ast('''
            foo.attr = 42
            blah.attr = foo.attr
        ''',
        [
            Assignment(
                ObjectMember(_('foo'), _('attr')),
                Integer(42)
            ),
            Assignment(
                ObjectMember(_('blah'), _('attr')),
                ObjectMember(_('foo'), _('attr'))
            )
        ])

if __name__ == '__main__':
    unittest.main()
