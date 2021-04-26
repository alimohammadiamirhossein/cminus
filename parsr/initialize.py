from parsr.state import State, Terminal, NonTerminal


class Initializer:
    def __init__(self):
        self.terminals = []
        self.non_terminals = []
        self.terminals.append(Terminal("while"))
        self.terminals.append(Terminal("("))
        self.terminals.append(Terminal(")"))
        self.terminals.append(Terminal("do"))
        self.terminals.append(Terminal("{"))
        self.terminals.append(Terminal("}"))
        self.terminals.append(Terminal(";"))
        self.terminals.append(Terminal("=="))
        self.terminals.append(Terminal("!="))
        self.terminals.append(Terminal("id"))
        self.terminals.append(Terminal("="))
        self.terminals.append(Terminal("ε"))
        self.terminals.append(Terminal("$"))
        self.non_terminals.append(NonTerminal("S"))
        self.non_terminals.append(NonTerminal("A"))
        self.non_terminals.append(NonTerminal("Y"))
        self.non_terminals.append(NonTerminal("X"))
        self.non_terminals.append(NonTerminal("Z"))
        self.non_terminals.append(NonTerminal("ST"))

    def find_state(self, name):
        for k in self.terminals:
            if k.name == name:
                return k
        for k in self.non_terminals:
            if k.name == name:
                return k
        return -1

