import pprint
from snowman import operators
from snowman.utils import ordereddict


class Node(object):
    abstract = True

    def __init__(self):
        if self.__class__.__dict__.get('abstract'):
            raise TypeError("Cannot instantiate abstract class '%s'" % type(self).__name__)
        self.children = ordereddict()

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return dict.__eq__(self.children, other.children)

    def __repr__(self):
        return '<%s %s>' % (
            self.__class__.__name__,
            '\n'.join('%s:%s' % (k, v) for k, v in self.children.iteritems())
        )

class Operator(Node):
    def __init__(self, op):
        Node.__init__(self)
        self.children['op'] = op

    @classmethod
    def for_symbol(cls, symbol):
        return cls(operators.for_symbol(symbol))

# Expressions.
class Expression(Node):
    abstract = True

class ExpressionContainer(Expression):
    def __init__(self, expr):
        Node.__init__(self)
        assert isinstance(expr, Node)
        self.children['expression'] = expr


class Identifier(Expression):
    def __init__(self, name):
        Expression.__init__(self)
        self.children['name'] = name

class TypeIdentifier(Identifier):
    def __init__(self, name, pointer=False):
        Identifier.__init__(self, name)
        self.children['pointer'] = pointer

class ObjectMember(Expression):
    def __init__(self, obj, member):
        Expression.__init__(self)
        self.children['object'] = obj
        self.children['member'] = member


class Literal(Expression):
    abstract = True

    def __init__(self, value):
        Expression.__init__(self)
        self.children['value'] = value

class String(Literal):
    pass

class Number(Literal):
    abstract = True

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
    def __init__(self, function_name, argument_list):
        Expression.__init__(self)
        assert isinstance(argument_list, list), argument_list
        self.children['function_name'] = function_name
        self.children['argument_list'] = argument_list


class FlatListExpression(Expression):
    abstract = True

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

class MathExpression(FlatListExpression):
    def __init__(self, *nodes):
        FlatListExpression.__init__(self, *nodes)


# Statements.
class Statement(Node):
    abstract = True

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
    def __init__(self, name, parent_type, decl_block):
        Statement.__init__(self)
        self.children['name'] = name
        if parent_type.children['name'] != 'Object':
            self.children['parent_type'] = parent_type
        else:
            self.children['parent_type'] = None
        self.children['decl_block'] = decl_block

class If(Statement):
    def __init__(self, expr, block, else_block=None):
        Statement.__init__(self)
        assert isinstance(block, Block)
        self.children['expr'] = expr
        self.children['block'] = block
        self.children['else_block'] = else_block
