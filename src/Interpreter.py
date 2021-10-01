from src.Parser import *
from src.Lexer import *

class Interpreter():
    def __init__(self, code):
        self.code = code
        self.lexer = Lexer(code)
        self.parser = Parser(self.lexer.tokenize())
        self.ast = self.parser.make_lst()
