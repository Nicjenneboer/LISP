
from ast import parse
import re

class Token():
    
    def __init__(self, t_type, t_value):
        self.token_type = t_type
        self.token_value = t_value

    def __str__(self):
        return "'%s'" % (self.token_value) 

    def __repr__(self):
        return self.__str__()

class lexer():

    def __init__(self, code):
        self.code = code
        self.elements = []
        self.tokens = []

    def splitcode(self):
        self.elements = list(filter(None, re.split('([(|)|\'\"|+])|\s+', self.code)))

    def assigntoken(self, element):
        if element.isdigit():
            token = Token('INT', int(element))
        elif re.match(r'^-?\d+(?:\.\d+)$', element):
            token = Token('FLOAT', float(element))
        elif element == '+':
            token = Token('PLUS', element)
        elif element == '-':
            token = Token('MINUS', element)
        elif element == '(':
            token = Token('O_BRACKET', element)
        elif element == ')':
            token = Token('C_BRACKET', element) 
        else:
            token = Token('?', element)
        return token

    def tokenizer(self):
        tokens = map(self.assigntoken, self.elements)

        return list(tokens)

class parser():
    def __init__(self, tokens):
        self.tokens = tokens

    def make_lst(self, index=0, lst=[]):
        if self.tokens[index].token_type == 'O_BRACKET':
            tmp_lst, index = self.make_lst(index+1, lst=[])
            lst += tmp_lst
            if len(self.tokens) > index+1:
                return self.make_lst(index+1, lst)
        elif self.tokens[index].token_type == 'C_BRACKET':
            return [lst], index
        else:
            return self.make_lst(index+1, lst+[self.tokens[index]])
        return lst
   



def main():
    while True:
        code = input('lisp: ')
        Lexer = lexer(code)
        Lexer.splitcode()
        result = Lexer.tokenizer()
        Parser = parser(result)
        parse_list = Parser.make_lst()
        print(parse_list)


if __name__ == '__main__':
    main()