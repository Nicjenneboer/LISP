from src.Interpreter import *
import sys

def main(commandline=True, file=None):
    if commandline:
        while True:
            code = input('lisp: ')
            preter = Interpreter(code)
            print(preter.ast)
            code = ''
    else:
        f = open(file, 'r')
        code = f.read()
        preter = Interpreter(code)
        print(preter.ast)



if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    else:
        main(False, sys.argv[1])