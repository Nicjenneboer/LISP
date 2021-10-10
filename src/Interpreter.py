from os import lstat
from src.Parser import *
from src.Lexer import *
from src.Error import *

class Table():
    def __init__(self, error):
        self.error = error
        self.table = { 'var' : {}, 'func' : {}}

    def setVar(self, id, val, func=None):
        if func:
            self.table['func'][func]['args'][id] = val
        else:
            self.table['var'][id] = val

    def getVar(self, token):
        return self.table['var'][token.value]

    def getFuncVar(self, func):
            return self.table['func'][func]

    def setFunc(self, node):
        self.table['func'][node.id.value] = {'val' : node.val, 'args': {}}
        if node.args:
            args = list(enumerate(node.args))
            any(map(lambda x: self.setVar(x[0], x[1].id, node.id.value), args))

    def __add__(self, table):
        self.table['var'].update(table.table['var'])
        self.table['func'].update(table.table['func'])
        return self
        

    def __str__(self):
        return str(self.table)
    
    def __repr__(self):
        return self.__str__()


class Interpreter():
    def __init__(self, code):
        self.code = code
        self.error = error(code)
        self.lexer = Lexer(code, self.error)
        self.tokens = self.lexer.tokenize()
        self.parser = Parser(self.tokens, self.error)
        self.tree = self.parser.create_nodes()
        self.table = Table(self.error)
        

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

    def print(self, lst, func):
        tmp = func(*list(map(self.run, lst)))
        if hasattr(tmp, 'value') : tmp = tmp.value
        return tmp



    def run(self, node):
        if isinstance(node, Node):

            if node.eval == 'BINOP':
                tmp = self.binOp(node.lst, self.eval[node.op.type])
                return tmp
            elif node.eval == 'BOOL':
                return 'NIL' if self.binOp(node.lst, self.eval[node.op.type]) == 'NIL' else 'T'
            elif node.eval == 'PRINT':
                return self.print(node.lst, self.eval[node.op.type])
            elif node.eval == 'CONDITION':
                return self.run(self.eval[node.op.type](self.run(node.cond), node.lst[0], node.lst[1]))
            elif node.eval == 'SETVAR':
                return self.table.setVar(node.id.value, self.run(node.val))
            elif node.eval == 'SETFUNC':
                self.table.setFunc(node)
            elif node.eval == 'CALLFUNC':
                func = self.table.getFuncVar(node.id.value)
                prog = func['val']
                if node.args:
                    args = func['args']
                    backup = self.table
                    newtable = Table(self.error)
                    any(map(lambda x: newtable.setVar(args[x[0]], self.run(x[1])), list(enumerate(node.args))))
                    self.table += newtable
                    list(map(self.run, prog))
                    self.table = backup
                    return
                

                    
                    
            elif node.eval == 'EMPTY':
                print("EMPTY NODE")

        if isinstance(node, Token):
            if node.type == 'VAR':
                return self.table.getVar(node)


        return node
