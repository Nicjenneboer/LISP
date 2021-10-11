from src.Classes import *

#Return a node from an list of Tokens
def create_node(lst):
    if lst == []:
        return []
    eval = lst[0].eval
    if eval == 'BINOP':
        return OpNode(lst[0], lst[1:])
    elif eval == 'BOOL':
        return OpNode(lst[0], lst[1:])
    elif eval == 'PRINT':
        return OpNode(lst[0], lst[1:])
    elif eval == 'CONDITION':
        return conNode(lst[0], lst[1], lst[2:])
    elif eval == 'SETVAR':
        return SetVarNode(lst[0], lst[1], lst[2])
    elif eval == 'SETFUNC':
        return SetFuncNode(lst[0], lst[1], lst[2], lst[3:])
    elif eval == 'VAR':
        return varNode(lst)


    elif eval == 'NUMBER':
        return lst
    else:
        print(eval)
        print("ERROR")
        exit()


# Create a node from a list of tokens inside every depth brackets 
def create_nodes(tokens, depth=0, lst=[] ):
    if tokens[0].type == 'O_BRACKET':
        node, tokens, depth = create_nodes(tokens[1:], depth+1, lst=[])
        lst += [node]
    elif tokens[0].type == 'C_BRACKET':
        #if depth <= 0:
            #error.newError('Bracket Error', tokens[index].pos)
        return create_node(lst), tokens, depth-1
    else:
        return create_nodes(tokens[1:], depth, lst+[tokens[0]])
    if len(tokens) > 1:
        return create_nodes(tokens[1:], depth, lst)
    #if depth != 0:
        #self.error.newError('Bracket Error', tokens[index].pos)
    return initNode(lst)