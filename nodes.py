class Node(object):
    pass

class Expression(Node):
    pass

class Declaration(Expression):
    def __init__(self, name, type):
        Expression.__init__(self)
        self.name = name
        self.type = type

    def __repr__(self):
        return '<%s at 0x%x = %r as %r>' % (type(self).__name__, id(self), self.name, self.type)

class Identifier(Expression):
    def __init__(self, name):
        Expression.__init__(self)
        self.name = name

    def __repr__(self):
        return '<%s at 0x%x = %r>' % (type(self).__name__, id(self), self.name)

class Literal(Expression):
    def __init__(self, value):
        Expression.__init__(self)
        self.value = value

    def __repr__(self):
        return '<%s at 0x%x = %r>' % (type(self).__name__, id(self), self.value)

class String(Literal):
    pass

class Number(Literal):
    pass

class Assignment(Expression):
    def __init__(self, name, value):
        Expression.__init__(self)
        self.name = name
        self.value = value

    def __repr__(self):
        return '<%s at 0x%x = %r <- %r>' % (type(self).__name__, id(self), self.name, self.value)

class Definition(Node):
    def __init__(self, decl, value):
        Node.__init__(self)
        self.decl = decl
        self.value = value

    def __repr__(self):
        return '<%s at 0x%x = %r <- %r>' % (type(self).__name__, id(self), self.decl, self.value)

class Block(Node):
    def __init__(self, statements):
        Node.__init__(self)
        self.statements = statements

    def __repr__(self):
        return '<%s at 0x%x = %r>' % (type(self).__name__, id(self), self.statements)

class DeclarationBlock(Node):
    def __init__(self, decls):
        Node.__init__(self)
        self.decls = decls

    def __repr__(self):
        return '<%s at 0x%x = %r>' % (type(self).__name__, id(self), self.decls)


class Function(Expression):
    def __init__(self, return_type, signature, block):
        Expression.__init__(self)
        self.return_type = return_type
        self.signature = signature
        self.block = block

    def __repr__(self):
        return '<%s at 0x%x = %r(%r): %r>' % (type(self).__name__, id(self),
            self.return_type, self.signature, self.block)

class Call(Expression):
    def __init__(self, name, argument_list):
        Expression.__init__(self)
        self.name = name
        self.argument_list = argument_list

    def __repr__(self):
        return '<%s at 0x%x = %r(%r)>' % (type(self).__name__, id(self),
            self.name, self.argument_list)

class Return(Node):
    def __init__(self, expr):
        Node.__init__(self)
        self.expr = expr

    def __repr__(self):
        return '<%s at 0x%x = %r>' % (type(self).__name__, id(self), self.expr)

class ObjectTypeDeclaration(Node):
    def __init__(self, name, decl_block):
        Node.__init__(self)
        self.name = name
        self.decl_block = decl_block

    def __repr__(self):
        return '<%s at 0x%x = %r, %r>' % (type(self).__name__, id(self), self.name, self.decl_block)


