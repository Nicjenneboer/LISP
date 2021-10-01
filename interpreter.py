from Parser import *
from lexer import *

class Interpreter():
    def __init__(self, code):
        self.code = code
        self.lexer = Lexer(code)
        self.parser = Parser(self.lexer.tokenize())
        self.ast = self.parser.make_lst()

def main():
    f = open('test.lsp', 'r')
    code = f.read()
    preter = Interpreter(code)
    print(preter.ast)


if __name__ == '__main__':
    main()
