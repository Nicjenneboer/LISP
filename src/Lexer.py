import re
from parser import *

class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()

class Lexer():

    def __init__(self, code):
        self.code = code
        self.elements = []
        self.tokens = []

    def create_elements(self):
        self.elements = list(filter(None, re.split('([(|)|+])|\s+', self.code)))

    def assigntoken(self, element):
        if element.lstrip('-').isdigit():
            token = Token('INT', int(element))
        elif re.match(r'^-?\d+(?:\.\d+)$', element):
            token = Token('FLOAT', float(element))
        elif element[0] == '"' and element[-1] == '"':
            token = Token('STRING', element[1:-1])
        elif element == '+':
            token = Token('PLUS', element)
        elif element == '-':
            token = Token('MIN', element)
        elif element == '*':
            token = Token('MUL', element)
        elif element == '/':
            token = Token('DIV', element)
        elif element == '(':
            token = Token('O_BRACKET', element)
        elif element == ')':
            token = Token('C_BRACKET', element) 
        return token

    def tokenize(self):
        self.create_elements()
        self.tokens = map(self.assigntoken, self.elements)
        return list(self.tokens)