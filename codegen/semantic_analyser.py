class Semantic_writer:
    def __init__(self):
        self.file = open(f"semantic_check.txt", "w+")
        self.errors = []
        self.file_ = open(f"semantic_errors.txt", "w+")


    def writer(self):
        for x in self.errors:
            self.file_.write(x)
            self.file_.write("\n")
        self.file_.close()
        if len(self.errors) == 0:
            pass


    def add_error(self, str1):
        self.errors.append(str1)