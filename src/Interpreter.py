from src.Classes import *


# LAMBDA FUNCTIONS FOR OPERATIONS
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

# Recursive binary operations for a list
def binOp(lst: List[Token], func: eval, stack: Stack) -> int:
    tmp = run(lst[-1], stack)
    if hasattr(tmp, 'value') : tmp = tmp.value
    if len(lst)==1:
        return tmp
    return func(tmp, binOp(lst[:-1], func, stack))

# Execute a list of nodes
def init(nodes: List[Node], stack: Stack):
    if len(nodes) == 1:
        return [run(nodes[0], stack)]
    return [run(nodes[0], stack)] + init(nodes[1:], stack)

# Execute node and all child nodes
def run(node: Node, stack=Stack()):
    if isinstance(node, Node):
        
        # First node
        if node.eval == 'INIT':
            return init(node.lst, stack)
        # Binary operation node
        elif node.eval == 'BINOP':
            return binOp(node.lst, eval[node.op.type], stack)
        # Bool operation node
        elif node.eval == 'BOOL':
            return 'NIL' if  binOp(node.lst, eval[node.op.type], stack) == 'NIL' else 'T'
        # Print node
        elif node.eval == 'PRINT':
            return eval[node.op.type](*init(node.lst, stack))
        # Condition node
        elif node.eval == 'CONDITION':
            return run(eval[node.op.type](run(node.cond, stack), node.lst[0], node.lst[1]), stack)

        # Define variable
        elif node.eval == 'SETVAR':
            return stack.varadd(node.id.value, run(node.val, stack))

        # Define function
        elif node.eval == 'SETFUNC':
            return stack.funcadd(node.id.value, node.args, node.val)

        # Execute funtion
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
                        # Set function variables in stack
                        list(map(lambda x,y: stack.varadd(x.value, run(y, stack)), args, node.lst[1:]))
            tmp = init(func[1], stack)
            if args:
                # Remove function variables from stack
                stack.removevar(len(args))
            return tmp[0]
                    
     
        elif node.eval == 'EMPTY':
            print("EMPTY NODE")

    elif isinstance(node, Token):
        if node.type == 'VAR':
            return stack.varget(node.value)

    return node
