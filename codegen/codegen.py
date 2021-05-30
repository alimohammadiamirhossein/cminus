class CodeGen:
    def __init__(self , symbol_table):
        self.semantic_stack = []
        self.program_block = []
        self.symbol_table = symbol_table
        self.tempVarIndex = 500
        self.top = 0

    def getTemp(self):
        self.tempVarIndex += 4
        return self.tempVarIndex

    def getAddress(self,token):
        for i in range(len(self.symbol_table)) :
            if self.symbol_table[i] == token:
                return i
        return -1

    def checkAction(self,actionName , token):
        if actionName == "pid":
            self.pid(token)



    # here we have the function of actions

    def pid(self,token):
        add = self.getAddress(token)
        self.semantic_stack.append(add)
        self.top += 1

    def pnum(self, token):
        self.semantic_stack.append(f"#{token}")


    def parr(self, token=None):
        len1 = self.semantic_stack.pop()
        tmp_address = self.getTemp()
        array_start_address = self.semantic_stack.pop()
        self.program_block.append(f"MULT, #4, {len1}, {tmp_address}")
        self.program_block.append(f"ADD, {array_start_address}, {tmp_address}, {tmp_address}")
        self.semantic_stack.append(f"{tmp_address}")


    #def declare_id(self):
        #ssssssssssssssssssssssssssssssssssssssssssssssssssssssss

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
        self.semantic_stack.append(self.operands[token.lexeme])

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
        self.semantic_stack.append(f"({op}, {a}, {b}, {tmp_address})")
        self.semantic_stack.append(tmp_address)