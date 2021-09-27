import re

class Token():
    
    def __init__(self, t_type, t_value):
        self.t_type = t_type
        self.t_value = t_value

    def __str__(self):
        return "Token Type = '%s', Token Value = '%s'" % (self.t_type, self.t_value) 

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




            

def main():
    while True:
        code = input('lisp: ')
        Lexer = lexer(code)
        Lexer.splitcode()
        result = Lexer.tokenizer()
        print(result)


if __name__ == '__main__':
    main()