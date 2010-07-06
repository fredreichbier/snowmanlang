import pprint
from utils import ordereddict


class Node(object):
    def __init__(self):
        self.children = ordereddict()

    def __repr__(self):
        return '<%r \n%s>' % (
            type(self).__name__,
            self.children
        )

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return dict.__eq__(self.children, other.children)

# Expressions.
class Expression(Node):
    pass

class ExpressionContainer(Expression):
    def __init__(self, expr):
        Node.__init__(self)
        assert isinstance(expr, Node)
        self.children['expression'] = expr

    def __repr__(self):
        return '(%s)' % self.children['expression']


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

class Integer(Number):
    _type = int

class Float(Number):
    _type = float


class Assignment(Expression):
    def __init__(self, name, value):
        Expression.__init__(self)
        self.children['name'] = name
        self.children['value'] = value


class FunctionHeader(Expression):
    def __init__(self, return_type, signature):
        Expression.__init__(self)
        assert isinstance(return_type, (Identifier, type(None)))
        self.children['return_type'] = return_type
        self.children['signature'] = signature

class Call(Expression):
    def __init__(self, name, argument_list):
        Expression.__init__(self)
        assert isinstance(argument_list, list), argument_list
        self.children['name'] = name
        self.children['argument_list'] = argument_list


class FlatListExpression(Expression):
    def __init__(self, *nodes):
        Expression.__init__(self)
        self.children['nodes'] = list(nodes)

    def merge_list(self, other):
        assert isinstance(other, list)
        for op, expr in other:
            self.children['nodes'].append(op)
            if isinstance(expr, type(self)):
                # further recursion detected. *aufloes*
                self.children['nodes'].extend(expr.children['nodes'])
            else:
                self.children['nodes'].append(expr)
        return self

class Condition(FlatListExpression):
    def __init__(self, *nodes):
        FlatListExpression.__init__(self, *nodes)

    def __repr__(self):
        return '<%s>' % repr(self.children['nodes'])[1:-1]

class MathExpression(FlatListExpression):
    def __init__(self, *nodes):
        FlatListExpression.__init__(self, *nodes)


# Statements.
class Statement(Node):
    pass

class Declaration(Statement):
    def __init__(self, name, type):
        Statement.__init__(self)
        self.children['name'] = name
        self.children['type'] = type

class Definition(Statement):
    def __init__(self, decl, value):
        Statement.__init__(self)
        self.children['declaration'] = decl
        self.children['value'] = value

class Function(Statement):
    def __init__(self, name, header, body):
        Statement.__init__(self)
        self.children['name'] = name
        self.children['header'] = header
        self.children['body'] = body

class Block(Statement):
    def __init__(self, statements):
        Statement.__init__(self)
        self.children['statements'] = statements

class DeclarationBlock(Statement):
    def __init__(self, decls):
        Statement.__init__(self)
        self.children['decls'] = decls

class Return(Statement):
    def __init__(self, expr):
        Statement.__init__(self)
        self.children['expr'] = expr

class ObjectTypeDeclaration(Statement):
    def __init__(self, name, decl_block):
        Statement.__init__(self)
        self.children['name'] = name
        self.children['decl_block'] = decl_block

class If(Statement):
    def __init__(self, expr, block, else_block=None):
        Statement.__init__(self)
        assert isinstance(block, Block)
        self.children['expr'] = expr
        self.children['block'] = block
        self.children['else_block'] = else_block
