import os
from future_builtins import map
from itertools import chain
import cStringIO as stringio
from types import GeneratorType
from snowman.backends import Backend
from snowman import nodes

C_BUILTIN_TYPES = dict((snow_type, snow_type.lower()) for snow_type in
                       ('Int', 'Float', 'Boolean', 'Double', 'Char', 'Void'))
C_BUILTIN_TYPES['String'] = 'char*'

def fmt(string, *args, **kwargs):
    for arg in args:
        assert isinstance(arg, str), type(arg)
    for value in kwargs.itervalues():
        assert isinstance(value, str), type(value)
    return string.format(*args, **kwargs)

def indent_lines(iterator):
    return ''.join('\n    ' + line for line in iterator)

class CGeneratorBackend(Backend):
    fileext = '.c'

    def __init__(self, ast):
        Backend.__init__(self, ast)
        self._buf = stringio.StringIO()

    def _prepare_translation(self):
        self._var_type_map = {}
        self._type_members_map = {}

    def translate(self):
        def _write_chunk(chunk):
            self._buf.write(chunk)
            self._buf.write('\n')
        for chunk in Backend.translate(self):
            if isinstance(chunk, GeneratorType):
                for iteritbaby in map(_write_chunk, chunk):
                    pass
            else:
                _write_chunk(chunk)
        return self._buf.getvalue()

    def visit_statement(self, node):
        res = self.visit_node(node)
        if isinstance(node, (nodes.Function, nodes.ImportStatement)):
            return res
        if isinstance(res, GeneratorType):
            res = ';\n'.join(res)
        return res + ';'

    def visit_Ast(self, ast):
        for node in ast:
            yield self.visit_statement(node)

    def visit_Identifier(self, node):
        return node.children['name']

    def visit_TypeIdentifier(self, node):
        name = node.children['name']
        ptr = node.children['pointer'] and '*' or ''
        return C_BUILTIN_TYPES.get(name, name) + ptr

    def visit_Operator(self, node):
        return node.children['op'].symbol

    def visit_Integer(self, node):
        return str(node.children['value'])

    visit_Float = visit_Integer

    def visit_String(self, node):
        return '"%s"' % repr(node.children['value'])[1:-1]

    def visit_Declaration(self, node):
        return fmt('{type} {name}',
            type=self.visit_node(node.children['type']),
            name=self.visit_node(node.children['name'])
        )

    def visit_Definition(self, node):
        return '%s = %s' % tuple(map(self.visit_node, node.children.itervalues()))

    def visit_Block(self, node):
        stmts = map(self.visit_statement, node.children['body'])
        return '\n{' + indent_lines(stmts) + '\n}'

    def visit_Function(self, node):
        old_var_type_map, self._var_type_map = self._var_type_map, {}
        header = node.children['header']
        signature = map(self.visit_node, header.children['signature'])
        return_type = header.children['return_type']
        if return_type:
            return_type = self.visit_node(return_type)
        else:
            return_type = 'void'
        dct = {
            'name' : self.visit_node(node.children['name']),
            'body' : self.visit_node(node.children['body']),
            'return_type' : return_type,
            'signature'   : ', '.join(signature)
        }
        self._var_type_map = old_var_type_map
        return fmt('{return_type} {name}({signature}){body}', **dct)

    def visit_Return(self, node):
        if not node.children['expr']:
            return 'return'
        return 'return %s' % self.visit_node(node.children['expr'])

    def visit_Call(self, node):
        argument_list = ', '.join(map(self.visit_node, node.children['argument_list']))
        return fmt('{function_name}({argument_list})',
            function_name=self.visit_node(node.children['function_name']),
            argument_list=argument_list
        )

    def visit_MathExpression(self, node):
        return ' '.join(map(str, self.translate_child(node, 'nodes')))

    def visit_ObjectTypeDeclaration(self, node):
        type_name = self.visit_node(node.children['name'])
        members = []
        parent = node.children['parent_type']
        if parent is not None:
            members.append(self.visit_statement(
                nodes.Declaration(nodes.Identifier('__super__'), parent)
            ))
        members.extend(map(self.visit_statement,
                           node.children['decl_block'].children['decls']))

        self._type_members_map[type_name] = members

        yield 'typedef struct _%s %s' % (type_name, type_name)
        yield 'struct _%s {%s\n}' % (
            type_name,
            indent_lines(members)
        )

    def visit_DeclarationBlock(self, node):
        return indent_lines(map(self.visit_statement, node.children['decls']))

    def visit_ImportStatement(self, node):
        path = node.children['path']
        fname, ext = os.path.splitext(path)
        if not ext:
            path += '.h'
        if path.startswith('./'):
            return '#include "%s"' % path
        else:
            return '#include <%s>' % path

    def visit_Assignment(self, node):
        return '%s = %s' % tuple(map(self.visit_node, node.children.itervalues()))

    def visit_ObjectMember(self, node):
        obj, do_unary, name = node.children.itervalues()
        return ''.join((self.visit_node(obj), '->' if do_unary else '.', self.visit_node(name)))

    def visit_Char(self, node):
        return "'%s'" % node.children['value']
