from src.Classes import *



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

def binOp(lst, func, stack):
    tmp = run(lst[-1], stack)
    if hasattr(tmp, 'value') : tmp = tmp.value
    if len(lst)==1:
        return tmp
    return func(tmp, binOp(lst[:-1], func, stack))

def init(nodes, stack):
    if len(nodes) == 1:
        return [run(nodes[0], stack)]
    return [run(nodes[0], stack)] + init(nodes[1:], stack)


def run(node, stack=Stack()):
    if isinstance(node, Node):

        if node.eval == 'INIT':
            return init(node.lst, stack)

        elif node.eval == 'BINOP':
            return binOp(node.lst, eval[node.op.type], stack)
        elif node.eval == 'BOOL':
            return 'NIL' if  binOp(node.lst, eval[node.op.type], stack) == 'NIL' else 'T'
        elif node.eval == 'PRINT':
            return eval[node.op.type](*init(node.lst, stack))
        elif node.eval == 'CONDITION':
            return run(eval[node.op.type](run(node.cond, stack), node.lst[0], node.lst[1]), stack)

        elif node.eval == 'SETVAR':
            return stack.varadd(node.id.value, run(node.val, stack))


        elif node.eval == 'SETFUNC':
            return stack.funcadd(node.id.value, node.args, node.val)


        elif node.eval == 'VAR':

            func = stack.funcget(node.lst[0].value)
            if func == "func not exist": print('func not exist')
            args = []
            if func[0] or len(node.lst) > 1:
                if not func[0]:
                    print('To many args')
                else:
 
                    args = func[0].lst
                    if len(args) > len(node.lst)-1:
                        print('To few args')
                    elif len(args) < len(node.lst)-1:
                        print('To many args')
                    else:
                        list(map(lambda x,y: stack.varadd(x.value, run(y, stack)), args, node.lst[1:]))
            tmp = init(func[1], stack)
            if args:
                stack.removevar(len(args))
            return tmp[0]
                    
     
        elif node.eval == 'EMPTY':
            print("EMPTY NODE")

    if isinstance(node, Token):
        if node.type == 'VAR':
            return stack.varget(node.value)


    return node
