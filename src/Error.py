class error():
    def __init__(self, code):
        self.code = code
        self.errors = []

    def newError(self, string, pos):
        self.errors += [[string, pos]]

    def print(self, error):
        return error[0] + ': line ' + str(error[1].row) + '\n' + self.code.split('\n')[error[1].row] + '\n' + (' ' * error[1].index ) + '^'

    def __str__(self):
        return '\n'.join(list(map(self.print, self.errors)))
    
    def __repr__(self):
        return self.__str__()