from parsr.state import State, Terminal, NonTerminal


class Grammar:
    def __init__(self, patch, initializer):
        self.initializer = initializer
        self.grammar_file = open(patch+'grammar.txt', 'r', encoding='utf-8')
        self.grammar_rules = {}
        self.firsts_rules = {}
        self.follows_rules = {}
        self.parse_table = {}
        self.grammar_file_reader()
        self.first_or_follow_reader(patch+'first.txt', True)
        self.first_or_follow_reader(patch + 'follow.txt', False)
        self.make_parse_table()
        print(self.parse_table)

    def first_or_follow_reader(self, patch1, is_first):
        x1 = {}
        file1 = open(patch1, 'r', encoding='utf-8')
        line1 = "a"
        while line1 != "":
            line1 = file1.readline()
            attributes = line1.split()
            if len(attributes) < 2:
                continue
            if x1.get(attributes[0]) is None:
                x1[attributes[0]] = attributes[2:]
            else:
                for i in range(1, len(attributes)):
                    x1[attributes[0]].append(attributes[i])
        file1.close()
        if is_first:
            self.firsts_rules = x1
        else:
            self.follows_rules = x1

    def epsilon_check(self, params):
        index1 = 0
        while index1 < len(params):
            if self.is_in_first('ε', params[index1]):
                index1 += 1
            else:
                break
        if index1 == len(params) and len(params) > 0:
            return True
        return False

    def is_in_first_for_multi_parameters(self, token1, parameters1):
        index1 = 0
        while index1 < len(parameters1):
            if self.is_in_first(token1, parameters1[index1]):
                return True
            elif self.is_in_first('ε', parameters1[index1]):
                index1 += 1
            else:
                break
        return False

    def is_in_first(self, token1, parameter1):
        if isinstance(self.initializer.find_state(parameter1), Terminal):
            if token1 == parameter1:
                return True
        elif token1 in self.firsts_rules[parameter1]:
            return True
        return False

    def is_in_follow(self, token1, parameter1):
        if token1 in self.follows_rules[parameter1]:
            return True
        return False

    def grammar_file_reader(self):
        line_ = "a"
        while line_ != "":
            line_ = self.grammar_file.readline()
            names = line_.split()
            index = 2
            scenario = []
            while index < len(names):
                if names[index] != "|":
                    scenario.append(names[index])
                index += 1
                if index == len(names) or names[index] == "|":
                    if self.grammar_rules.get(names[0]) is None:
                        self.grammar_rules[names[0]] = [scenario]
                    else:
                        self.grammar_rules[names[0]].append(scenario)
                    scenario = []

    def make_parse_table(self): #it probably have bug
        for A in self.initializer.non_terminals:
            if self.parse_table.get(A.name) is None:
                self.parse_table[A.name] = {}
            for a in self.initializer.terminals:
                if a.name == 'ε':
                    continue
                for x in self.grammar_rules[A.name]:
                    if x == ['ε']:
                        continue
                    if self.is_in_first_for_multi_parameters(a.name, x):
                        self.parse_table[A.name][a.name] = self.find_all_state(x)
                        break
                else:
                    if self.is_in_follow(a.name, A.name):
                        if self.is_in_first('ε', A.name):
                            self.parse_table[A.name][a.name] = [['ε', 'Terminal']]
                            for x in self.grammar_rules[A.name]:
                                if self.epsilon_check(x):
                                    self.parse_table[A.name][a.name] = self.find_all_state(x)
                                    break
                        else:
                            self.parse_table[A.name][a.name] = [['sync', '']]
                    else:
                        self.parse_table[A.name][a.name] = [['empty', '']]

    def find_all_state(self, list1):
        result = []
        for r in list1:
            state1 = self.initializer.find_state(r)
            if isinstance(state1, Terminal):
                result.append([r, 'Terminal'])
            else:
                result.append([r, 'Non-Terminal'])
        return result

    def get_parse_table(self):
        return self.parse_table