class FileWriter:
    def __init__(self):
        self.address = "lexical_errors.txt"
        file_ = open(self.address, "w+")
        file_.close()

    def lexical_errors(self, lineNumber, errorType, errorToken):
        file = open(self.address, "a")
        str_ = ""
        str_ += f"{lineNumber}.\t({errorToken}, {errorType})\n"
        file.write(str_)
        file.close()
