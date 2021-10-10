from src.Interpreter import *
import sys

def main(commandline=True, file=None):
    if commandline:
        print('LISTP COMMANDLINE INTERPRETER:\n')
        while True:
            code = input('lisp: ')
            preter = Interpreter(code)
            preter.run(preter.tree)
    else:
        f = open(file, 'r')
        code = f.read()
        preter = Interpreter(code)
        #print(preter)
        list(map(preter.run, preter.tree))
        #print(preter.run(preter.tree))



if __name__ == '__main__':

    main(len(sys.argv) == 1, sys.argv[1] if len(sys.argv) == 2 else None)