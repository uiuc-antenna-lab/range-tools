# Simple parser for command files
#
# Written by Brian Gibbons
#
# Version 0.1 - October 16, 2013


#global project, datafile

#project = 'unset'
#datafile = 'unset'
#option = 'unset'
#power = 'unset'
#fstart = 'unset'
#fstop = 'unset'
#npts = 'unset'
#pol = 'unset'
#ares = 'unset'
#start = 'unset'
#stop = 'unset'

# Tokens

literals = ['e','E']

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
    'h' : 'H1',
    'H' : 'H2', # I suspect there's a better way to do this...
    'horiz' : 'H3',
    'Horiz' : 'H4',
    'HORIZ' : 'H5',
    'v' : 'V1',
    'V' : 'V2',
    'vert' : 'V3',
    'Vert' : 'V4',
    'VERT' : 'V5',
}
# TODO: Add capability to use MHz, GHz, dBm, mW, etc.

tokens = ['ID','NUMBER','EQ'] + list(reserved.values())

t_EQ = r'='
#t_PLUS    = r'\+'
#t_MINUS   = r'-'
#t_TIMES   = r'\*'
#t_DIVIDE  = r'/'
#t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'


def t_USERCOMMENT(t):
    r'\#.*\n'
    # Discard all characters between a '#' and the end of the line
    pass

def t_NUMBER(t):
#    r'\d+'
    r'[0-9]+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # TODO: add support for filenames beginning with digits (enclose in quotes)
    t.type = reserved.get(t.value,'ID') # Look for reserved keywords; if none found, default to ID
    return t

#def t_EOFSTRING(t): # End Of File String (which is a comment)

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)




finput = open('test.mes','r')
ftext = finput.read()   # Read in entire file into string
finput.close()

# Build the lexer
import ply.lex as lex
lexer = lex.lex()
lexer.input(ftext)

while 1:    # Display all tokens
    tok = lexer.token()
    if not tok: break
    print tok




# Parsing rules (grammar)

def p_cmdfile(p):
    '''cmdfile : cmdfile param
               | param'''
    if (len(p) == 3):
#        print("  cmdfile 1: ")
#        print(type(p[1]))
#        print(type(p[2]))
        p[1].update(p[2])
        p[0] = p[1]
        #p[0] = (p[1]).update(p[2])
#        print(type(p[0]))
#        print("end update")
    else:
        p[0] = p[1]

def p_param(p):
    '''param : projfile
             | datasavefile
             | optionset
             | powerset
             | freqset
             | polset
             | angleset
             | commentset'''
    p[0] = p[1]
#    print("param: '%s'" % p[1])

def p_projfile(p):
    'projfile : PROJECT EQ ID'
    p[0] = {'project' : p[3]}

def p_datasavefile(p):
    'datasavefile : DATASAVE EQ ID'
    p[0] = {'datafile' : p[3]}

def p_optionset(p):
    '''optionset : OPTION EQ MEASURE
                 | OPTION EQ SGH'''
    p[0] = {'option' :  p[3]}

def p_powerset(p):
    '''powerset : POWER EQ DEFAULT
                | POWER EQ value'''
    if (p[3] != 'default'):
        print("Power changed from default to '%s'" % p[3])
        p[0] = {'power' : p[3]}
    else:
        p[0] = {}

def p_freqset(p):
    ''' freqset : freqstart
                | freqstop
                | numpoints'''
    p[0] = p[1]

def p_freqstart(p):
    'freqstart : FSTART EQ value'
    p[0] = {'fstart' : p[3]}
   
def p_freqstop(p):
    'freqstop : FSTOP EQ value'
    p[0] = {'fstop' : p[3]}

def p_numpoints(p):
    'numpoints : NPTS EQ value'
    p[0] = {'npts' : p[3]}

def p_polset(p):
    '''polset : POL EQ polh
              | POL EQ polv'''
    p[0] = {'pol' : p[3]}

def p_polh(p):
    '''polh : H1
            | H2
            | H3
            | H4
            | H5'''
    p[0] = 'H'


def p_polv(p):
    '''polv : V1
            | V2
            | V3
            | V4
            | V5'''
    p[0] = 'V'


def p_angleset(p):
    '''angleset : anglestart
                | anglestop
                | angleres'''
    p[0] = p[1]

def p_anglestart(p):
    'anglestart : START EQ value'
    p[0] = {'start' : p[3]}

def p_anglestop(p):
    'anglestop : STOP EQ value'
    p[0] = {'stop' : p[3]}

def p_angleres(p):
    'angleres : ARES EQ value'
    p[0] = {'ares' : p[3]}

def p_commentset(p):
    'commentset : COMMENTS' #EOFSTRING'
    #comments = p[2]
    p[0] = {}


def p_value(p):
    '''value : value 'e' NUMBER
             | value 'E' NUMBER
             | NUMBER '''
    # TODO: add MHz etc. here
    if (len(p) == 4):
        p[0] = p[1] * (10**p[3])
    else:
        p[0] = p[1]
    

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"



# Build the parser
import ply.yacc as yacc
parser = yacc.yacc()


result = parser.parse(ftext)
#print("project = " + project)
#print("datafile = " + datafile)
#print("option = " + option)
#print("power = " + power)
#print("fstart = " + fstart)
#print("fstop = " + fstop)
#print("npts = " + npts)
#print("pol = " + pol)
#print("ares = " + pol)
#print("start = " + start)
#print("stop = " + stop)


print("\nParsed values:")
print(result)


#while True:
#    try:
#        s = raw_input('calc > ')
#    except EOFError:
#        break
#    if not s: continue
#    result = parser.parse(s)
#    print result


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
