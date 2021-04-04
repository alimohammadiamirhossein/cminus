class FileReader:
    def __init__(self, path):
        self.file = open(path, 'r', encoding='utf-8')
        self.backup_line = ""
        self.start_char = -1
        self.current_char = -1
        self.current_line = 0
        self.load_backup_line()
        self.is_last_line = False

    def load_backup_line(self):             # read next line and check if we are at end of file
        self.backup_line = self.file.readline()
        self.start_char = 0
        self.current_char = -1
        if self.backup_line != "":
            self.current_line += 1
        else:
            self.is_last_line = True

    def forward_read(self):
        if not self.is_last_line:
            self.current_char += 1
            return self.backup_line[self.current_char]

    def backward_read(self):
        self.current_char -= 1
        return self.backup_line[self.current_char]

    def return_token(self):
        start_index = self.start_char
        self.start_char = self.current_char + 1
        return self.backup_line[start_index:self.current_char+1]


# if __name__ == "__main__":
#     fr = FileReader(path="input.txt")
#     while not fr.is_last_line:
#         if fr.current_char == len(fr.backup_line) - 1:
#             fr.load_backup_line()
#         print(fr.forward_read(), end=" ")


#hello