class CodeGen:
    def __init__(self, symbol_table):
        self.semantic_stack = []
        self.symbol_table = symbol_table
        self.tempVarIndex = 500
        self.top = 0

    def getTemp(self):
        self.tempVarIndex += 4
        return self.tempVarIndex

    def getAddress(self, token):
        for i in range(len(self.symbol_table)):
            if self.symbol_table[i] == token:
                return i
        return -1

    def checkAction(self, actionName, token):
        if actionName == "pid":
            self.pid(token)

            # here we have the function of actions

    def pid(self, token):
        add = self.getAddress(token)
        self.semantic_stack.append(add)
        self.top += 1

    def pnum(self, token):
        self.semantic_stack.append(f"#{token.lexeme}")

    def pzero(self, token=None):
        self.semantic_stack.append(f"#0")

    def prv(self, token=None):
        self.semantic_stack.append(self.rf.rv)

    def parr(self, token=None):
        offset = self.semantic_stack.pop()
        temp = self.get_temp_var()
        self.assembler.program_block.append(f"(MULT, #{self.MLD.WORD_SIZE}, {offset}, {temp})")
        self.assembler.program_block.append(f"(ADD, {self.semantic_stack.pop()}, {temp}, {temp})")
        self.semantic_stack.append(f"@{temp}")

    def pop(self, token=None):
        self.semantic_stack.pop()

    def declare_arr(self, token=None):
        self.assembler.program_block.append(f"(ASSIGN, {self.rf.sp}, {self.semantic_stack[-2]}, )")
        self.stack.reserve(int(self.semantic_stack.pop()[1:]))

    def declare_func(self, token=None):
        self.assembler.data_pointer = self.assembler.data_address
        self.assembler.temp_pointer = self.assembler.temp_address

        # only when zero init is activated
        self.assembler.program_block[-1] = ""

        id_record = self.find_var(self.assembler.last_id.lexeme)
        id_record.address = len(self.assembler.program_block)

    def declare_id(self, token):
        id_record = self.find_var(token.lexeme)
        id_record.address = self.get_data_var()

        self.assembler.last_id = token

        if self.assembler.arg_dec:
            self.arg_assign(id_record.address)
        else:
            self.assembler.program_block.append(f"(ASSIGN, #0, {id_record.address}, )")
            pass

    @staticmethod
    def declare(Token=None):
        tables.get_symbol_table().set_declaration(True)

    def assign(self, token=None):
        self.assembler.program_block.append(f"(ASSIGN, {self.semantic_stack.pop()}, {self.semantic_stack[-1]}, )")

    def op_exec(self, token=None):
        second = self.semantic_stack.pop()
        operand = self.semantic_stack.pop()
        first = self.semantic_stack.pop()
        result = self.get_temp_var()
        self.assembler.program_block.append(f"({operand}, {first}, {second}, {result})")
        self.semantic_stack.append(result)

    operands = {'+': 'ADD', '-': 'SUB', '*': 'MULT', '<': 'LT', '==': 'EQ'}

    def op_push(self, token):
        self.semantic_stack.append(self.operands[token.lexeme])

    def hold(self, token=None):
        self.label()
        self.assembler.program_block.append("(new you see me!)")

    def label(self, token=None):
        self.semantic_stack.append(len(self.assembler.program_block))

    def decide(self, token=None):
        address = self.semantic_stack.pop()
        self.assembler.program_block[
            address] = f"(JPF, {self.semantic_stack.pop()}, {len(self.assembler.program_block)}, )"

    def case(self, token=None):
        result = self.get_temp_var()
        self.assembler.program_block.append(f"(EQ, {self.semantic_stack.pop()}, {self.semantic_stack[-1]}, {result})")
        self.semantic_stack.append(result)

    def jump_while(self, token=None):
        head1 = self.semantic_stack.pop()
        head2 = self.semantic_stack.pop()
        self.assembler.program_block.append(f"(JP, {self.semantic_stack.pop()}, , )")
        self.semantic_stack.append(head2)
        self.semantic_stack.append(head1)

    def output(self, token=None):
        self.assembler.program_block.append(f"(PRINT, {self.semantic_stack.pop()}, , )")

    def get_temp_var(self):
        self.assembler.temp_address += self.MLD.WORD_SIZE
        return self.assembler.temp_address - self.MLD.WORD_SIZE

    def get_data_var(self, chunk_size=1):
        self.assembler.data_address += self.MLD.WORD_SIZE * chunk_size
        return self.assembler.data_address - self.MLD.WORD_SIZE * chunk_size

    def store(self):
        # storing data
        for data in range(self.assembler.data_pointer, self.assembler.data_address, self.MLD.WORD_SIZE):
            self.stack.push(data)
        # storing temp
        for temp in range(self.assembler.temp_pointer, self.assembler.temp_address, self.MLD.WORD_SIZE):
            self.stack.push(temp)
        # storing registers
        self.stack.store_registers()

    def restore(self):
        # loading registers
        self.stack.load_registers()
        # loading temps
        for temp in range(self.assembler.temp_address, self.assembler.temp_pointer, -self.MLD.WORD_SIZE):
            self.stack.pop(temp - self.MLD.WORD_SIZE)
        # loading data
        for data in range(self.assembler.data_address, self.assembler.data_pointer, -self.MLD.WORD_SIZE):
            self.stack.pop(data - self.MLD.WORD_SIZE)

    def collect(self):
        # collect
        result = self.get_temp_var()
        self.assembler.program_block.append(f"(ASSIGN, {self.rf.rv}, {result}, )")
        self.semantic_stack.append(result)

    def push_args(self):
        # arg pass
        for arg in range(self.assembler.arg_pointer.pop(), len(self.semantic_stack)):
            self.stack.push(self.semantic_stack.pop())

    def func_call(self, token=None):
        self.store()
        self.push_args()
        # setting registers
        self.assembler.program_block.append(f"(ASSIGN, #{len(self.assembler.program_block) + 2}, {self.rf.ra}, )")
        # call!
        self.assembler.program_block.append(f"(JP, {self.semantic_stack.pop()}, , )")
        self.restore()
        self.collect()

    def func_return(self, token=None):
        self.assembler.program_block.append(f"(JP, @{self.rf.ra}, , )")

    # argument management
    def arg_init(self, token=None):
        self.assembler.arg_dec = True

    def arg_finish(self, token=None):
        self.assembler.arg_dec = False

    def arg_assign(self, address):
        self.stack.pop(address)

    def arg_pass(self, token=None):
        self.assembler.arg_pointer.append(len(self.semantic_stack))

    # scope
    def scmod_f(self, token=None):
        self.scope.push_scmod("f")  # function

    def scmod_c(self, token=None):
        self.scope.push_scmod("c")  # container

    def scmod_s(self, token=None):
        self.scope.push_scmod("s")  # simple

    def scmod_t(self, token=None):
        self.scope.push_scmod("t")  # temporary

    def scope_start(self, token=None):
        tables.get_symbol_table().new_scope()
        self.scope.new_scope()

    def scope_stop(self, token=None):
        tables.get_symbol_table().remove_scope()
        self.scope.del_scope()

    def prison(self, token=None):
        self.scope.prison()

    def prison_break(self, token=None):
        self.scope.prison_break()

    @staticmethod
    def find_var(id):
        return tables.get_symbol_table().fetch(id)

    def export(self, path):
        with open(path, "w") as f:
            for i, l in enumerate(self.assembler.program_block):
                f.write(f"{i}\t{l}\n")

    def apply_template(self):
        self.assembler.program_block.append(f"(ASSIGN, #{self.MLD.STACK_ADDRESS}, {self.rf.sp}, )")
        self.assembler.program_block.append(f"(ASSIGN, #{self.MLD.STACK_ADDRESS}, {self.rf.fp}, )")

        self.assembler.program_block.append(f"(ASSIGN, #9999, {self.rf.ra}, )")
        self.assembler.program_block.append(f"(ASSIGN, #9999, {self.rf.rv}, )")

        self.assembler.program_block.append(f"(JP, 9, , )")
        self.stack.pop(self.rf.rv)
        self.assembler.program_block.append(f"(PRINT, {self.rf.rv}, , )")
        self.assembler.program_block.append(f"(JP, @{self.rf.ra}, , )")
        self.get_data_var()

    def set_exec(self, token=None):
        if not self.assembler.set_exec:
            self.assembler.set_exec = True
            func = self.semantic_stack.pop()
            self.assembler.program_block.pop()
            self.hold()
            self.semantic_stack.append(func)

    def execute_from(self, func_name):
        try:
            id_record = self.find_var(func_name)
            self.assembler.program_block[self.semantic_stack.pop()] = f"(JP, {id_record.address}, , )"
        except:
            sys.stderr.write(f"couldn't set the executable path")
