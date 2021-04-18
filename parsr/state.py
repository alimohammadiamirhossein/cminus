class State:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Terminal(State):
    def __init__(self, name):
        super().__init__(name)


class NonTerminal(State):
    def __init__(self, name, first=[], follow=[]):
        super().__init__(name)
        self.firsts = first
        self.follows = follow

    @classmethod
    def get_next_state(cls, token):
        if token[1] == 'KEYWORD':
            name = token[2]
        else:
            name = token[1]
