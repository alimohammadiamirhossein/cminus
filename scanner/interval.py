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


class Other:
    def __init__(self):
        self.except_chars = []
        self.all_valid_chars = Interval()

    def add_except_chars(self, first, last=None):
        if last is not None:
            self.expects.append([first, last])
        else:
            self.expects.append([first, first])

    def is_contain(self, char):
        for [first1, last1] in self.except_chars:
            if first1 <= char <= last1:
                return False

    def set_all_valid_char(self):
        self.all_valid_chars.add_interval("0", "9")
