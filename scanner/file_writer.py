class FileWriter:
    def __init__(self):
        file_ = open("lexical_errors.txt", "w+")
        file_.close()
        file_ = open("token.txt", "w+")
        file_.close()
        self.token_str = ""
        self.token_line = 0

    @classmethod
    def lexical_errors(cls, lineNumber, errorType, errorToken):
        file = open("lexical_errors.txt", "a")
        str_ = ""
        str_ += f"{lineNumber}.\t({errorToken}, {errorType})\n"
        file.write(str_)
        file.close()

    def tokens_writer(self, line_number, current_state, token):
        if self.token_line < line_number:
            file_ = open("token.txt", "a")
            file_.write(self.token_str[0:len(self.token_str)-1])
            file_.close()
            self.token_line = line_number
            if line_number != 1:
                self.token_str = f"\n{line_number}.\t"
            else:
                self.token_str = f"{line_number}.\t"

        self.token_str += f"({current_state}, {token}) "








