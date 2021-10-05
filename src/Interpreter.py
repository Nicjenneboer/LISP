from os import lstat
from src.Parser import *
from src.Lexer import *
from src.functions import *



class Interpreter():
    def __init__(self, code):
        self.code = code
        self.lexer = Lexer(code)
        self.tokens = self.lexer.tokenize()
        self.parser = Parser(self.tokens)
        self.tree = self.parser.create_nodes()
        

    def __str__(self):
        line = 'Lexer: \n'
        line += str(self.tokens) + '\n\n'
        line += 'Parser: \n'
        line += str(self.tree)
        return line

    eval = {
        'PLUS'  : lambda x,y: x + y,
        'MIN'   : lambda x,y: y - x,
        'MUL'   : lambda x,y: x * y,
        'DIV'   : lambda x,y: y / x,
        'EQUAL' : lambda x,y: 'T' if y == x else 'NIL', # NEED FIX FOR MORE VALUES
        'IF'    : lambda x,y,z: y if x == 'T' else z
    }

    def binOp(self, lst, func):
        tmp = self.run(lst[-1]) 
        if len(lst)==1:
            return tmp.value if hasattr(tmp, 'value') else tmp
        else:
            return func(tmp.value if hasattr(tmp, 'value') else tmp, self.binOp(lst[:-1], func))

    def specOp(self, lst, func):
        return func(*list(map(self.run, lst))).value


    def run(self, node):
        if isinstance(node, Node):

                if node.eval == 'BINOP':
                    return self.binOp(node.lst, self.eval[node.op.type])
                elif node.eval == 'SPECOP':
                    return self.specOp(node.lst, self.eval[node.op.type])
      
        return node
