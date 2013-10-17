# Simple parser for command files
#
# Written by Brian Gibbons
#
# Version 0.1 - October 16, 2013


# Tokens

literals = ['e']

reserved = {
    'project' : 'PROJECT',
	'datasave' : 'DATASAVE',
	'option' : 'OPTION',
	'power' : 'POWER',
	'fstart' : 'FSTART',
	'fstop' : 'FSTOP',
	'npts' : 'NPTS',
	'pol' : 'POL',
	'ares' : 'ARES',
	'start' : 'START',
	'stop' : 'STOP',
	'comments' : 'COMMENTS',
    'measure' : 'MEASURE',
    'sgh' : 'SGH',
    'default' : 'DEFAULT',
    'h' : 'HORIZ',
    'H' : 'HORIZ',
    'v' : 'VERT',
    'V' : 'VERT',
}
# TODO: Add capability to use MHz, GHz, dBm, mW, etc.

tokens = ['KEYWORD','NUMBER','VERT','HORIZ','EQ'] + list(reserved.values())

t_EQ = r'='
#t_PLUS    = r'\+'
#t_MINUS   = r'-'
#t_TIMES   = r'\*'
#t_DIVIDE  = r'/'
#t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'


def t_USERCOMMENT(t):
    r'\#.*\n'
    # Discard all characters between a '#' and the end of the line
    print("User comment")
    pass

def t_KEYWORD(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # TODO: add support for filenames beginning with digits (enclose in quotes)
    t.type = reserved.get(t.value,'ERROR')
    if t.type == 'ERROR':
        print("Unknown keyword '%s'" % t.value)
        # TODO: stop here?
    else :
        return t

def t_NUMBER(t):
#    r'\d+'
    r'[0-9]+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)



# Build the lexer
import ply.lex as lex
lex.lex()


finput = open('test.mes','r')
ftext = finput.read()   # Read in entire file into string
lex.input(ftext)
while 1:
    tok = lex.token()
    if not tok: break
    print tok


# Parsing rules





#precedence = (
#    ('left','PLUS','MINUS'),
#    ('left','TIMES','DIVIDE'),
#    ('right','UMINUS'),
#    )
#
## dictionary of names
#names = { }
#
#def p_statement_assign(t):
#    'statement : NAME EQUALS expression'
#    names[t[1]] = t[3]
#
#def p_statement_expr(t):
#    'statement : expression'
#    print(t[1])
#
#def p_expression_binop(t):
#    '''expression : expression PLUS expression
#                  | expression MINUS expression
#                  | expression TIMES expression
#                  | expression DIVIDE expression'''
#    if t[2] == '+'  : t[0] = t[1] + t[3]
#    elif t[2] == '-': t[0] = t[1] - t[3]
#    elif t[2] == '*': t[0] = t[1] * t[3]
#    elif t[2] == '/': t[0] = t[1] / t[3]
#
#def p_expression_uminus(t):
#    'expression : MINUS expression %prec UMINUS'
#    t[0] = -t[2]
#
#def p_expression_group(t):
#    'expression : LPAREN expression RPAREN'
#    t[0] = t[2]
#
#def p_expression_number(t):
#    'expression : NUMBER'
#    t[0] = t[1]
#
#def p_expression_name(t):
#    'expression : NAME'
#    try:
#        t[0] = names[t[1]]
#    except LookupError:
#        print("Undefined name '%s'" % t[1])
#        t[0] = 0
#
#def p_error(t):
#    print("Syntax error at '%s'" % t.value)
#
#import ply.yacc as yacc
#yacc.yacc()
#
#while 1:
#    try:
#        s = input('calc > ')   # Use raw_input on Python 2
#    except EOFError:
#        break
#    yacc.parse(s)
