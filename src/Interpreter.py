from os import lstat
from src.Parser import *
from src.Lexer import *
from src.functions import *
from src.Error import *

class VarTable():
    def __init__(self):
        self.table = {}

    def __str__(self):
        return str(self.table)
    
    def __repr__(self):
        return self.__str__()

    def setVar(self, id, val):
        self.table[id] = val

    def getVar(self, id):
        return self.table[id]
  

class Interpreter():
    def __init__(self, code):
        self.code = code
        self.error = error(code)
        self.lexer = Lexer(code, self.error)
        self.tokens = self.lexer.tokenize()
        self.parser = Parser(self.tokens, self.error)
        self.tree = self.parser.create_nodes()
        self.table = VarTable()
        

    def __str__(self):
        line = 'Lexer: \n'
        line += str(self.tokens) + '\n\n'
        line += 'Parser: \n'
        line += str(self.tree)
        return line

    eval = {
        #BINARY OPERATIONS
        'PLUS'  : lambda x,y: x + y,
        'MIN'   : lambda x,y: y - x,
        'MUL'   : lambda x,y: x * y,
        'DIV'   : lambda x,y: y / x,

        #BOOL OPERATIONS
        'EQUAL' : lambda x,y=None: 'NIL' if y == 'NIL' else x if y == x else 'NIL',
        'GREATER' : lambda x,y: 'NIL' if y == 'NIL' else x if y > x else 'NIL',
        'LESS' : lambda x,y: 'NIL' if y == 'NIL' else x if y < x else 'NIL',
        'GREATEROREQUAL' : lambda x,y: 'NIL' if y == 'NIL' else x if y >= x else 'NIL',
        'LESSOREQUAL' : lambda x,y: 'NIL' if y == 'NIL' else x if y <= x else 'NIL',

        #SPECIAL OPERATIONS
        'IF'    : lambda x,y,z=None: y if x == 'T' else z if z != None else 'NIL',
        'PRINT' : lambda x: print(x),
    }

    def binOp(self, lst, func):
        tmp = self.run(lst[-1])
        if hasattr(tmp, 'value') : tmp = tmp.value
        if len(lst)==1:
            return tmp
        return func(tmp, self.binOp(lst[:-1], func))

    def specOp(self, lst, func):
        tmp = func(*list(map(self.run, lst)))
        if hasattr(tmp, 'value') : tmp = tmp.value
        return tmp


    def run(self, node):
        if isinstance(node, Node):

            if node.eval == 'BINOP':
                return self.binOp(node.lst, self.eval[node.op.type])
            elif node.eval == 'BOOL':
                return 'NIL' if self.binOp(node.lst, self.eval[node.op.type]) == 'NIL' else 'T'
            elif node.eval == 'SPECOP':
                  return self.specOp(node.lst, self.eval[node.op.type])
            elif node.eval == 'SETVAR':
                return self.table.setVar(node.id.value, self.run(node.val))
            elif node.eval == 'SETFUNC':
                return self.table.setVar(node.id.value, node)
            elif node.eval == 'GET':
                return list(map(self.run, self.table.getVar(node.id.value).val))


        return node
