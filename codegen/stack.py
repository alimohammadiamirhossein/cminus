class Stack:
    def __init__(self, program_block, sp, fp, ra, rv):
        self.program_block = program_block
        self.stack_pointer = sp
        self.first_pointer = fp
        self.return_address = ra
        self.return_value = rv

    def push(self, v):
        self.program_block.append(f"(ASSIGN, {v}, @{self.stack_pointer}, )")
        self.program_block.append(f"(ADD, {self.stack_pointer}, #4, {self.stack_pointer})")

    def pop(self, assign):
        self.program_block.append(f"(SUB, {self.stack_pointer}, #4, {self.stack_pointer})")
        self.program_block.append(f"(ASSIGN, @{self.stack_pointer}, {assign}, )")

    def new_scope(self):
        self.program_block.append("new scope create/stack")
        self.push(self.first_pointer)
        self.first_pointer = self.stack_pointer

    def delete_scope(self):
        self.stack_pointer = self.first_pointer
        self.first_pointer = self.pop()
        self.program_block.append("delete scope/stack")

    def save_stack_info(self):
        self.push(self.stack_pointer)
        self.push(self.first_pointer)
        self.push(self.return_address)

    def load_stack_info(self):
        self.return_address = self.pop()
        self.first_pointer = self.pop()
        self.stack_pointer = self.pop()