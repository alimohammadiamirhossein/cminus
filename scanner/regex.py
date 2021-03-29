from scanner.state import State, FinalState
from scanner.interval import Interval


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
        interval_state1 = Interval()
        interval_state1.expect("a", "z")
        interval_state1.expect("A", "Z")
        interval_state1.expect("0", "9")
        state1.add_next_state(interval_state1, state2)
        self.states.append(state1)
        self.states.append(state2)

    def ID_keyword(self):
        ...

    def symbol(self):
        state5 = FinalState()
        state6 = State()
        state7 = FinalState()
        state8 = State()
        state9 = FinalState()


    def comment(self):
        ...

    def whitespace(self):
        ...



# hello 