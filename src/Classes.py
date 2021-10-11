from typing import List

#TOKEN CLASSES

class Token():
    def __init__(self, type, eval, value, pos):
        self.type = type
        self.eval = eval
        self.value = value
        self.pos = pos


    def __str__(self):
        return self.type + ' ' + str(self.value)

    def __repr__(self):
        return self.__str__()


class Pos():
    def __init__(self, row=0, index=0):
        self.row = row
        self.index = index

    def __str__(self):
        return str((self.row, self.index))

    def __repr__(self):
        return self.__str__()

# NODE CLASSES

class Node():
    def __init__(self, eval: str):
        self.eval = eval

    def __str__(self) -> str:
        return self.eval

    def __repr__(self) -> str:
        return self.__str__()


class OpNode(Node):
    def __init__(self, op: Token, lst: List[Token]):
        Node.__init__(self, op.eval)
        self.lst = lst
        self.op = op

class conNode(Node):
    def __init__(self, op: Token, cond: Token, lst: List[Token]):
        Node.__init__(self, op.eval)
        self.op = op
        self.cond = cond
        self.lst = lst
    
class SetVarNode(Node):
    def __init__(self, op: Token, id: Token, val: Token):
        Node.__init__(self, op.eval)
        self.op = op
        self.id = id
        self.val = val

class varNode(Node):
    def __init__(self, lst: List[Token]):
        Node.__init__(self, 'VAR')
        self.op = 'VAR'
        self.lst = lst

    def __str__(self):
        return str(self.lst)

    def __repr__(self):
        return self.__str__()

class SetFuncNode(Node):
    def __init__(self, op: Token, id: Token, args: List[Token], val: Token):
        Node.__init__(self, op.eval)
        self.op = op
        self.id = id
        self.args = args
        self.val = val

    def __str__(self):
        return str(self.id.value) + ' ' + str(self.args) + ' ' + str(self.val)

    def __repr__(self):
        return self.__str__()

class FuncNode(Node):

    def __init__(self, id: Token, args: List[Token] = None):
        Node.__init__(self, 'CALLFUNC')
        self.id = id
        self.args = args


    def __str__(self):
        return 'FUNC ' + str(self.id.value) + ' ' + str(self.args)

    def __repr__(self):
        return self.__str__()

class initNode(Node):

    def __init__(self, lst: List[Node]):
        Node.__init__(self, 'INIT')
        self.lst = lst





# STACK CLASS


class Stack():
    def __init__(self):
        self.varlst = []   
        self.varindex = 0
        self.funclst = []   
        self.funcindex = 0

    def varadd(self, id, val):
        self.varlst += [(id, val)]
        self.varindex += 1

    def varget(self, id, index=0):
        if index == self.varindex:
            return 'Var not exist'
        elif self.varlst[-1-index][0] == id:
            return self.varlst[-1-index][1]
        return self.varget(id, index+1)
    
    def removevar(self, x=1):
        self.varlst = self.varlst[:-x]
        self.varindex -= x

    def funcadd(self, id, args, val):
        self.funclst += [(id, args, val)]
        self.funcindex += 1

    def funcget(self, id, index=0):
        if index == self.funcindex:
            return 'func not exist'
        elif self.funclst[-1-index][0] == id:
            return self.funclst[-1-index][1:]
        return self.funcget(id, index+1)