class CodeGen:
    def __init__(self, symbol):
        self.semantic_stack = []
        self.program_block = []
        self.symbol = symbol
        self.tempVarIndex = 500
        self.dataVarIndex = 0

    def getTemp(self):
        self.tempVarIndex += 4
        return self.tempVarIndex - 4

    def getDataAdd(self):
        self.dataVarIndex += 4
        return self.dataVarIndex

    # def getAddress(self,token):
    #     for i in range(len(self.symbol_table)) :
    #         if self.symbol_table[i] == token:
    #             return i
    #     return -1

    def checkAction(self, actionName, token):
        actionName = actionName[1:]
        token = token[2]
        if actionName == "pid":
            self.pid(token)
        elif actionName == "pnum":
            self.pnum(token)
        elif actionName == "parr":
            self.parr(token)
        elif actionName == "declare_id":
            self.declare_id(token)
        elif actionName == "declare_arr":
            self.declare_arr(token)
        elif actionName == "assign":
            self.assign(token)
        elif actionName == "op_push":
            self.op_push(token)
        elif actionName == "op_exec":
            self.op_exec(token)
        elif actionName == "negative":
            self.negative()
        elif actionName == "output":
            self.output()
        elif actionName == "end":
            self.end()
        # print(self.semantic_stack)
        print(actionName)
        print(self.program_block)
        # print(self.symbol.symbol_table)
        # print(token)
        # print(11111111111111111111111111111111111)



    # here we have the function of actions

    def pid(self,token):
        x = self.symbol.find_symbol(token)
        self.semantic_stack.append(x.address)

    def pnum(self, token):
        self.semantic_stack.append(f"#{token}")

    def parr(self, token=None):
        len1 = self.semantic_stack.pop()
        tmp_address = self.getTemp()
        array_start_address = self.semantic_stack.pop()
        self.program_block.append(f"MULT, #4, {len1}, {tmp_address}")
        self.program_block.append(f"ADD, {array_start_address}, {tmp_address}, {tmp_address}")
        self.semantic_stack.append(f"{tmp_address}")

    def declare_id(self, token):
        x = self.symbol.find_symbol(token)
        # print(x)
        x.address = self.getTemp()
        self.program_block.append(f"(ASSIGN, #0, {x.address}, )")
        # print(x.address)

    def declare_arr(self, token=None):
        len1 = self.semantic_stack.pop()
        len1 = int(len1[1:])
        len1 -= 1
        self.top += 4 * len1

    def assign(self, token=None):
        value = self.semantic_stack.pop()
        assign_par = self.semantic_stack.pop()
        self.program_block.append(f"(ASSIGN, {value}, {assign_par}, )")
        self.semantic_stack.append(assign_par)

    def op_push(self, token):
        self.semantic_stack.append(token)

    def op_exec(self, token):
        b = self.semantic_stack.pop()
        op = self.semantic_stack.pop()
        a = self.semantic_stack.pop()
        if op == "+":
            op = "ADD"
        elif op == "-":
            op = "SUB"
        elif op == "*":
            op = "MULT"
        elif op == "<":
            op = "LT"
        elif op == "==":
            op = "EQ"
        tmp_address = self.getTemp()
        self.program_block.append(f"({op}, {a}, {b}, {tmp_address})")
        self.semantic_stack.append(tmp_address)

    def negative(self):
        b = self.semantic_stack.pop()
        tmp_address = self.getTemp()
        self.program_block.append(f"(SUB, #0, {b}, {tmp_address})")
        self.semantic_stack.append(tmp_address)

    def output(self):
        self.program_block.append(f"(PRINT, {self.semantic_stack.pop()}, , )")

    def end(self):
        self.semantic_stack.pop()