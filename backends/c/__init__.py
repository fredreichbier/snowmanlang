from future_builtins import map
import cStringIO as stringio
from .. import Backend

C_BUILTIN_TYPES = dict((snow_type, snow_type.lower()) for snow_type in
                       ('Int', 'Float', 'Boolean', 'Double', 'Char'))
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

    def __init__(self):
        self.reset()

    def reset(self):
        self._buf = stringio.StringIO()

    def translate_ast(self, ast, as_string=True):
        try:
            for chunk in Backend.translate_ast(self, ast):
                self._buf.write(chunk)
                self._buf.write('\n')
            if as_string:
                return self._buf.getvalue()
            else:
                return self._buf
        except Exception as exc:
           self.reset()
           raise

    def visit_statement(self, node):
        return self.visit_node(node) + ';'


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
        return '"%s"' % node.children['value']

    def visit_Declaration(self, node):
        return fmt('{type} {name}',
            type=self.visit_node(node.children['type']),
            name=self.visit_node(node.children['name'])
        )

    def visit_Definition(self, node):
        return '%s = %s' % tuple(map(self.visit_node, node.children.itervalues()))

    def visit_Block(self, node):
        stmts = map(self.visit_statement, node.children['statements'])
        return '\n{' + indent_lines(stmts) + '\n}'

    def visit_Function(self, node):
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
        return 'typedef struct {%s\n} %s;\n' % tuple(
            map(self.visit_node, reversed(node.children.values())))

    def visit_DeclarationBlock(self, node):
        return indent_lines(map(self.visit_statement, node.children['decls']))
