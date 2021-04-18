from parsr.state import State, Terminal, NonTerminal


class Initializer:
    def __init__(self):
        self.terminals = []
        self.non_terminals = []
        self.terminals.append(Terminal("ID"))
        self.non_terminals.append(NonTerminal("Program"))

    def find_state(self, name):
        for k in self.terminals:
            if k.name == name:
                return k
        for k in self.non_terminals:
            if k.name == name:
                return k
        return -1

