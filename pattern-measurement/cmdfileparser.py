# Simple parser for command files
#
# This uses the module PLY, which is a python implementation of lex and yacc,
# which are tools for writing compilers (flex and bison, respectively, are
# probably more common versions of these programs). PLY may be found at
# http://www.dabeaz.com/ply/

# Written by Brian Gibbons

# Version 0.6 - October 18, 2013
#   -Turns script into a function
#   -power setting now explictly returned if set, even if just to 'default'

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
#    -Adds support for comment section at end of file

# Version 0.2 - October 17, 2013
#    -Extends number support to include decimals, scientific notation, and signs

# Version 0.1 - October 16, 2013


import ply.lex as lex
import ply.yacc as yacc
import os
    
# The class Parser and this method of converting to classes is heavily based on
# an example written by David McNab and provided with the PLY distribution.
class Parser:
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    reserved = ()
    tokens = ()
    precedence = ()

    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.names = { }
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[1] + "_" + self.__class__.__name__
        except:
            modname = "parser"+"_"+self.__class__.__name__
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"
        #print self.debugfile, self.tabmodule

        # Build the lexer and parser
        lex.lex(module=self, debug=self.debug)
        yacc.yacc(module=self,
                  debug=self.debug,
                  debugfile=self.debugfile,
                  tabmodule=self.tabmodule)

    def parse(self, inputstring):
        result = yacc.parse(inputstring)
        return result


class CmdfileParser(Parser):
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
    
    def t_USERCOMMENT(self, t):
        r'\#.*\n'
        # Discard all characters between a '#' and the end of the line
        t.lexer.lineno += 1
    
    def t_SCINUMDECIMAL(self, t):
        r'[+-]?[0-9]*\.[0-9]+[eE][+-]?[0-9]+'
        t.type = 'NUMBER'
        t.value = float(t.value)
        return t
    
    def t_DECIMAL(self, t):
        r'[+-]?[0-9]*\.[0-9]+'
        t.type = 'NUMBER'
        t.value = float(t.value)
        return t
    
    def t_SCINUMINT(self, t):
        r'[+-]?[0-9]+[eE][+-]?[0-9]+'
        t.type = 'NUMBER'
        t.value = float(t.value)
        return t
    
    def t_NUMBER(self, t):
    #    r'\d+'
        r'[+-]?[0-9]+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %d", t.value)
            t.value = 0
        return t
    
    def t_COMMENTS(self, t): # Comment section at end of command file
        r'[Cc]omments'
        # Set token value to be comment string
        t.value = t.lexer.lexdata[t.lexer.lexpos : len(t.lexer.lexdata)-1]
        t.value = str.lstrip(t.value)   # Strip leading whitespace characters
        # Set position to end of input so it doesn't parse the comment section
        t.lexer.lexpos = len(t.lexer.lexdata)
        return t
    
    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        # TODO: add support for filenames beginning with digits (enclose in quotes)
        t.type = self.reserved.get(t.value,'ID') # Look for reserved keywords; if none found, default to ID
        return t
    
    # Ignored characters
    t_ignore = " \t"    # Ignore spaces and tabs (these will be stripped out)
    
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
        
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
    

    #############################
    #  Parsing rules (grammar)  #
    #############################
    def p_cmdfile(self, p):   # Starting grammar symbol
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
    
    def p_param(self, p):
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
    
    def p_projfile(self, p):
        'projfile : PROJECT EQ ID'
        p[0] = {'project' : p[3]}
    
    def p_datasavefile(self, p):
        'datasavefile : DATASAVE EQ ID'
        p[0] = {'datafile' : p[3]}
    
    def p_optionset(self, p):
        '''optionset : OPTION EQ measure
                     | OPTION EQ sgh'''
        p[0] = {'option' :  p[3]}
    
    def p_measure(self, p):
        '''measure : MEAS1
                   | MEAS2
                   | MEAS3'''
        p[0] = 'measure'
    
    def p_sgh(self, p):
        '''sgh : SGH1
               | SGH2
               | SGH3'''
        p[0] = 'sgh'
    
    def p_powerset(self, p):
        '''powerset : POWER EQ default
                    | POWER EQ value'''
#        if (p[3] != 'default'):
#            #print("Power changed from default to '%s'" % p[3])
#            p[0] = {'power' : p[3]}
#        else:
#            #print("Power set by user to default")
#            p[0] = {}
        p[0] = {'power' : p[3]} # Return power, even if just 'default', since user explicitly set it
    
    def p_default(self, p):
        '''default : DEFAULT1
                   | DEFAULT2
                   | DEFAULT3'''
        p[0] = 'default'
    
    def p_freqset(self, p):
        ''' freqset : freqstart
                    | freqstop
                    | numpoints'''
        p[0] = p[1]
    
    def p_freqstart(self, p):
        '''freqstart : FSTART EQ value
                     | FSTART EQ value mhz
                     | FSTART EQ value ghz'''
        if (len(p) == 4): # First rule
            p[0] = {'fstart' : p[3]}
        else: # Second or third rules
            p[0] = {'fstart' : p[3] * (10**p[4])}
       
    def p_freqstop(self, p):
        'freqstop : FSTOP EQ value'
        p[0] = {'fstop' : p[3]}
    
    # NOTE: the non-terminals mhz and ghz could be worked into value, in which case
    #       they'd simply be synonymous with *(10**6) and *(10**9), respectively.
    #       I've chosen to instead only add them to the grammar for the frequency
    #       set commands since this is the only proper place they should be used.
    def p_mhz(self, p):
        '''mhz : MHZ1
               | MHZ2
               | MHZ3
               | MHZ4'''
        p[0] = 6    # Value will be used as the exponent
    
    def p_ghz(self, p):
        '''ghz : GHZ1
               | GHZ2
               | GHZ3
               | GHZ4'''
        p[0] = 9    # Value will be used as the exponent
    
    def p_numpoints(self, p):
        'numpoints : NPTS EQ value'
        p[0] = {'npts' : p[3]}
    
    def p_polset(self, p):
        '''polset : POL EQ polh
                  | POL EQ polv'''
        p[0] = {'pol' : p[3]}
    
    def p_polh(self, p):
        '''polh : HORIZ1
                | HORIZ2
                | HORIZ3
                | HORIZ4
                | HORIZ5'''
        p[0] = 'H'
    
    
    def p_polv(self, p):
        '''polv : VERT1
                | VERT2
                | VERT3
                | VERT4
                | VERT5'''
        p[0] = 'V'
    
    
    def p_angleset(self, p):
        '''angleset : anglestart
                    | anglestop
                    | angleres'''
        p[0] = p[1]
    
    def p_anglestart(self, p):
        'anglestart : START EQ value'
        p[0] = {'start' : p[3]}
    
    def p_anglestop(self, p):
        'anglestop : STOP EQ value'
        p[0] = {'stop' : p[3]}
    
    def p_angleres(self, p):
        'angleres : ARES EQ value'
        p[0] = {'ares' : p[3]}
    
    def p_commentset(self, p):
        'commentset : COMMENTS'
        p[0] = {'comments' : p[1]}
    
    
    def p_value(self, p):
        'value : NUMBER'
        p[0] = p[1]
        
    # From PLY documentation:
    # Compute column
    #     input is the input text string
    #     token is a token instance
    def find_column(self, input,token):
        last_cr = input.rfind('\n',0,token.lexpos)
        if last_cr < 0:
            last_cr = 0
        column = (token.lexpos - last_cr) + 1
        return column
    
    # Error rule for syntax errors
    def p_error(self, p):
        print("\nERROR: Syntax error in input [%s]" % p)
        print("     Line "+str(p.lexer.lineno)+", position "+str(find_column(ftext,p)))
    
