from enum import Enum


class ScopeType(Enum):
    Function = 1
    For = 2
    If = 3
    State = 4


class Scope:
    def __init__(self, memory, type1):
        self.brakesAddress = []
        self.memory = memory
        self.scope_type: ScopeType
        # self.tempVarIndex = self.memory.tempVarIndex
        # self.dataVarIndex = self.memory.dataVarIndex
        self.temp_list = []
        self.data_list = []

        self.scope_type = type1

    def add_break_point(self):
        self.brakesAddress.append(len(self.memory.program_block))
        self.memory.program_block.append('wait for new break point')

    def fill_break_point(self):
        fill_in_program_block = self.brakesAddress.pop()
        self.memory.program_block[fill_in_program_block] = f"(JP, {len(self.memory.program_block)}, , )"

    def update_memory(self):
        self.temp_list.append(self.memory.tempVarIndex)
        self.data_list.append(self.memory.dataVarIndex)
        # self.jail.append("|")

    def restore_memory(self):
        self.memory.tempVarIndex = self.temp_list.pop()
        self.memory.dataVarIndex = self.data_list.pop()

class ScopeLists:
    def __init__(self, memory, stack):
        self.scopes = []
        self.memory = memory
        self.stack = stack

    def append_scope(self, type1):  # type : 'function' 'for' 'if'
        type1 = self.find_type(type1)
        sc = Scope(self.memory, type1)
        if type1 == "function":
            sc.update_memory()
            # self.temp_stack.append(self.assembler.temp_address)
            # self.data_stack.append(self.assembler.data_address)

        self.scopes.append(sc)

    def find_index_scope_by_type(self, type1):
        for i in range(len(self.scopes) - 1, -1, -1):
            # print(str(self.scopes[i].scope_type) ,12, str(type1))
            if str(self.scopes[i].scope_type) == str(type1):
                return i

    def add_break_point(self, type1):
        type1 = self.find_type(type1)
        index1 = self.find_index_scope_by_type(type1)
        self.scopes[index1].add_break_point()

    def fill_break_point(self, type1):
        type1 = self.find_type(type1)
        index1 = self.find_index_scope_by_type(type1)
        self.scopes[index1].fill_break_point()

    def delete_scope(self, type1):
        type1 = self.find_type(type1)
        index1 = self.find_index_scope_by_type(type1)
        # print("annnn",self.scopes)
        while len(self.scopes[index1].brakesAddress) > 0:
            self.scopes[index1].fill_break_point()


    # print(index1, type1)
        if type1 == "function":
            self.scopes[index1].restore_memory()
        # print("love ", self.memory.tempVarIndex)
        self.scopes.pop(index1)

    def find_type(self, type1):
        if type1 == "function":
            type1 = ScopeType.Function
        elif type1 == "for":
            type1 = ScopeType.For
        elif type1 == "if":
            type1 = ScopeType.If
        elif type1 == "state":
            type1 = ScopeType.State
        return type1
