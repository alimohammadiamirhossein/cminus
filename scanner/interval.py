class Interval:
    def __init__(self):
        self.contains = []
        self.intervals = []

    def add_interval(self, first, last=None):
        if last is not None:
            self.intervals.append([first, last])
        else:
            self.intervals.append([first, first])

    def is_contain(self, char):
        for [first1, last1] in self.intervals:
            if first1 <= char <= last1:
                return True
        return False


class OtherTypeInterval:
    def __init__(self, just_valid_char=True):
        self.except_chars = []
        self.all_valid_chars = Interval()
        self.set_all_valid_char()
        self.just_valid_char = just_valid_char

    def add_except_chars(self, first, last=None):
        if last is not None:
            self.except_chars.append([first, last])
        else:
            self.except_chars.append([first, first])

    def is_contain(self, char):
        for [first1, last1] in self.except_chars:
            if first1 <= char <= last1:
                return False
        if self.just_valid_char:
            for [first1, last1] in self.all_valid_chars.intervals:
                if first1 <= char <= last1:
                    return True
            return False
        else:
            return True

    def set_all_valid_char(self):
        self.all_valid_chars.add_interval("0", "9")
        self.all_valid_chars.add_interval("a", "z")
        self.all_valid_chars.add_interval("A", "Z")
        self.all_valid_chars.add_interval(";")
        self.all_valid_chars.add_interval(":")
        self.all_valid_chars.add_interval(",")
        self.all_valid_chars.add_interval("[")
        self.all_valid_chars.add_interval("]")
        self.all_valid_chars.add_interval("(")
        self.all_valid_chars.add_interval(")")
        self.all_valid_chars.add_interval("{")
        self.all_valid_chars.add_interval("}")
        self.all_valid_chars.add_interval("+")
        self.all_valid_chars.add_interval("-")
        self.all_valid_chars.add_interval("*")
        self.all_valid_chars.add_interval("<")
        self.all_valid_chars.add_interval(">")
        self.all_valid_chars.add_interval("=")
        self.all_valid_chars.add_interval(" ")
        self.all_valid_chars.add_interval("\n")
        self.all_valid_chars.add_interval("\r")
        self.all_valid_chars.add_interval("\t")
        self.all_valid_chars.add_interval("\v")
        self.all_valid_chars.add_interval("\f")


