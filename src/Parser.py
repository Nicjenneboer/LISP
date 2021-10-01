
class Node():
    pass

    def __str__(self):
        return('opnode ' + self.op.type)

    def __repr__(self):
        return self.__str__()

class OpNode(Node):
    def __init__(self, op, lst):
        self.op = op
        self.lst = lst

class Parser():
    def __init__(self, tokens):
        self.tokens = tokens

    def create_node(self, lst):
        if lst[0].type in ['PLUS', 'MIN', 'MUL', 'DIV']:
            return OpNode(lst[0], lst[1:])
        else:
            print("ERRORRR")


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