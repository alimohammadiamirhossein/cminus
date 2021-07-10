class Semantic_writer:
    def __init__(self):
        self.file = open(f"semantic_check.txt", "w+")
        self.errors = []

    def writer(self):
        for x in self.errors:
            print(x)

    def add_error(self, str1):
        self.errors.append(str1)