
class Node():
    def __init__(self, eval):
        self.eval = eval

    def __str__(self):
        return self.eval

    def __repr__(self):
        return self.__str__()


class OpNode(Node):
    def __init__(self, op, lst):
        Node.__init__(self, op.eval)
        self.lst = lst
        self.op = op
    
class SetVarNode(Node):
    def __init__(self, op, id, val):
        Node.__init__(self, op.eval)
        self.op = op
        self.id = id
        self.val = val

class SetFuncNode(Node):
    def __init__(self, op, id, args, *val):
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
    def __init__(self, id, args):
        Node.__init__(self, id.eval)
        self.id = id
        self.args = args

    def __str__(self):
        return str(self.id.value) + ' ' + str(self.id.value)

    def __repr__(self):
        return self.__str__()


class Parser():
    def __init__(self, tokens, error):
        self.tokens = tokens
        self.error = error

    def create_node(self, lst):
        if lst == []:
            return Node('EMPTY')
        eval = lst[0].eval
        if eval == 'BINOP':
            return OpNode(lst[0], lst[1:])
        elif eval == 'BOOL':
            return OpNode(lst[0], lst[1:])
        elif eval == 'SPECOP':
            return OpNode(lst[0], lst[1:])
        elif eval == 'SETVAR':
            return SetVarNode(lst[0], lst[1], lst[2])
        elif eval == 'SETFUNC':
            return SetFuncNode(lst[0], lst[1], lst[2], *lst[3:])
        elif eval == 'GET':
            return FuncNode(lst[0], lst[1:])
        elif eval == 'NUMBER':
            return lst
        else:
            print("ERRORRR2")
            exit()


    def create_nodes(self, index=0, depth=0, lst=[] ):
        if self.tokens[index].type == 'O_BRACKET':
            node, index, depth = self.create_nodes(index+1, depth+1, lst=[])
            lst += [node]
        elif self.tokens[index].type == 'C_BRACKET':
            if depth <= 0:
                self.error.newError('Bracket Error', self.tokens[index].pos)
            return self.create_node(lst), index, depth-1
        else:
            return self.create_nodes(index+1, depth, lst+[self.tokens[index]])
        if len(self.tokens) > index+1:
            return self.create_nodes(index+1, depth, lst)
        if depth != 0:
            self.error.newError('Bracket Error', self.tokens[index].pos)
        return lst