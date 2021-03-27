class FileReader:
    def __init__(self, path):
        self.file = open(path, 'r')
        self.backup_line = ""
        self.current_char = -1
        self.current_line = -1
        self.load_backup_line()
        self.is_last_line = False

    def load_backup_line(self):
        self.backup_line = self.file.readline()
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


# if __name__ == "__main__":
#     fr = FileReader(path="input.txt")
#     while not fr.is_last_line:
#         if fr.current_char == len(fr.backup_line) - 1:
#             fr.load_backup_line()
#         print(fr.forward_read(), end=" ")

