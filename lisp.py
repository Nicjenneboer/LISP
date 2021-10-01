from src.Interpreter import *

def main():
    f = open('test.lsp', 'r')
    code = f.read()
    preter = Interpreter(code)
    print(preter.ast)


if __name__ == '__main__':
    main()
