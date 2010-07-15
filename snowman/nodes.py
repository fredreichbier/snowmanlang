from future_builtins import map
from snowman import operators
from snowman.utils import ordereddict

class NIL:
    def __repr__(self):
        return '<NIL>'
NIL = NIL()

class Node(object):
    abstract = True

    def __init__(self, *args, **kwargs):
        if self.__class__.__dict__.get('abstract'):
            raise TypeError("Cannot instantiate abstract class '%s'" % type(self).__name__)

        self.children = ordereddict()

        # ugly code that populates the .children dictionary with arguments
        # taken from *args and **kwargs, respectively.
        def normalize_attr(attr):
            if isinstance(attr, tuple):
                assert len(attr) in (2, 3)
                if len(attr) == 3:
                    return attr
                else:
                    return (attr[0], attr[1], None)
            else:
                return (attr, NIL, None)

        args = list(reversed((args)))
        attrs = self.attributes
        for attr in attrs:
            name, default_value, conversion_func = normalize_attr(attr)
            try:
                self.children[name] = kwargs.pop(name)
                continue
            except KeyError:
                pass

            if not args:
                if default_value is NIL:
                    raise TypeError("Expected argument '%s'" % attr)
                else:
                    value = default_value
            else:
                value = args.pop()
            if conversion_func is not None:
                value = conversion_func(value)
            self.children[name] = value

        if kwargs:
            raise TypeError("Unexpected keyword arguments '%r'" % kwargs.keys())
        if args:
            raise TypeError("Unexpected positional arguments '%r'" % args)

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
    attributes = ['op']

    @classmethod
    def for_symbol(cls, symbol):
        return cls(operators.for_symbol(symbol))

# Expressions.
class Expression(Node):
    abstract = True

class ExpressionContainer(Expression):
    attributes = ['expression']


class Identifier(Expression):
    attributes = ['name']

class TypeIdentifier(Identifier):
    attributes = ['name', ('pointer', False)]

class ObjectMember(Expression):
    attributes = ['object', 'member', 'do_unary']


class Literal(Expression):
    abstract = True
    attributes = ['value']

class String(Literal):
    pass

class Char(Literal):
    pass

class Number(Literal):
    abstract = True

class Integer(Number):
    _type = int

class Float(Number):
    _type = float


class AtomicIncrDecr(Expression):
    attributes = ['expr', ('return_new_value', False)]

class AtomicIncrement(AtomicIncrDecr):
    pass

class AtomicDecrement(AtomicIncrDecr):
    pass

class Assignment(Expression):
    attributes = ['assignee', 'rval']

class FunctionHeader(Expression):
    attributes = ['return_type', 'signature']

class Call(Expression):
    attributes = ['function_name', 'argument_list']

class FlatListExpression(Expression):
    abstract = True
    attributes = ['nodes']

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
    pass

class MathExpression(FlatListExpression):
    pass

# Statements.
class Statement(Node):
    abstract = True

class Declaration(Statement):
    attributes = ['name', 'type']

class Definition(Statement):
    attributes = ['declaration', 'value']

class Function(Statement):
    attributes = ['name', 'header', 'body']

class Block(Statement):
    attributes = ['body']

class DeclarationBlock(Statement):
    attributes = ['decls']

class Return(Statement):
    attributes = ['expr']

class ObjectTypeDeclaration(Statement):
    _none_if_Object = lambda par:None if par.children['name'] == 'Object' else par

    attributes = ['name', ('parent_type', NIL, _none_if_Object), 'decl_block']

class If(Statement):
    attributes = ['expr', 'block', ('else_block', None)]

class ImportStatement(Statement):
    attributes = ['name']

class Loop(Statement):
    abstract = True

class ForLoop(Loop):
    attributes = ['variable', 'count_start', 'count_end', 'count_step']

class WhileLoop(Statement):
    attributes = ['condition', 'body']
