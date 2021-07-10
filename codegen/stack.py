class Stack:
    def __init__(self, program_block, sp, fp, ra, rv):
        self.program_block = program_block
        self.stack_pointer = sp
        self.first_pointer = fp
        self.return_address = ra
        self.return_value = rv
        self.last_func_stack_pointer = 84846968

    def push(self, v , str = ""):
        str = ""
        self.program_block.append(f"{str}(ASSIGN, {v}, @{self.stack_pointer}, )")
        self.program_block.append(f"{str}(ADD, {self.stack_pointer}, #4, {self.stack_pointer})")

    def pop(self, assign , str = ""):
        str = ""
        self.program_block.append(f"{str}(SUB, {self.stack_pointer}, #4, {self.stack_pointer})")
        self.program_block.append(f"{str}(ASSIGN, @{self.stack_pointer}, {assign}, )")

    def new_scope(self):
        self.program_block.append("")
        self.push(self.first_pointer)
        self.program_block.append(f"(ASSIGN, {self.stack_pointer}, {self.first_pointer}, )")

    def delete_scope(self):
        self.stack_pointer = self.first_pointer
        self.first_pointer = self.pop()
        self.program_block.append("delete scope/stack")

    def save_stack_info(self):
        self.push(self.stack_pointer , "save")
        self.push(self.first_pointer, "save")
        self.push(self.return_address , "save")

    def load_stack_info(self):
        self.pop(self.return_address,"load")
        self.pop(self.first_pointer,"load")
        self.pop(self.stack_pointer,"load")