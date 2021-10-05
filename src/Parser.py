
class Node():
    def __init__(self, lst, eval):
        self.lst = lst
        self.eval = eval

    def __str__(self):
        line = 'opnode ' + self.op.type
        line += str(self.lst)
        return line

    def __repr__(self):
        return self.__str__()


class OpNode(Node):
    def __init__(self, op, lst):
        Node.__init__(self, lst, op.eval)
        self.op = op



class Parser():
    def __init__(self, tokens):
        self.tokens = tokens

    def create_node(self, lst):
        eval = lst[0].eval
        if eval == 'BINOP':
            return OpNode(lst[0], lst[1:])
        elif eval == 'BOOL':
            return OpNode(lst[0], lst[1:])
        elif eval == 'SPECOP':
            return OpNode(lst[0], lst[1:])
        else:
            print("ERRORRR")
            exit()


    def create_nodes(self, index=0, lst=[] ):
        if self.tokens[index].type == 'O_BRACKET':
            node, index = self.create_nodes(index+1, lst=[])
            lst += [node]
            if len(self.tokens) > index+1:
                return self.create_nodes(index+1, lst)
        elif self.tokens[index].type == 'C_BRACKET':
            return self.create_node(lst), index
        else:
            return self.create_nodes(index+1, lst+[self.tokens[index]])
        return node