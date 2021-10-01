class Parser():
    def __init__(self, tokens):
        self.tokens = tokens

    def make_lst(self, index=0, lst=[]):
        if self.tokens[index].type == 'O_BRACKET':
            tmp_lst, index = self.make_lst(index+1, lst=[])
            lst += [tmp_lst]
            if len(self.tokens) > index+1:
                return self.make_lst(index+1, lst)
        elif self.tokens[index].type == 'C_BRACKET':
            return lst, index
        else:
            return self.make_lst(index+1, lst+[self.tokens[index]])
        return lst
