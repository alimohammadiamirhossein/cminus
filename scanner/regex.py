from scanner.state import State, FinalState
from scanner.interval import Interval, OtherTypeInterval


class Regex:
    def __init__(self):
        self.state_zero = State()
        self.states = [self.state_zero]
        self.number()
        self.ID_keyword()
        self.whitespace()
        self.symbol()
        self.comment()

    def set_all_chars(self):
        self.all_characters.add_interval("0", "9")
        self.all_characters.add_interval("")

    def number(self):
        state1 = State()
        state2 = FinalState(True)
        tmp = Interval()
        tmp.add_interval("0", "9")
        self.state_zero.add_next_state(tmp, state1)
        state1.add_next_state(tmp, state1)
        interval_state1 = OtherTypeInterval()
        interval_state1.add_except_chars("a", "z")
        interval_state1.add_except_chars("A", "Z")
        interval_state1.add_except_chars("0", "9")
        state1.add_next_state(interval_state1, state2)
        self.states.append(state1)
        self.states.append(state2)

    def ID_keyword(self):
        ...

    def symbol(self):
        state5 = FinalState(False)
        state6 = State()
        state7 = FinalState(False)
        state8 = State()
        state9 = FinalState(True)
        inter1 = Interval()
        inter1.add_interval(";")
        inter1.add_interval(":")
        inter1.add_interval(",")
        inter1.add_interval("[")
        inter1.add_interval("]")
        inter1.add_interval("(")
        inter1.add_interval(")")
        inter1.add_interval("{")
        inter1.add_interval("}")
        inter1.add_interval("+")
        inter1.add_interval("-")
        inter1.add_interval("*")
        inter1.add_interval("<")
        inter1.add_interval(">")
        self.state_zero.add_next_state(inter1, state5)



    def comment(self):
        ...

    def whitespace(self):
        ...



# hello 