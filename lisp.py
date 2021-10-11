from src.Lexer import *
from src.Parser import *
from src.Interpreter import *

def main():
    f = open('test.lsp', 'r')
    code = f.read()
    tokens = tokenize(code)
    tree = create_nodes(tokens)
    run(tree)



if __name__ == '__main__':

    main()