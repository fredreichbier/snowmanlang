from dparser import Parser
from itertools import starmap
import nodes, preprocessor

def d_program(t):
    ''' program: stuff '''
    return t[0]

def d_stuff(t):
    ''' stuff: statement* '''
    return t[0]

def d_statement(t):
    ''' statement: expression
                 | declaration
                 | definition
                 | function_definition
                 | assignment
                 | return_statement
                 | type_declaration
                 | if_statement
                 | import_statement
    '''
    return t[0]

# Expressions.
def d_expression(t):
    ''' expression: literal
                  | variable
                  | assignment
                  | call
                  | function_header
                  | condition
                  | math_expression
                  | '(' expression ')'
    '''
    if len(t) == 1:
        # no parenthesis
        return t[0]
    else:
        assert len(t) == 3
        return nodes.ExpressionContainer(t[1])

def d_variable(t):
    r''' variable: identifier | member '''
    return t[0]

def d_identifier(t):
    r''' identifier: "[a-zA-Z_][a-zA-Z0-9_]*" '''
    return nodes.Identifier(t[0])

def d_type_identifier(t):
    r''' type_identifier: identifier '*'? '''
    return nodes.TypeIdentifier(
        t[0].children['name'],
        len(t[1]) == 1 # 1 = '*' given
    )

def d_member(t):
    r''' member: identifier '.' identifier '''
    return nodes.ObjectMember(t[0], t[2])

def d_declaration(t):
    r''' declaration: identifier 'as' type_identifier '''
    return nodes.Declaration(t[0], t[2])

def d_literal(t):
    ''' literal: string
               | number
    '''
    return t[0]

def d_string(t):
    r''' string: "\"[^\"]*\"" '''
    return nodes.String(t[0].decode('string-escape')[1:-1])

def d_number(t):
    r''' number: "[0-9][0-9_\.]*" '''
    number = t[0]
    first_dot = number.find('.')
    if first_dot != -1:
        # at least one dot. this is a float
        node_cls = nodes.Float
        second_dot = number.find('.', first_dot+1)
        if second_dot != -1:
            # two dots detected
            raise SyntaxError(
                number[:second_dot] + '[syntax error]' + number[second_dot:]
            )
    else:
        # no dots. this is an integer
        node_cls = nodes.Integer
    return node_cls(node_cls._type(number.replace('_', '')))

def d_math_expression(t):
    ''' math_expression: expression (math_operator expression)+ '''
    return nodes.MathExpression(t[0]).merge_list(t[1])

def d_math_operator(t):
    ''' math_operator: '+'
                     | '-'
                     | '*'
                     | '/'
                     | '^'
                     | '**'
    '''
    return nodes.Operator.for_symbol(t[0])

def d_condition(t):
    ''' condition: 'not'? expression (logical_operator expression)* '''
    assert len(t) == 3
    if t[0]:
        return nodes.Condition(
            nodes.Operator.for_symbol(t[0][0]),
            t[1]
        ).merge_list(t[2])
    else:
        return nodes.Condition(t[1]).merge_list(t[2])

def d_logical_operator(t):
    ''' logical_operator: 'is'
                        | 'not'
                        | 'and'
                        | 'or'
                        | '<'
                        | '>'
                        | '<='
                        | '>='
                        | '&'
                        | '|'
                        | 'xor'
    '''
    return nodes.Operator.for_symbol(t[0])

# Statements.
def d_type_declaration(t):
    ''' type_declaration: object_type_declaration '''
    return t[0]

def d_object_type_declaration(t):
    ''' object_type_declaration: type_identifier '<-' type_identifier ':' declaration_block '''
    return nodes.ObjectTypeDeclaration(t[0], t[2], t[4])

def d_declaration_block(t):
    ''' declaration_block: '{' declaration* '}' '''
    return nodes.DeclarationBlock(t[1])

def d_call(t):
    ''' call: variable '(' argument_list? ')' '''
    return nodes.Call(t[0], t[2][0] if t[2] else [])

def d_function_definition(t):
    ''' function_definition: identifier 'as' function_header ':' block '''
    return nodes.Function(t[0], t[2], t[4])

def d_function_header(t):
    ''' function_header: 'Function(' signature? ')' ('->' type_identifier)?'''
    # very ugly find-out-whether-there-are-signature-and-or-return-type code.
    tokens = iter(t)
    tokens.next() # pass left parent
    signature = tokens.next()
    if not isinstance(signature, list):
        assert signature == ')'
        signature = ()
    else:
        signature = signature[0]
        tokens.next() # pass right parent
    return_type = tokens.next()
    if return_type:
        if not isinstance(return_type, list):
            assert return_type == ':', return_type
            return_type = None
        else:
            return_type = return_type[0][1]
    else:
        return_type = None
    return nodes.FunctionHeader(return_type, signature)

def d_signature(t):
    ''' signature: (declaration ',')* declaration '''
    decls = []
    for decl, comma in t[0]:
        decls.append(decl)
    decls.append(t[1])
    return decls

def d_argument_list(t):
    ''' argument_list: (expression ',')* expression '''
    exprs = []
    for expr, comma in t[0]:
        exprs.append(expr)
    exprs.append(t[1])
    return exprs

def d_block(t):
    ''' block: '{' stuff '}' '''
    return nodes.Block(t[1])

def d_return_statement(t):
    ''' return_statement: 'return' expression? '''
    return nodes.Return(t[1][0] if t[1] else None)

def d_definition(t):
    ''' definition: declaration '=' expression '''
    return nodes.Definition(t[0], t[2])

def d_assignment(t):
    ''' assignment: variable '=' expression '''
    return nodes.Assignment(t[0], t[2])

def d_if_statement(t):
    ''' if_statement: 'if' condition ':' block ('else:' block)? '''
    return nodes.If(t[1], t[3], t[4][0][1] if t[4] else None)

def d_import_statement(t):
    r''' import_statement: 'import' "[^ \\\n]+" '''
    # TODO: the \n stuff should probably go into d_statement.
    return nodes.ImportStatement(t[1])

def parse(s, parser=None):
    if parser is None:
        parser = Parser()
    return parser.parse(preprocessor.preprocess(s)).structure
