from dparser import Parser
from itertools import starmap

import nodes, preprocessor, operators

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
                 | return_statement
                 | type_declaration
                 | if_statemenet
    '''
    return t[0]

def d_return_statement(t):
    ''' return_statement: 'return' expression '''
    return nodes.Return(t[1])

def d_definition(t):
    ''' definition: declaration '<-' expression '''
    return nodes.Definition(t[0], t[2])

def d_assignment(t):
    ''' assignment: identifier '<-' expression '''
    return nodes.Assignment(t[0], t[2])

def d_if_statement(t):
    ''' if_statemenet: 'if' expression ':' block ('else:' block)? '''
    return nodes.If(t[1], t[3], t[4][0] if t[4] else None)

def d_expression(t):
    ''' expression: '('? _expression ')'? '''
    if len(t) == 1:
        return t[0]
    else:
        expr = t[1]
        expr.eval_first = True
        return expr

def d__expression(t):
    ''' _expression: literal
                   | identifier
                   | assignment
                   | function
                   | call
                   | condition
    '''
    return t[0]

def d_condition(t):
    ''' condition: expression (logical_operator expression)*
    '''
    return nodes.Condition(t)

def d_logical_operator(t):
    ''' logical_operator: 'is'
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
    return operators.for_symbol(t[0])

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

def d_type_declaration(t):
    ''' type_declaration: object_type_declaration '''
    return t[0]

def d_object_type_declaration(t):
    ''' object_type_declaration: identifier '<-' 'Object' ':' declaration_block '''
    return nodes.ObjectTypeDeclaration(t[0], t[4])

def d_declaration_block(t):
    ''' declaration_block: '{' declaration* '}' '''
    return nodes.DeclarationBlock(t[1])

def parse(s):
    return Parser().parse(preprocessor.preprocess(s)).getStructure()
