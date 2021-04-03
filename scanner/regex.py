from scanner.state import State, FinalState, ErrorState
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

    # error state
    # def first_char(self):
    #     state_e1 = ErrorState("e1")
    #     other = OtherTypeInterval()
    #     self.state_zero.add_next_state(other.all_valid_chars, state_e1)

    def number(self):
        state3 = State("3")
        state4 = FinalState("4", True)
        tmp = Interval()
        tmp.add_interval("0", "9")
        self.state_zero.add_next_state(tmp, state3)
        state3.add_next_state(tmp, state3)
        interval_state1 = OtherTypeInterval()
        interval_state1.add_except_chars("a", "z")
        interval_state1.add_except_chars("A", "Z")
        interval_state1.add_except_chars("0", "9")
        state3.add_next_state(interval_state1, state4)
        self.states.append(state3)
        self.states.append(state4)
        # error state
        state_e4 = ErrorState("e4")
        inter3 = Interval()
        inter3.add_interval("a", "z")
        inter3.add_interval("A", "Z")
        state3.add_next_state(inter3, state_e4)

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
        inter2 = Interval()
        inter2.add_interval("=")
        inter3 = Interval()
        inter3.add_interval("*")
        other3 = OtherTypeInterval()
        other3.add_except_chars("/")
        other4 = OtherTypeInterval()
        other4.add_except_chars("=")
        self.state_zero.add_next_state(inter1, state5)
        self.state_zero.add_next_state(inter2, state6)
        self.state_zero.add_next_state(inter3, state8)
        state6.add_next_state(inter2, state7)
        state6.add_next_state(other4, state9)
        state8.add_next_state(other3, state9)
        # error state
        state_e3 = ErrorState("e3")
        inter4 = Interval()
        inter4.add_interval("/")
        state8.add_next_state(inter4, state_e3)

    def comment(self):
        state_a = State("a")
        state_b = State("b")
        state_c = FinalState("c", False)
        state_d = State("d")
        state_e = State("e")
        inter1 = Interval()
        inter2 = Interval()
        inter3 = Interval()
        other3 = OtherTypeInterval()
        other4 = OtherTypeInterval()
        other5 = OtherTypeInterval()
        inter1.add_interval("/")
        inter2.add_interval("*")
        inter3.add_interval("\n")
        other3.add_except_chars("\n")
        other3.add_except_chars("EOF")
        other4.add_except_chars("*")
        other4.add_except_chars("EOF")
        other5.add_except_chars("/")
        other5.add_except_chars("*")
        other5.add_except_chars("EOF")
        self.state_zero.add_next_state(inter1, state_a)
        state_a.add_next_state(inter1, state_b)
        state_a.add_next_state(inter2, state_d)
        state_b.add_next_state(inter3, state_c)
        state_b.add_next_state(other3, state_b)
        state_d.add_next_state(other4, state_d)
        state_d.add_next_state(inter2, state_e)
        state_e.add_next_state(inter2, state_e)
        state_e.add_next_state(other5, state_d)
        state_e.add_next_state(inter1, state_c)
        # error state
        state_e2 = ErrorState("e2")
        interval = Interval()
        interval.add_interval("EOF") #EOF
        state_b.add_next_state(interval, state_e2)
        state_d.add_next_state(interval, state_e2)
        state_e.add_next_state(interval, state_e2)

    def whitespace(self):
        state_f = FinalState("f", False)
        inter1 = Interval()
        inter1.add_interval(" ")
        inter1.add_interval("\n")
        inter1.add_interval("\r")
        inter1.add_interval("\t")
        inter1.add_interval("\v")
        inter1.add_interval("\f")
        self.state_zero.add_next_state(inter1, state_f)

# hello
