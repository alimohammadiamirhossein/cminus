class Interval:
    def __init__(self):
        self.contains = []
        self.expects = []
        self.intervals = []
        self.expects = []

    def add_interval(self, first, last=None):
        if last is not None:
            self.intervals.append([first, last])
        else:
            self.intervals.append([first, first])

    def expect(self, first, last=None):
        if last is not None:
            self.expects.append([first, last])
        else:
            self.expects.append([first, first])

    def is_contain(self, char):
        # for [first1, last1] in self.intervals:
        #     if first1 <= char <= last1:
        #         return True
        # for [first1, last1] in self.expects:
        #     if first1 <= char <= last1:
        #         return False
        return True


