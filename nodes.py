import pprint
from gpyconf._internal.dicts import ordereddict


class Node(object):
    def __init__(self):
        self.children = ordereddict()

    def __repr__(self):
        return '<%r \n{%s}>' % (
            type(self).__name__,
            pprint.pformat([(name, child) for name, child in
                            self.children.iteritems()])[1:-1]
        )

    def __eq__(self, other):
        return dict.__eq__(self.children, other.children)

class Expression(Node):
    pass

class ExpressionContainer(Expression):
    def __init__(self, expr):
        Node.__init__(self)
        assert isinstance(expr, Node)
        self.children['expression'] = expr

    def __repr__(self):
        return '(%s)' % self.children['expression']

class Declaration(Expression):
    def __init__(self, name, type):
        Expression.__init__(self)
        self.children['name'] = name
        self.children['type'] = type

class Identifier(Expression):
    def __init__(self, name):
        Expression.__init__(self)
        self.children['name'] = name

    def __repr__(self):
        return '`%s`' % repr(self.children['name'])[1:-1]

class Literal(Expression):
    def __init__(self, value):
        Expression.__init__(self)
        self.children['value'] = value

class String(Literal):
    pass

class Number(Literal):
    pass

class Assignment(Expression):
    def __init__(self, name, value):
        Expression.__init__(self)
        self.children['name'] = name
        self.children['value'] = value

class Definition(Node):
    def __init__(self, decl, value):
        Node.__init__(self)
        self.children['decl'] = decl
        self.children['value'] = value

class Block(Node):
    def __init__(self, statements):
        Node.__init__(self)
        self.children['statements'] = statements

class DeclarationBlock(Node):
    def __init__(self, decls):
        Node.__init__(self)
        self.children['decls'] = decls

class Function(Expression):
    def __init__(self, return_type, signature, block):
        Expression.__init__(self)
        self.children['return_type'] = return_type
        self.children['signature'] = signature
        self.children['block'] = block

class Call(Expression):
    def __init__(self, name, argument_list):
        Expression.__init__(self)
        self.children['name'] = name
        self.children['argument_list'] = argument_list

class Return(Node):
    def __init__(self, expr):
        Node.__init__(self)
        self.children['expr'] = expr

class ObjectTypeDeclaration(Node):
    def __init__(self, name, decl_block):
        Node.__init__(self)
        self.children['name'] = name
        self.children['decl_block'] = decl_block

class If(Node):
    def __init__(self, expr, block, else_block=None):
        Node.__init__(self)
        self.children['expr'] = expr
        self.children['block'] = block
        self.children['else_block'] = else_block

class Condition(Node):
    def __init__(self, *nodes):
        Node.__init__(self)
        self.children['nodes'] = list(nodes)

    def __repr__(self):
        return '<%s>' % repr(self.children['nodes'])[1:-1]

    def merge_list(self, other):
        assert isinstance(other, list)
        for op, expr in other:
            self.children['nodes'].append(op)
            if isinstance(expr, Condition):
                # further recursion detected. *aufloes*
                self.children['nodes'].extend(expr.children['nodes'])
            else:
                self.children['nodes'].append(expr)
        return self
