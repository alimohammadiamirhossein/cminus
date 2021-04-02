from scanner.interval import Interval


class State:
    def __init__(self, char):
        self.next_states = []
        self.stateID = char

    def add_next_state(self, interval, next_state):
        self.next_states.append([interval, next_state])

    def get_next_state(self, char):
        for [interval1, next1] in self.next_states:
            if interval1.is_contain(char):
                return next1
        return ErrorState("e1")

    def __str__(self):
        return self.stateID


class FinalState(State):
    def __init__(self, char, backward):
        super().__init__(char)
        self.backward = backward

    def is_backward(self):
        return self.backward

    def __str__(self):
        if self.stateID == "2":
            return "KEYWORD"
        elif self.stateID == "4":
            return "NUM"
        elif self.stateID == "5" or self.stateID == "7" or self.stateID == "9":
            return "SYMBOL"


class ErrorState(State):
    def __init__(self, char):
        super().__init__(char)

    def typeError(self):
        if self.stateID == "e1":
            print("Invalid input")
        if self.stateID == "e2":
            print("Unclosed comment")
        if self.stateID == "e3":
            print("Unmatched comment")
        if self.stateID == "e4":
            print("Invalid number")
