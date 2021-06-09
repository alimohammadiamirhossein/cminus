from enum import Enum


class ScopeType(Enum):
    Function = 1
    For = 2
    If = 3


class Scope:
    def __init__(self, memory, type1):
        self.brakesAddress = []
        self.memory = memory
        self.scope_type: ScopeType
        self.tempVarIndex = self.memory.tempVarIndex
        self.dataVarIndex = self.memory.dataVarIndex
        self.scope_type = type1

    def add_break_point(self):
        self.brakesAddress.append(len(self.memory.program_block))
        self.memory.program_block('wait for new break point')

    def fill_break_point(self):
        fill_in_program_block = self.brakesAddress.pop()
        self.memory.program_block[fill_in_program_block] = f"(JP, {len(self.memory.program_block)}, , )"


class ScopeLists:
    def __init__(self, memory):
        self.scopes = []
        self.memory = memory

    def append_scope(self, type1): #type : 'function' 'for' 'if'
        if type1 == "function":
            type1 = ScopeType.Function
        elif type1 == "for":
            type1 = ScopeType.For
        elif type1 == "if":
            type1 = ScopeType.If

        self.scopes.append(self.memory, type1)

    def find_index_scope_by_type(self, type1):
        for i in range(len(self.scopes)-1, -1, -1):
            if str(self.scopes[i].scope_type) == str(type1):
                return  i

    def add_break_point(self, type1):
        index1 = self.find_index_scope_by_type(type1)
        self.scopes[index1].add_break_point()

    def fill_break_point(self, type1):
        index1 = self.find_index_scope_by_type(type1)
        self.scopes[index1].fill_break_point()

