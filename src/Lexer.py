import re
from src.Classes import *

#Split code in elements and add element position
def group(lst, deli, pos=Pos(), tmp=[], str='' ):
    if len(lst) < 1:
        return tmp
    if lst[0] in ' \n' + deli:
        if str: tmp+=[[str, pos]]; str=''
        if lst[0] == '\n': pos=Pos(pos.row+1, -1)
        elif lst[0] != ' ': tmp+=[[lst[0], pos]]
    else:
        str+=lst[0]
    return group(lst[1:], deli, Pos(pos.row, pos.index+1), tmp, str)

#Make a token from an element
def assigntoken(element):
    pos = element[1]
    element = element[0]

    # TYPES
    if element.lstrip('-').isdigit():
        type, eval = 'INT', 'NUMBER'
        element = int(element)
    elif re.match(r'^-?\d+(?:\.\d+)$', element):
        type, eval = 'FLOAT', 'NUMBER'
        element = float(element)
    elif element[0] == '"' and element[-1] == '"':
        type, eval = 'STRING', 'TEXT'
        element = element[1:-1]
    
    # BINARY OPERATIONS
    elif element == '+':
        type, eval = 'PLUS', 'BINOP'
    elif element == '-':
        type, eval = 'MIN', 'BINOP'
    elif element == '*':
        type, eval = 'MUL', 'BINOP'
    elif element == '/':
        type, eval = 'DIV', 'BINOP'
    elif element == '=':
        type, eval = 'EQUAL', 'BOOL'
    elif element == '>':
        type, eval = 'GREATER', 'BOOL'
    elif element == '<':
        type, eval = 'LESS', 'BOOL'
    elif element == '>=':
        type, eval = 'GREATEROREQUAL', 'BOOL'
    elif element == '<=':
        type, eval = 'LESSOREQUAL', 'BOOL'


    elif element == '(':
        type, eval = 'O_BRACKET', 'BRACKET'
    elif element == ')':
        type, eval = 'C_BRACKET', 'BRACKET'

    
    #SPECIAL OPERATIONS
    elif element == 'if':
        type, eval = 'IF', 'CONDITION'
    elif element == 'write':
        type, eval = 'PRINT', 'PRINT'
    
    # DEFINE OPERATIONS
    elif element == 'setf':
        type, eval = 'SET', 'SETVAR'
            
    elif element == 'defun':
        type, eval = 'SET', 'SETFUNC'

    # VARIABLES
    elif element.isalnum():
        type, eval = 'VAR', 'VAR'

    else:
        return
        
    return Token(type, eval, element, pos)

#List Elements to List Tokens
def tokenize(code):
    return list(map(assigntoken, group(code, '()')))