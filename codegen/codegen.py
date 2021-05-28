class CodeGen:
    def __init__(self , symbol_table):
        self.semantic_stack = []
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
