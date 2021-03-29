from scanner.interval import Interval
class State:
    def __init__(self):
        self.next_states = []

    def add_next_state(self, interval, next_state):
        self.next_states.append([interval, next_state])

    def get_next_state(self, char):
        for [interval1, next1] in self.next_states:
            if interval1.is_contain(char):
                return next1


class FinalState(State):
    def __init__(self, backward):
        super().__init__()
        self.backward = backward

