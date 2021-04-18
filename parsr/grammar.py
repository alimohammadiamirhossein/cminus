from parsr.state import State, Terminal, NonTerminal


class Grammar:
    def __init__(self, patch, initializer):
        self.initializer = initializer
        file = open(patch, 'r', encoding='utf-8')
        line_ = "a"
        self.dict_ = {}
        while line_ != "":
            line_ = file.readline()
            names = line_.split()
            index = 3
            scenario = []
            while index < len(names):
                if names[index] != "|":
                    scenario.append(names[index])
                index += 1
                if index == len(names) or names[index] == "|":
                    sc = self.make_scenario(scenario)
                    if self.dict_.get(names[1]) is None:
                        self.dict_[names[1]] = [sc]
                    else:
                        self.dict_[names[1]].append(sc)
                    scenario = []

    def make_scenario(self, scenario):
        states = []
        for i in range(len(scenario)):
            a = self.initializer.find_state(scenario[i])
            states.append(a)
        return states

    '''need to check     probably have bug'''
    def match(self, token_name, current_scenario):
        for i in range(len(self.dict_[current_scenario])):
            scenario_next = self.dict_[current_scenario][i]
            if isinstance(scenario_next, Terminal):
                if token_name == scenario_next.name:
                    print("Match")
            elif isinstance(scenario_next, NonTerminal):
                if scenario_next.is_in_first(token_name):
                    return scenario_next
        print('error')

