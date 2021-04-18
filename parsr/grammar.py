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

