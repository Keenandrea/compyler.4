import os, sys
import errno
import string
import token

# fsa table, where the magic happens. column [ws] for whitespace, [c] for character, [d] for digit, [eof] for end-of-file, [unk] for unknown character. the rest is explained clearly by
# the comments on the upperhand side of the columns and those on the righthands side of the table. lower into the programming of this module, the functionality for the table is clear
"""                      ws     c     d     =     <     >    <=    >=    ==     :     +     -     *     /     %     .     (     )     ,     {     }     ;     [     ]   eof    unk """
fsa_table         = [ [   0,    1,    2,    3,    4,    5,    6,    7,    8,    9,   10,   11,   12,   13,   14,   15,   16,   17,   18,   19,   20,   21,   22,   23,   -1,   -2], # row0
                      [1000,    1,    1, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000,    1], # row1  id
                      [1001, 1001,    2, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001], # row2  int
                      [1002, 1002, 1002, 1002, 1002, 1002, 1002, 1002, 1002, 1002, 1002, 1002, 1002, 1002, 1002, 1002, 1002, 1002, 1002, 1002, 1002, 1002, 1002, 1002, 1002, 1002], # row3  =
                      [1003, 1003, 1003, 1003, 1003, 1003, 1003, 1003, 1003, 1003, 1003, 1003, 1003, 1003, 1003, 1003, 1003, 1003, 1003, 1003, 1003, 1003, 1003, 1003, 1003, 1003], # row4  <
                      [1004, 1004, 1004, 1004, 1004, 1004, 1004, 1004, 1004, 1004, 1004, 1004, 1004, 1004, 1004, 1004, 1004, 1004, 1004, 1004, 1004, 1004, 1004, 1004, 1004, 1004], # row5  >
                      [1005, 1005, 1005, 1005, 1005, 1005, 1005, 1005, 1005, 1005, 1005, 1005, 1005, 1005, 1005, 1005, 1005, 1005, 1005, 1005, 1005, 1005, 1005, 1005, 1005, 1005], # row6  <=
                      [1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006], # row7  >=
                      [1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007], # row8  ==
                      [1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008], # row9  :
                      [1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009], # row10 +
                      [1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010], # row11 -
                      [1011, 1011, 1011, 1011, 1011, 1011, 1011, 1011, 1011, 1011, 1011, 1011, 1011, 1011, 1011, 1011, 1011, 1011, 1011, 1011, 1011, 1011, 1011, 1011, 1011, 1011], # row12 *
                      [1012, 1012, 1012, 1012, 1012, 1012, 1012, 1012, 1012, 1012, 1012, 1012, 1012, 1012, 1012, 1012, 1012, 1012, 1012, 1012, 1012, 1012, 1012, 1012, 1012, 1012], # row13 /
                      [1013, 1013, 1013, 1013, 1013, 1013, 1013, 1013, 1013, 1013, 1013, 1013, 1013, 1013, 1013, 1013, 1013, 1013, 1013, 1013, 1013, 1013, 1013, 1013, 1013, 1013], # row14 %
                      [1014, 1014, 1014, 1014, 1014, 1014, 1014, 1014, 1014, 1014, 1014, 1014, 1014, 1014, 1014, 1014, 1014, 1014, 1014, 1014, 1014, 1014, 1014, 1014, 1014, 1014], # row15 .
                      [1015, 1015, 1015, 1015, 1015, 1015, 1015, 1015, 1015, 1015, 1015, 1015, 1015, 1015, 1015, 1015, 1015, 1015, 1015, 1015, 1015, 1015, 1015, 1015, 1015, 1015], # row16 (
                      [1016, 1016, 1016, 1016, 1016, 1016, 1016, 1016, 1016, 1016, 1016, 1016, 1016, 1016, 1016, 1016, 1016, 1016, 1016, 1016, 1016, 1016, 1016, 1016, 1016, 1016], # row17 )
                      [1017, 1017, 1017, 1017, 1017, 1017, 1017, 1017, 1017, 1017, 1017, 1017, 1017, 1017, 1017, 1017, 1017, 1017, 1017, 1017, 1017, 1017, 1017, 1017, 1017, 1017], # row18 ,
                      [1018, 1018, 1018, 1018, 1018, 1018, 1018, 1018, 1018, 1018, 1018, 1018, 1018, 1018, 1018, 1018, 1018, 1018, 1018, 1018, 1018, 1018, 1018, 1018, 1018, 1018], # row19 {
                      [1019, 1019, 1019, 1019, 1019, 1019, 1019, 1019, 1019, 1019, 1019, 1019, 1019, 1019, 1019, 1019, 1019, 1019, 1019, 1019, 1019, 1019, 1019, 1019, 1019, 1019], # row20 }
                      [1020, 1020, 1020, 1020, 1020, 1020, 1020, 1020, 1020, 1020, 1020, 1020, 1020, 1020, 1020, 1020, 1020, 1020, 1020, 1020, 1020, 1020, 1020, 1020, 1020, 1020], # row21 ;
                      [1021, 1021, 1021, 1021, 1021, 1021, 1021, 1021, 1021, 1021, 1021, 1021, 1021, 1021, 1021, 1021, 1021, 1021, 1021, 1021, 1021, 1021, 1021, 1021, 1021, 1021], # row22 [
                      [1022, 1022, 1022, 1022, 1022, 1022, 1022, 1022, 1022, 1022, 1022, 1022, 1022, 1022, 1022, 1022, 1022, 1022, 1022, 1022, 1022, 1022, 1022, 1022, 1022, 1022], # row23 ]
                    ] # col0  col1  col2  col3  col4  col5  col6  col7  col8  col9 col10 col11 col12 col13 col14 col15 col16 col17 col18 col19 col20 col21 col22 col23 col24 col25    

# a dictionary of key :
# values pairs where ke
# ys are the exhaustive
# final states of our f
# sa table and values a
# re their correspondin
# g identifiers
final_states = {
    1000 : 'ID_tk',
    1001 : 'INT_tk',
    1002 : 'ASSIGN_tk',
    1003 : 'LT_tk',
    1004 : 'GT_tk',
    1005 : 'LT_EQ_tk',
    1006 : 'GT_EQ_tk',
    1007 : 'EQ_tk',
    1008 : 'COLON_tk',
    1009 : 'PLUS_tk',
    1010 : 'MINUS_tk',
    1011 : 'ASTERISK_tk',
    1012 : 'FSLASH_tk',
    1013 : 'MODULO_tk',
    1014 : 'DOT_tk',
    1015 : 'LPAREN_tk',
    1016 : 'RPAREN_tk',
    1017 : 'COMMA_tk',
    1018 : 'LBRACE_tk',
    1019 : 'RBRACE_tk',
    1020 : 'SEMICOLON_tk',
    1021 : 'LBRACKET_tk',
    1022 : 'RBRACKET_tk',
    -1   : 'EOF_tk',
    -2   : 'ERROR_tk',
}

# a dictionary of key : val
# ue pairs where keys are k
# eyword or reserved word l
# iterals and values are th
# e identifying tokens
keywords = {
    'start'   : 'START_tk',
    'stop'    : 'STOP_tk',
    'iterate'    : 'ITER_tk',
    'void'    : 'VOID_tk',
    'var'     : 'VAR_tk',
    'return'  : 'RETURN_tk',
    'in'      : 'IN_tk',
    'out'     : 'OUT_tk',
    'program' : 'PROGRAM_tk',
    'cond'    : 'COND_tk',
    'then'    : 'THEN_tk',
    'let'     : 'LET_tk',
}

# a diction
# ary of ke
# y : value
# pairs whe
# re keys a
# re symbol
# literals
# and value
# s are the
# fsa table
# indexing
symbols = {
    '='  : 3,
    '<'  : 4,
    '>'  : 5,
    '<=' : 6,
    '>=' : 7,
    '==' : 8,
    ':'  : 9,
    '+'  : 10,
    '-'  : 11,
    '*'  : 12,
    '/'  : 13,
    '%'  : 14,
    '.'  : 15,
    '('  : 16,
    ')'  : 17,
    ','  : 18,
    '{'  : 19,
    '}'  : 20,
    ';'  : 21,
    '['  : 22,
    ']'  : 23,
}

# list of all
# special cha
# racters for
# edge cases
specials = [
    '=', 
    '<',
    '>',
    '<=',
    '>=',
    '==',
    ':',
    '+',  
    '-',  
    '*',  
    '/',  
    '%',  
    '.',  
    '(',  
    ')',  
    ',',  
    '{',  
    '}',  
    ';',  
    '[',  
    ']',
    '~',
    '`',
    '!',
    '$',
    '^',
    '&',
    '_',
    '|',
    '\\',
    '"',  
]

# second call out of driver, get_toke
# ns will create a token with regards
# to the lexical analysis performed i
# nside the driver function
def get_tokens(state, literal, line):
    state_token = token.Token()
    if literal in keywords:
        state_token.identity = keywords.get(literal)
        state_token.instance = literal
        state_token.location = line
    elif final_states.has_key(state):
        state_token.identity = final_states.get(state)
        state_token.instance = literal
        state_token.location = line
    return state_token

# first call out of th
# e driver funtion, ge
# t_column will get th
# e state column of ou
# r fsa table above an
# d return it with reg
# ards to the file dat
# um under current ana
# lysis
def get_column(datum):
    if datum.isalpha():
        if datum.isupper():
            return 25
        else:
            return 1
    if datum.isdigit():
        return 2
    if datum.isspace():
        return 0
    if datum in specials:
        if symbols.has_key(datum):
            value = symbols.get(datum)
            return value
        else:
            return 25
    else:
        return 24

# driver function is th
# e first call in the m
# odule. it instantiate
# s a token, then loops
# through the fsa table
# above, analyzing lexe
# mes and mapping these
# to our language defin
# ing tokens as it goes
# the driver is for all
# intents and purposes,
# the scanner of this s
# mall lexical analysis
# and will throw errors
# if an illegal token i
# s scanned, if a token
# too large of length i
# s scanner, and will a
# lso default to an err
# or token
def driver(f,line):
    this_state = 0
    next_state = 0
    tk = token.Token()
    literal = ""

    while this_state < 1000 and this_state > -1:
        fpos = f.tell()
        datum = f.read(1)
        if datum == '#':
            while True:
                datum = f.read(1)
                if datum == '\n':
                    break
        fsa_state = get_column(datum)
        next_state = fsa_table[this_state][fsa_state]
        if this_state == 4 and fsa_state == 3:
            next_state = 1005
        if this_state == 5 and fsa_state == 3:
            next_state = 1006
        if this_state == 3 and fsa_state == 3:
            next_state = 1007
        if next_state >= 1000 or next_state < 0:
            if next_state >= 1000:
                if next_state == 1005:
                    tk = get_tokens(next_state, '<=', line)
                    tk.location = line
                    return tk, line 
                elif next_state == 1006:
                    tk = get_tokens(next_state, '>=', line)
                    tk.location = line
                    return tk, line 
                elif next_state == 1007:
                    tk = get_tokens(next_state, '==', line)
                    tk.location = line
                    return tk, line 
                else:
                    tk = get_tokens(next_state, literal, line)
                    tk.location = line
                    f.seek(fpos, os.SEEK_SET)
                    return tk, line 
            if next_state == -1:
                tk.identity = token.token_ids.token_names[35]
                tk.instance = 'EOF'
                tk.location = line
                return tk, line
            if next_state == -2:
                print "SCANNER ERROR: Illegal character '%s' on line %d" % (datum,line)
                tk.identity = token.token_ids.token_names[36]
                tk.instance = 'bad token'
                tk.location = line
                return tk, line              
        else:
            unit = datum
            if unit.isspace() == False:
                literal += unit
            if len(literal) > 7:
                print "SCANNER ERROR: Illegal identifier '%s' length is greater than %d on line %d" % (literal, len(literal), line) 
                tk.identity = token.token_ids.token_names[36]
                tk.instance = literal
                tk.location = line
                return tk, line            
            if datum == '\n':
                line = line + 1
            this_state = next_state
    return token.Token(token.token_ids.token_names[36],'bad token',line)