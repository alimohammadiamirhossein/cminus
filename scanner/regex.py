from scanner.state import State, FinalState
from scanner.interval import Interval, OtherTypeInterval


class Regex:
    def __init__(self):
        self.state_zero = State("0")
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
        state1 = State("3")
        state2 = FinalState("4", True)
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
        state1 = State("1")
        state2 = FinalState("2", True)
        inter1 = Interval()
        inter2 = Interval()
        inter3 = OtherTypeInterval()
        inter1.add_interval("a", "z")
        inter1.add_interval("A", "Z")
        inter2.add_interval("a", "z")
        inter2.add_interval("A", "Z")
        inter2.add_interval("0", "9")
        inter3.add_except_chars("a", "z")
        inter3.add_except_chars("A", "Z")
        inter3.add_except_chars("0", "9")
        self.state_zero.add_next_state(inter1, state1)
        state1.add_next_state(inter2, state1)
        state1.add_next_state(inter3, state2)

    def symbol(self):
        state5 = FinalState("5", False)
        state6 = State("6")
        state7 = FinalState("7", False)
        state8 = State("8")
        state9 = FinalState("9", True)
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
        inter1.add_interval("<")
        self.state_zero.add_next_state(inter1, state5)
        inter2 = Interval()
        inter2.add_interval("=")
        self.state_zero.add_next_state(inter2, state6)
        state6.add_next_state(inter2, state7)
        inter3 = Interval()
        inter3.add_interval("*")
        self.state_zero.add_next_state(inter3, state8)
        other3 = OtherTypeInterval()
        other3.add_except_chars("/")
        state8.add_next_state(other3, state9)

    def comment(self):
        ...

    def whitespace(self):
        ...

# hello
