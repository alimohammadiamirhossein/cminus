class FileWriter:
    def __init__(self):
        self.directory_adress = "C:/Users/samen/Desktop/comp-fin/cminus/report/scanner/"
        file_ = open(f"{self.directory_adress}lexical_errors.txt", "w+")
        file_.close()
        file_ = open(f"{self.directory_adress}token.txt", "w+")
        file_.close()
        self.lexical_str = ""
        self.lexical_line = 0
        self.token_str = ""
        self.token_line = 0
        self.symbol_tables = ["if", "else", "void", "int", "while", "break", "switch",
                                  "default", "case", "return", "for"]

    def add_symbol_to_symbol_table(self, token):
        if token not in self.symbol_tables:
            self.symbol_tables.append(token)

    def write_symbol_table(self):
        file_ = open(f"{self.directory_adress}symbol_table.txt", "w+")
        str1_ = ""
        for i in range(len(self.symbol_tables)):
            str1_ += f"{i+1}\t{self.symbol_tables[i]}\n"
        file_.write(str1_)
        file_.close()

    def lexical_errors(self, lineNumber, errorType, errorToken):
        if lineNumber > self.lexical_line:
            if self.lexical_line == 0:
                self.lexical_str += f"{lineNumber}.\t({errorToken}, {errorType})"
            else:
                self.lexical_str += f"\n{lineNumber}.\t({errorToken}, {errorType})"
            self.lexical_line = lineNumber
        else:
            self.lexical_str += f" ({errorToken}, {errorType})"

    def lexical_error_write(self):
        file = open(f"{self.directory_adress}lexical_errors.txt", "w")
        file.write(self.lexical_str)
        if self.lexical_str == "":
            file.write("There is no lexical error.")
        self.lexical_str = ""
        file.close()

    def tokens_writer(self, line_number, current_state, token):
        if self.token_line < line_number:
            file_ = open(f"{self.directory_adress}token.txt", "a")
            file_.write(self.token_str[0:len(self.token_str)-1])
            file_.close()
            if self.token_line != 0:
                self.token_str = f"\n{line_number}.\t"
            else:
                self.token_str = f"{line_number}.\t"
            self.token_line = line_number

        self.token_str += f"({current_state}, {token}) "
#amirhossein
