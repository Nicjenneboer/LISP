from src.Parser import *
from src.Lexer import *
from src.functions import *



class Interpreter():
    def __init__(self, code):
        self.code = code
        self.lexer = Lexer(code)
        self.parser = Parser(self.lexer.tokenize())
        self.tree = self.parser.create_nodes()

    eval = {
        'PLUS'  : lambda x,y: x + y,
        'MIN'   : lambda x,y: y - x,
        'MUL'   : lambda x,y: x * y,
        'DIV'   : lambda x,y: y / x,
        'EQUAL' : lambda x,y: 'T' if y == x else 'NIL', # NEED FIX FOR MORE VALUES
        'IF'    : lambda x,y,z: y if x == 'T' else z
    }

    def exec(self, lst, func):
        if isinstance(lst[-1], Node):
            return func(self.run(lst[-1]), self.exec(lst[:-1], func))
        if len(lst)==1:
            return lst[0].value
        else:
            return func(lst[-1].value, self.exec(lst[:-1], func))

    def execop(self, lst, func):
        return func(self.run(lst[0]), self.run(lst[1]), self.run(lst[2]))

    def run(self, node):
        if isinstance(node, OpNode):
            return self.exec(node.lst, self.eval[node.op.type])
        elif isinstance(node, KeyNode):
            return self.execop(node.lst, self.eval[node.op.type])
        return node
