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


class FinalState(State):
    def __init__(self, char, backward):
        super().__init__(char)
        self.backward = backward


class ErrorState(State):
    def __init__(self):
        super().__init__()

