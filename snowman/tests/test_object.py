import unittest
from snowman.tests import Testcase, _, _t
from snowman.nodes import *

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
                    _t('Foo'),
                    _t('Object'),
                    DeclarationBlock([
                        Declaration(_('a'), _t('Int')),
                        Declaration(_('b'), _t('Float')),
                        Declaration(_('foo'), _t('Foo'))
                    ])
                )
            ])

    def test_inheritance(self):
        ast = self.assert_generates_ast('''
            Parent <- Object:
                a as Int
                b as Parent*
            Child1 <- Parent:
                c as Parent*
                d as Float
            Child2 <- Parent:
                e as Int
            Child1_1 <- Child1:
                f as Child2
        ''',
        [
            ObjectTypeDeclaration(
                _t('Parent'),
                _t('Object'),
                DeclarationBlock([
                    Declaration(_('a'), _t('Int')),
                    Declaration(_('b'), _t('Parent', True))
                ])
            ),
            ObjectTypeDeclaration(
                _t('Child1'),
                _t('Parent'),
                DeclarationBlock([
                    Declaration(_('c'), _t('Parent', True)),
                    Declaration(_('d'), _t('Float'))
                ])
            ),
            ObjectTypeDeclaration(
                _t('Child2'),
                _t('Parent'),
                DeclarationBlock([
                    Declaration(_('e'), _t('Int'))
                ])
            ),
            ObjectTypeDeclaration(
                _t('Child1_1'),
                _t('Child1'),
                DeclarationBlock([
                    Declaration(_('f'), _t('Child2'))
                ])
            )
        ])
        Parent, Child1, Child2, Child1_1 = ast
        self.assert_equal(Parent.children['parent_type'], None)
        self.assert_equal(Child1.children['parent_type'], _t('Parent'))
        self.assert_equal(Child2.children['parent_type'], _t('Parent'))
        self.assert_equal(Child1_1.children['parent_type'], _t('Child1'))

    def test_malloc(self):
        self.assert_generates_ast('''
            Blah <- Object:
                a as Int
            fizz as Blah* = malloc(sizeof(Blah))
        ''',
        [
            ObjectTypeDeclaration(
                _t('Blah'),
                _t('Object'),
                DeclarationBlock([
                    Declaration(_('a'), _t('Int'))
                ])
            ),
            Definition(
                Declaration(_('fizz'), _t('Blah', True)),
                Call(_('malloc'), [Call(_('sizeof'), [_('Blah')])])
            )
        ])

    def test_read_member(self):
        self.assert_generates_ast('''
            foo->attr
            blah.attr2
        ''',
        [
            ObjectMember(_('foo'), _('attr'), do_unary=True),
            ObjectMember(_('blah'), _('attr2'), do_unary=False)
        ])

    def test_set_member(self):
        self.assert_generates_ast('''
            foo->attr = 42
            blah.attr = foo->attr
        ''',
        [
            Assignment(
                ObjectMember(_('foo'), _('attr'), do_unary=True),
                Integer(42)
            ),
            Assignment(
                ObjectMember(_('blah'), _('attr'), do_unary=False),
                ObjectMember(_('foo'), _('attr'), do_unary=True)
            )
        ])

if __name__ == '__main__':
    unittest.main()
