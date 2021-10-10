from src.Interpreter import *
import sys

def main():
    f = open('test.lsp', 'r')
    code = f.read()
    preter = Interpreter(code)
    list(map(preter.run, preter.tree))



if __name__ == '__main__':

    main()