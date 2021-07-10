class Stack:
    def __init__(self, program_block, sp, fp, ra, rv):
        self.program_block = program_block
        self.stack_pointer = sp
        self.first_pointer = fp
        self.last_pointer = None
        self.return_address = ra
        self.return_value = rv


    def push(self, v , str = ""):
        str = ""
        programBlock = self.program_block
        programBlock.append(f"{str}(ASSIGN, {v}, @{self.stack_pointer}, )")
        programBlock.append(f"{str}(ADD, {self.stack_pointer}, #4, {self.stack_pointer})")

    def check_stack(self):
        if len(self.program_block) > 0 :
            return True

    def pop(self, assign , str = ""):
        str = ""
        programBlock = self.program_block
        programBlock.append(f"{str}(SUB, {self.stack_pointer}, #4, {self.stack_pointer})")
        programBlock.append(f"{str}(ASSIGN, @{self.stack_pointer}, {assign}, )")

    def new_scope(self):
        programBlock = self.program_block
        programBlock.append("")
        self.push(self.first_pointer)
        programBlock.append(f"(ASSIGN, {self.stack_pointer}, {self.first_pointer}, )")

    def delete_scope(self):
        self.program_block.append("this place is for scope and stack deletion")
        self.stack_pointer = self.first_pointer
        self.first_pointer = self.pop()

    def save_stack_info(self):
        print("stack debug" , self.first_pointer , self.stack_pointer , self.return_address)
        self.push(self.first_pointer, "save")
        self.push(self.stack_pointer , "save")
        self.push(self.return_address , "save")

    def load_stack_info(self):
        print("stack debug load" , self.first_pointer , self.stack_pointer , self.return_address)
        self.pop(self.first_pointer,"load")
        self.pop(self.return_address,"load")
        self.pop(self.stack_pointer,"load")


