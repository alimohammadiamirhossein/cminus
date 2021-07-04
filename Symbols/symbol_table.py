class Symbol:
    def __init__(self):
        self.symbol_table = ["if", "else", "void", "int", "while", "break", "switch",
                                  "default", "case", "return", "for"]
        self.IDs = []

    def add_symbol_to_symbol_table(self, token):
        if token not in self.symbol_table:
            self.symbol_table.append(token)
            tmp = ID(token)
            self.IDs.append(tmp)

    def write_symbol_table(self, file_):
        print("hello")
        str1_ = ""
        for i in range(len(self.symbol_table)):
            str1_ += f"{i+1}\t{self.symbol_table[i]}\n"
        file_.write(str1_)

    def find_symbol(self, token):
        for x in self.IDs:
            if x.token == token:
                return x
        return None



class ID:
    def __init__(self, token):
        self.token = token
        self.address = None


