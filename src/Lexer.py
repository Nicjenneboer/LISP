import enum
import re
from parser import *

class Token():
    def __init__(self, type, eval, value, pos):
        self.type = type
        self.eval = eval
        self.value = value
        self.pos = pos


    def __str__(self):
        return self.type + ' ' + str(self.value)

    def __repr__(self):
        return self.__str__()


class Pos():
    def __init__(self, row=0, index=0):
        self.row = row
        self.index = index

    def __str__(self):
        return str((self.row, self.index))

    def __repr__(self):
        return self.__str__()

class Lexer():

    def __init__(self, code, error):
        self.code = code
        self.error = error

    def group(self, lst, deli, pos=Pos(), tmp=[], group='' ):
        if len(lst) < 1:
            return tmp
        if lst[0] in ' \n' + deli:
            if group: tmp+=[[group, pos]]; group=''
            if lst[0] == '\n': pos=Pos(pos.row+1, -1)
            elif lst[0] != ' ': tmp+=[[lst[0], pos]]
        else:
            group+=lst[0]
        return self.group(lst[1:], deli, Pos(pos.row, pos.index+1), tmp, group)

    def assigntoken(self, element):
        pos = element[1]
        element = element[0]
        if element.lstrip('-').isdigit():
            type, eval = 'INT', 'NUMBER'
            element = int(element)
        elif re.match(r'^-?\d+(?:\.\d+)$', element):
            type, eval = 'FLOAT', 'NUMBER'
            element = float(element)
        elif element[0] == '"' and element[-1] == '"':
            type, eval = 'STRING', 'TEXT'
            element = element[1:-1]
        elif element == '+':
            type, eval = 'PLUS', 'BINOP'
        elif element == '-':
            type, eval = 'MIN', 'BINOP'
        elif element == '*':
            type, eval = 'MUL', 'BINOP'
        elif element == '/':
            type, eval = 'DIV', 'BINOP'
        elif element == '(':
            type, eval = 'O_BRACKET', 'BRACKET'
        elif element == ')':
            type, eval = 'C_BRACKET', 'BRACKET'
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
        elif element == 'if':
            type, eval = 'IF', 'CONDITION'
        elif element == 'write':
            type, eval = 'PRINT', 'PRINT'
        elif element == 'setf':
            type, eval = 'SET', 'SETVAR'
            
        elif element == 'defun':
            type, eval = 'SET', 'SETFUNC'
        elif element.isalnum():
            type, eval = 'VAR', 'VAR'

        else:
            self.error.newError('Error', pos)
            return
        
        return Token(type, eval, element, pos)

    def tokenize(self):
        try:
            return list(map(self.assigntoken, self.group(self.code, '()')))
        except:
            print(self.error)
            return []