from enum import Enum


class ScopeType(Enum):
    Function = 1


class Scope:
    def __init__(self, memory):
        self.brakesAddress = []
        self.memory = memory

    def add_scope(self):
        pass

    def del_scope(self):
        pass

    def add_break_point(self):
        self.brakesAddress.append(len(self.memory.program_block))
        self.memory.program_block('wait for new break point')

    def fill_break_point(self):
        fill_in_program_block = self.brakesAddress.pop()
        self.memory.program_block[fill_in_program_block] = f"(JP, {len(self.memory.program_block)}, , )"

