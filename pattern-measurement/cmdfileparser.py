# Simple parser for command files
#
# Written by Brian Gibbons

# Version 0.5 - October 17, 2013
#   -Changes syntax error message to report line number of error
#   -Adds support for 'MHz' and 'GHz' in frequency settings
#   -Removes unused code
#   -Adds some comments and documentation

# Version 0.4 - October 17, 2013
#   -Adds support for scientific notation with decimal significands
#   -Removes unused grammar rule (and 'e' literals) for scientific notation
#   -Adds a few capitalization variants of some keywords
#   -Renames a few keywork tokens to be more descriptive 

# Version 0.3 - October 17, 2013
#	-Adds support for comment section at end of file

# Version 0.2 - October 17, 2013
#	-Extends number support to include decimals, scientific notation, and signs

# Version 0.1 - October 16, 2013


import ply.lex as lex
import ply.yacc as yacc



############
#  Tokens  #
############

reserved = {    # Dict of reserved keywords and their token (on right)
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
    'measure' : 'MEAS1',
    'Measure' : 'MEAS2',
    'MEASURE' : 'MEAS3',
    'sgh' : 'SGH1',
    'Sgh' : 'SGH2',
    'SGH' : 'SGH3',
    'default' : 'DEFAULT1',
    'Default' : 'DEFAULT2',
    'DEFAULT' : 'DEFAULT3',
    'h' : 'HORIZ1',
    'H' : 'HORIZ2', # I suspect there's a better way to do this...
    'horiz' : 'HORIZ3',
    'Horiz' : 'HORIZ4',
    'HORIZ' : 'HORIZ5',
    'v' : 'VERT1',
    'V' : 'VERT2',
    'vert' : 'VERT3',
    'Vert' : 'VERT4',
    'VERT' : 'VERT5',
    'mhz' : 'MHZ1',
    'Mhz' : 'MHZ2',
    'MHz' : 'MHZ3',
    'MHZ' : 'MHZ4',
    'ghz' : 'GHZ1',
    'Ghz' : 'GHZ2',
    'GHz' : 'GHZ3',
    'GHZ' : 'GHZ4',
}
# TODO: Add capability to use dBm, mW, etc.

# Tokens given in the list 'tokens' are defined in functions below
tokens = ['ID','NUMBER','EQ','COMMENTS'] + list(reserved.values())

t_EQ = r'=' # Simple token with regex for the equals sign

def t_USERCOMMENT(t):
    r'\#.*\n'
    # Discard all characters between a '#' and the end of the line
    t.lexer.lineno += 1

def t_SCINUMDECIMAL(t):
    r'[+-]?[0-9]*\.[0-9]+[eE][+-]?[0-9]+'
    t.type = 'NUMBER'
    t.value = float(t.value)
    return t

def t_DECIMAL(t):
    r'[+-]?[0-9]*\.[0-9]+'
    t.type = 'NUMBER'
    t.value = float(t.value)
    return t

def t_SCINUMINT(t):
    r'[+-]?[0-9]+[eE][+-]?[0-9]+'
    t.type = 'NUMBER'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
#    r'\d+'
    r'[+-]?[0-9]+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_COMMENTS(t): # Comment section at end of command file
    r'[Cc]omments'
    # Set token value to be comment string
    t.value = t.lexer.lexdata[t.lexer.lexpos : len(t.lexer.lexdata)-1]
    # Set position to end of input so it doesn't parse the comment section
    t.lexer.lexpos = len(t.lexer.lexdata)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # TODO: add support for filenames beginning with digits (enclose in quotes)
    t.type = reserved.get(t.value,'ID') # Look for reserved keywords; if none found, default to ID
    return t

# Ignored characters
t_ignore = " \t"    # Ignore spaces and tabs (these will be stripped out)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)



# Get input to parse
finput = open('test.mes','r')
ftext = finput.read()   # Read in entire file to string
finput.close()


lexer = lex.lex()   # Build the lexer
#lexer.input(ftext)  # Feed the input string to the lexer (to be tokenized)
#print("\nDisplaying parsed tokens:")
#print("*************************")
#while 1:    # Display all tokens
#    tok = lexer.token()
#    if not tok: break
#    print tok
## Note that printing tokens messes up line number counting (only needed for
## reporting location of syntax errors).




#############################
#  Parsing rules (grammar)  #
#############################
def p_cmdfile(p):   # Starting grammar symbol
    '''cmdfile : cmdfile param
               | param'''
    if (len(p) == 3):
        p[1].update(p[2])
        p[0] = p[1]
    else:
        p[0] = p[1]
# From the PLY documentation:
# The first rule defined in the yacc specification determines the starting
# grammar symbol [here, a rule for cmdfile appears first]. Whenever the
# starting rule is reduced by the parser and no more input is available,
# parsing stops and the final value is returned (this value will be whatever
# the top-most rule placed in p[0]). 

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
    '''optionset : OPTION EQ measure
                 | OPTION EQ sgh'''
    p[0] = {'option' :  p[3]}

def p_measure(p):
    '''measure : MEAS1
               | MEAS2
               | MEAS3'''
    p[0] = 'measure'

def p_sgh(p):
    '''sgh : SGH1
           | SGH2
           | SGH3'''
    p[0] = 'sgh'

def p_powerset(p):
    '''powerset : POWER EQ default
                | POWER EQ value'''
    if (p[3] != 'default'):
        #print("Power changed from default to '%s'" % p[3])
        p[0] = {'power' : p[3]}
    else:
        #print("Power set by user to default")
        p[0] = {}

def p_default(p):
    '''default : DEFAULT1
               | DEFAULT2
               | DEFAULT3'''
    p[0] = 'default'

def p_freqset(p):
    ''' freqset : freqstart
                | freqstop
                | numpoints'''
    p[0] = p[1]

def p_freqstart(p):
    '''freqstart : FSTART EQ value
                 | FSTART EQ value mhz
                 | FSTART EQ value ghz'''
    if (len(p) == 4): # First rule
        p[0] = {'fstart' : p[3]}
    else: # Second or third rules
        p[0] = {'fstart' : p[3] * (10**p[4])}
   
def p_freqstop(p):
    'freqstop : FSTOP EQ value'
    p[0] = {'fstop' : p[3]}

# NOTE: the non-terminals mhz and ghz could be worked into value, in which case
#       they'd simply be synonymous with *(10**6) and *(10**9), respectively.
#       I've chosen to instead only add them to the grammar for the frequency
#       set commands since this is the only proper place they should be used.
def p_mhz(p):
    '''mhz : MHZ1
           | MHZ2
           | MHZ3
           | MHZ4'''
    p[0] = 6    # Value will be used as the exponent

def p_ghz(p):
    '''ghz : GHZ1
           | GHZ2
           | GHZ3
           | GHZ4'''
    p[0] = 9    # Value will be used as the exponent

def p_numpoints(p):
    'numpoints : NPTS EQ value'
    p[0] = {'npts' : p[3]}

def p_polset(p):
    '''polset : POL EQ polh
              | POL EQ polv'''
    p[0] = {'pol' : p[3]}

def p_polh(p):
    '''polh : HORIZ1
            | HORIZ2
            | HORIZ3
            | HORIZ4
            | HORIZ5'''
    p[0] = 'H'


def p_polv(p):
    '''polv : VERT1
            | VERT2
            | VERT3
            | VERT4
            | VERT5'''
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
    'commentset : COMMENTS'
    p[0] = {'comments' : p[1]}


def p_value(p):
    'value : NUMBER'
    p[0] = p[1]
    
# From PLY documentation:
# Compute column
#     input is the input text string
#     token is a token instance
def find_column(input,token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
	last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column

# Error rule for syntax errors
def p_error(p):
    print("\nERROR: Syntax error in input [%s]" % p)
    print("     Line "+str(p.lexer.lineno)+", position "+str(find_column(ftext,p)))



parser = yacc.yacc()    # Build the parser
result = parser.parse(ftext)    # Feed the text input to the parser

print("\nParsed values dict:")
print(result)
