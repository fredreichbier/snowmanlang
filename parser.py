from dparser import Parser

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
                 | assignment
                 | definition
    '''
    return t[0]

def d_definition(t):
    ''' definition: declaration '<-' expression '''
    return nodes.Definition(t[0], t[2])

def d_assignment(t):
    ''' assignment: identifier '<-' expression '''
    return nodes.Assignment(t[0], t[2])

def d_expression(t):
    ''' expression: literal
                  | identifier
                  | assignment
                  | function
                  | call
    '''
    return t[0]

def d_call(t):
    '''
        call: identifier '(' argument_list? ')'
    '''
    return nodes.Call(t[0], t[2][0] if t[2] else [])

def d_function(t):
    ''' function: identifier '(' signature? ')' ':' block '''
    return nodes.Function(t[0], t[2][0] if t[2] else [], t[5])

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

def d_literal(t):
    ''' literal: string
               | number
    '''
    return t[0]

def d_string(t):
    r''' string: "\"[^\"]*\"" '''
    return nodes.String(t[0].decode('string-escape')[1:-1])

def d_number(t):
    r''' number: "[0-9]+" '''
    return nodes.Number(int(t[0]))

def d_declaration(t):
    r''' declaration: identifier 'as' identifier '''
    return nodes.Declaration(t[0], t[2])

def d_identifier(t):
    r''' identifier: "[a-zA-Z_][a-zA-Z0-9_]*" '''
    return nodes.Identifier(t[0])

def parse(s):
    return Parser().parse(preprocessor.preprocess(s)).getStructure()

from pprint import pprint
pprint(parse('''
a as Function <- String():
    132
    "huhu"

bubu <- a(3, "hallo")

urgh as String <- vzvz(6336, String():
    3544
)
'''))
#print parser.parse("""String get_name(person as Person):
#    return person.name

#""")
