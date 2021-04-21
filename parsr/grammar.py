from parsr.state import State, Terminal, NonTerminal


class Grammar:
    def __init__(self, patch, initializer):
        self.initializer = initializer
        self.grammar_file = open(patch+'grammar.txt', 'r', encoding='utf-8')
        # self.firsts_file = open(patch + 'firsts.txt', 'r', encoding='utf-8')
        # self.follows_file = open(patch + 'follows.txt', 'r', encoding='utf-8')
        self.grammar_rules = {}
        self.firsts_rules = {}
        self.follows_rules = {}
        self.parse_table = {}
        self.grammar_file_reader()
        self.first_reader()
        self.follow_reader()
        self.make_parse_table()

    def follow_reader(self):
        pass #need to complete

    def first_reader(self):
        pass #need to complete

    def grammar_file_reader(self):
        line_ = "a"
        while line_ != "":
            line_ = self.grammar_file.readline()
            names = line_.split()
            index = 3
            scenario = []
            while index < len(names):
                if names[index] != "|":
                    scenario.append(names[index])
                index += 1
                if index == len(names) or names[index] == "|":
                    if self.grammar_rules.get(names[1]) is None:
                        self.grammar_rules[names[1]] = [scenario]
                    else:
                        self.grammar_rules[names[1]].append(scenario)
                    scenario = []

    def make_parse_table(self): #it probably have bug
        for A in self.initializer.non_terminals:
            if self.parse_table[A.name] is None:
                self.parse_table[A.name] = {}
            for a in self.initializer.terminals:
                for x in self.grammar_rules[A.name]:
                    if a in first(x):#check kon a ozve x hast ya na
                        self.parse_table[A.name][a.name] = x
                else:
                    if a in follow(A):
                        self.parse_table[A.name][a.name] = 'synch'
                    else:
                        self.parse_table[A.name][a.name] = 'empty'


    # '''need to check     probably have bug'''
    # def match(self, token_name, current_scenario):
    #     for i in range(len(self.dict_[current_scenario])):
    #         scenario_next = self.dict_[current_scenario][i]
    #         if isinstance(scenario_next, Terminal):
    #             if token_name == scenario_next.name:
    #                 print("Match")
    #         elif isinstance(scenario_next, NonTerminal):
    #             if scenario_next.is_in_first(token_name):
    #                 return scenario_next
    #     print('error')

