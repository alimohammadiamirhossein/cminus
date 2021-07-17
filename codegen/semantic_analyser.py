class Semantic_writer:
    def __init__(self):
        self.file = open(f"semantic_check.txt", "w+")
        self.errors = []
        self.file_ = open(f"semantic_errors.txt", "w+")

    def writer(self):
        self.errors.append("")
        for i in range(len(self.errors)-1):
            if self.errors[i] == self.errors[i+1]:
                if self.errors[i+1].__contains__("is not defined"):
                    self.file_.write(self.errors[i])
                    self.file_.write("\n")
                else:
                    pass
            else:
                self.file_.write(self.errors[i])
                self.file_.write("\n")
            # self.file_.write(x)
            # self.file_.write("\n")
        # self.file_.close()
        # if len(self.errors) == 0:
        #     pass


    def add_error(self, str1):
        self.errors.append(str1)