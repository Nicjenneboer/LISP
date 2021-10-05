import re
from parser import *

class Token():
    def __init__(self, type, eval, value):
        self.type = type
        self.eval = eval
        self.value = value


    def __str__(self):
        return self.type + ' ' + str(self.value)

    def __repr__(self):
        return self.__str__()

class Lexer():

    def __init__(self, code):
        self.code = code

    def create_elements(self):
        return list(filter(None, re.split('([(|)|+])|\s+', self.code)))

    def assigntoken(self, element):
        if element.lstrip('-').isdigit():
            token = Token('INT', 'NUMBER', int(element))
        elif re.match(r'^-?\d+(?:\.\d+)$', element):
            token = Token('FLOAT', 'NUMBER', float(element))
        elif element[0] == '"' and element[-1] == '"':
            token = Token('STRING', 'TEXT', element[1:-1])
        elif element == '+':
            token = Token('PLUS', 'BINOP', element)
        elif element == '-':
            token = Token('MIN', 'BINOP', element)
        elif element == '*':
            token = Token('MUL', 'BINOP', element)
        elif element == '/':
            token = Token('DIV', 'BINOP', element)
        elif element == '(':
            token = Token('O_BRACKET', 'BRACKET', element)
        elif element == ')':
            token = Token('C_BRACKET', 'BRACKET', element) 
        elif element == '=':
            token = Token('EQUAL', 'BOOL', element)
        elif element == '>':
            token = Token('GREATER', 'BOOL', element)
        elif element == '<':
            token = Token('LESS', 'BOOL', element)
        elif element == '>=':
            token = Token('GREATEROREQUAL', 'BOOL', element)
        elif element == '<=':
            token = Token('LESSOREQUAL', 'BOOL', element)
        elif element == 'if':
            token = Token('IF', 'SPECOP', element)
        return token

    def tokenize(self):
        return list(map(self.assigntoken, self.create_elements()))