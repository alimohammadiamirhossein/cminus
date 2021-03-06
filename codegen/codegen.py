from codegen.scope import ScopeLists
from codegen.stack import Stack
from codegen.semantic_analyser import Semantic_writer
from Symbols.symbol_table import Token,  TokenType

class Memory:
    def __init__(self, symbol_table, dataVar=0, tempVar=0):
        self.program_block = []
        self.symbol = symbol_table
        self.tempVarIndex = tempVar
        self.dataVarIndex = dataVar
        self.tempPointer = tempVar
        self.dataPointer = dataVar
        self.line_number = 0

class CodeGen:
    def __init__(self, symbol):
        self.semantic_analyser = Semantic_writer()
        self.semantic_stack = []
        self.last_id_type = []
        self.last_id_name = ""
        self.last_arg_name = ""
        self.last_arg_good_name = ""
        self.left_arg = ""
        self.arg_pass_number = -1
        self.info = []
        self.memory = Memory(symbol)
        self.memory.dataVarIndex = 500
        self.memory.dataPointer = 500
        self.memory.tempVarIndex = 900
        self.memory.tempPointer = 900
        self.stack = Stack(self.memory.program_block, self.getDataAdd(), self.getDataAdd(),
                           self.getDataAdd(), self.getDataAdd())
        self.scope_lists = ScopeLists(self.memory, self.stack)
        self.scope_lists.semantic_analyser = self.semantic_analyser
        self.get_param_value = False
        self.assembler = Assembler()
        self.assembler.data_address = 500
        self.assembler.stack_address = 1000
        self.assembler.temp_address = 900

        self.params = []
        self.first_func = False
        self.jump_to_main_address = 0
        self.main_check = False
        self.is_print = False
        self.function_parameters_number = 0
        self.function_parameters_types = []
        self.function_first_detail = []
        self.function_parameters_is_array = []
        # for i in range(900 , 1000 , 4):
        #     self.memory.program_block.append(f"(ASSIGN, #0, {i}, )")
        self.memory.program_block.append(f"(ASSIGN, #1000, {self.stack.stack_pointer}, )")
        self.memory.program_block.append(f"(ASSIGN, #1000, {self.stack.first_pointer}, )")

        self.memory.program_block.append(f"(ASSIGN, #9999, {self.stack.return_address}, )")
        self.memory.program_block.append(f"(ASSIGN, #9999, {self.stack.return_value}, )")

        self.memory.program_block.append(f"(JP, 9, , )")
        self.stack.pop(self.stack.return_value)
        self.memory.program_block.append(f"(PRINT, {self.stack.return_value}, , )")
        self.memory.program_block.append(f"(JP, @{self.stack.return_address}, , )")
        # print(len(self.memory.program_block))
        self.getDataAdd()

    def getTemp(self):
        self.memory.tempVarIndex += 4

        return self.memory.tempVarIndex - 4

    def getDataAdd(self, count=1):
        self.memory.dataVarIndex += 4 * count
        return self.memory.dataVarIndex - 4 * count

    # def getAddress(self,token):
    #     for i in range(len(self.symbol_table)) :
    #         if self.symbol_table[i] == token:
    #             return i
    #     return -1

    def checkAction(self, actionName, token):
        actionName = actionName[1:]
        print("salam" , token)
        self.memory.line_number = token[0]
        token = token[2]
        print(token, actionName)
        print(self.semantic_stack)
        print("************")
        if actionName == "pid":
            self.pid(token)
        elif actionName == "pnum":
            self.pnum(token)
        elif actionName == "parray":
            self.parray(token)
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
        elif actionName == "label":
            self.label(token)
        elif actionName == "save":
            self.save(token)
        elif actionName == "whilejump":
            self.jump_while(token)
        elif actionName == "jpf_save":
            self.jpf_save(token)
        elif actionName == "return_value_push":
            self.return_value_push(token)
        elif actionName == "jp":
            self.jp(token)
        elif actionName == "push_stack":
            self.push_stack(token)
        elif actionName == "assign_parameters":
            self.assign_parameters(token)
        elif actionName == "first_function":
            self.first_function(token)
        elif actionName == "function_call":
            self.function_call(token)
        elif actionName == "jump_return_address":
            self.jump_return_address(token)
        elif actionName == "array_in_function":
            self.array_in_function(token)
        elif actionName == "check_main":
            self.check_main(token)
        elif actionName == "get_temp_save":
            self.get_temp_save()
        elif actionName == "assign_jp":
            self.assign_jp()
        elif actionName == "jp_fill_save":
            self.jp_fill_save()
        elif actionName == "for":
            self.for_()


        elif actionName == "declare_func":
            self.declare_func(token)
        elif actionName == "declare":
            self.declare(token)
        elif actionName == "set_exec":
            self.set_exec(token)
        elif actionName == "jump_while":
            self.jump_while(token)
        elif actionName == "check_void":
            self.check_void(token)
        elif actionName == "arg_pass":
            self.arg_pass(token)
        elif actionName == "arg_pass_finish":
            self.arg_pass_finish(token)
        elif actionName == "arg_counter":
            self.arg_counter(token)
        elif actionName == "arg_init":
            self.arg_init(token)
        elif actionName == "arg_finish":
            self.arg_finish(token)
        elif actionName == "arg_assign":
            self.arg_assign(token)
        elif actionName == "save_left_type":
            self.save_left_type(token)



        elif actionName == "save_variable":
            self.save_load_variables(True)
        elif actionName == "load_variable":
            self.save_load_variables(False)
        elif actionName == "param_value":
            self.param_value(token)
        elif actionName == "param_value_end":
            self.param_value_end(token)
        elif actionName == "function_address":
            self.function_address()
        elif actionName.startswith("add_scope_Type"):
            self.add_scope(actionName.split("_")[3])
        elif actionName.startswith("del_scope_Type"):
            self.del_scope(actionName.split("_")[3])
        elif actionName.startswith("add_break_point_Type"):
            self.add_break_point(actionName.split("_")[4])
        elif actionName.startswith("fill_break_point_Type"):
            self.fill_break_point(actionName.split("_")[4])

        # print(actionName)
        # print(self.memory.program_block, token)
        print(token , actionName)
        print(self.semantic_stack)
        # print(self.symbol.symbol_table)
        print("tmp", self.memory.tempVarIndex)
        print("-----------------------")
        # print(self.stack.first_pointer)
        # print(11111111111111111111111111111111111)
        self.output_writer()

    # here we have the function of actions
    def pid(self, token):
        # print("line_number",line_number)
        x = self.find_var(token)
        if self.arg_pass_number == -1:
            self.last_arg_good_name = x
        print(self.memory.line_number , "rap" , x)
        if x == None:
            self.semantic_stack.append("85856969")
            self.semantic_analyser.add_error(f"#{self.memory.line_number} : Semantic Error! '{token}' is not defined")
            pass
        else:
            if x.address == None:
                self.semantic_analyser.add_error(f"#{self.memory.line_number} : Semantic Error! '{token}' is not defined")
            self.semantic_stack.append(x.address)
            self.info.append(x)


    def arg_counter(self, token = None):
        if self.arg_pass_number != -1:
            self.arg_pass_number += 1

    def pnum(self, token):
        self.semantic_stack.append(f"#{token}")
        y = Token(TokenType.ID, f"#{token}")
        self.memory.symbol.add_symbol(y)
        x = self.find_var(f"#{token}")
        x.is_array = False
        if self.arg_pass_number == -1:
            self.last_arg_good_name = x
        self.info.append(x)


    def parray(self, token=None):
        # len1 = self.semantic_stack.pop()
        # tmp_address = self.getTemp()
        # array_start_address = self.semantic_stack.pop()
        # self.memory.program_block.append(f"(MULT, #4, {len1}, {tmp_address})")
        # self.memory.program_block.append(f"(ADD, #{array_start_address}, {tmp_address}, {tmp_address})")
        # self.semantic_stack.append(f"@{tmp_address}")
        offset = self.semantic_stack.pop()
        temp = self.getTemp()
        print("temp",temp)
        self.memory.program_block.append(f"(MULT, #{4}, {offset}, {temp})")
        self.memory.program_block.append(f"(ADD, {self.semantic_stack.pop()}, {temp}, {temp})")
        self.semantic_stack.append(f"@{temp}")

    # def declare_id(self, token):
    #     x = self.memory.symbol.find_symbol(token)
    #     # print(x.token, self.get_param_value)
    #     x.address = self.getDataAdd()
    #     if self.get_param_value:
    #         self.params.append(x)
    #         # print("Address " , x.address )
    #         # self.stack.pop(x.address)
    #     else:
    #         self.memory.program_block.append(f"(ASSIGN, #0, {x.address}, )")
    #     self.semantic_stack.append(x.address)  # not sure
    #     # print(x.address)

    def declare_arr(self, token=None):
        # len1 = self.semantic_stack.pop()
        # address1 = self.semantic_stack.pop()
        # len1 = int(len1[1:])
        # len1 -= 1
        # for i in range(len1):
        #     self.getDataAdd()
        #     self.memory.program_block.append(f"(ASSIGN, #0, {address1 + 4}, )")
        #     address1 += 4
        x = self.memory.symbol.fetch_from_address(self.semantic_stack[-2]) #todo hosein by address
        print('yo', self.semantic_stack[-2], x)
        x.is_array = True
        self.memory.program_block.append(f"(ASSIGN, {self.stack.stack_pointer}, {x.address}, )")
        chunk = int(self.semantic_stack.pop()[1:])
        self.memory.program_block.append(f"(ADD, #{4 * chunk}, {self.stack.stack_pointer}, {self.stack.stack_pointer})")
        print("owww", self.find_var(self.last_id_name))
        # if x.id_type == "void":
        #     print(f"#lineno: Semantic Error! Illegal type of void for {x.token.lexeme}")

    def array_in_function(self, token=None):
        print("lala")
        if self.assembler.arg_dec:
            self.function_parameters_is_array[-1] = False
            # print(f"lalala {x}")


    def assign(self, token=None):
        value = self.semantic_stack.pop()
        assign_par = self.semantic_stack.pop()
        # print(self.info[-1], self.info[-2], 'info')
        # if type(value) == str:
        #     if value[0] == "#":
        #         pass
        #     else:
        #         if self.last_arg_good_name.id_type == "int":
        #             if self.info[-1].is_array == self.info[-2].is_array:
        #                 pass
        #             else:
        #                 self.semantic_analyser.add_error(f"assign #{self.memory.line_number}: got array instead of int")
        #         else:
        #             if self.info[-1].id_type != None and self.info[-2].id_type != None:
        #                 self.semantic_analyser.add_error(f"assign#{self.memory.line_number}: got {self.info[-1].id_type} instead of {self.info[-2].id_type}")
        # else:
        #     if self.info[-1].id_type == self.info[-2].id_type:
        #         if self.info[-1].is_array == self.info[-2].is_array:
        #             pass
        #         else:
        #             self.semantic_analyser.add_error(f"assign#{self.memory.line_number}: got array instead of int")
        #     else:
        #         if self.info[-1].id_type != None and self.info[-2].id_type != None:
        #             self.semantic_analyser.add_error(f"assign#{self.memory.line_number}: got {self.info[-1].id_type} instead of {self.info[-2].id_type}")
###############################################
        # if self.info[-1].id_type == self.info[-2].id_type:
        #     if self.info[-1].is_array == self.info[-2].is_array:
        #         pass
        #     else:
        #         print(f"#{self.memory.line_number}: got array instead of int")
        # else:
        #     print(f"#{self.memory.line_number}: got {self.info[-1].id_type} instead of {self.info[-2].id_type}")
        self.memory.program_block.append(f"(ASSIGN, {value}, {assign_par}, )")
        self.semantic_stack.append(assign_par)

    def op_push(self, token):
        print("op_push11", token )

        self.left_arg = self.last_arg_good_name
        self.semantic_stack.append(token)

    def jump_return_address(self, token):
        self.memory.program_block.append(f"(JP, @{self.stack.return_address}, , )")

    def save_left_type(self , token):
        print(self.memory.line_number , "khastam" , token)

    def op_exec(self, token):
        b = self.semantic_stack.pop()
        op = self.semantic_stack.pop()
        a = self.semantic_stack.pop()
        print(self.memory.line_number , "sigar" , self.last_arg_good_name)
        # print("viking" , a , b[0])
        # print("superman" , self.info[-1] , self.info[-2])
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
        print("tmp_address",tmp_address)
        self.memory.program_block.append(f"({op}, {a}, {b}, {tmp_address})")
        self.semantic_stack.append(tmp_address)
        print(a , b)
        # x1 = self.memory.symbol.fetch_from_address(a)
        # x2 = self.memory.symbol.fetch_from_address(b)
        # print("day" , self.memory.line_number, x1 , x2)
        # print("joker" , self.info[-1].token.lexeme , self.info[-2].token.lexeme)
        # print("thanks" , self.info[-1] , self.info[-2])
        x1 = self.left_arg
        x2 = self.last_arg_good_name
        print("my baby" , x1 , x2)
        type1 = x1.id_type
        type2 = x2.id_type
        print(self.memory.line_number , "amirhossein" , x1.id_type , x2)
        if type(b) == str :
            if x1.address == None:
                pass
            elif b[0] == "#":
                type2 = "int"
                if x1.id_type == "int":
                    if x1.is_array:
                        self.semantic_analyser.add_error(f"#{self.memory.line_number} : Semantic Error! Type mismatch in operands, got array instead of int.")
                else:
                    self.semantic_analyser.add_error(f"#{self.memory.line_number} : Semantic Error! Type mismatch in operands, got int instead of {x1.id_type}.")
        elif type(a) == str:
            if x2.address == None:
                pass
            elif a[0] == "#":
                type1 = "int"
                if x2.id_type == "int":
                    if x2.is_array:
                        self.semantic_analyser.add_error(f"#{self.memory.line_number} : Semantic Error! Type mismatch in operands, got int instead of array.")
                else:
                    self.semantic_analyser.add_error(f"#{self.memory.line_number} : Semantic Error! Type mismatch in operands, got {x2.id_type} instead of int.")

        if x1.address == None or x2.address == None :
            pass
        else:
            if x1.id_type == x2.id_type:
                if x1.is_array == x2.is_array:
                    pass
                else:
                    print(self.memory.line_number , x1 , x2 , "error night")
                    self.semantic_analyser.add_error(f"#{self.memory.line_number} : Semantic Error! Type mismatch in operands, got array instead of int.")
            else:
                    print(self.memory.line_number , x1 , x2 , "error night")
                    self.semantic_analyser.add_error(f"#{self.memory.line_number} : Semantic Error! Type mismatch in operands, got {x1.id_type} instead of {x2.id_type}.")
##################################

        # if type(b) == str :
        #     if b[0] == "#":
        #         pass
        #     else:
        #         if x1.id_type == x2.id_type:
        #             if x1.is_array == x2.is_array:
        #                 pass
        #             else:
        #                 print(self.memory.line_number , x1 , x2 , "error night")
        #                 self.semantic_analyser.add_error(f"#{self.memory.line_number}: got array instead of int")
        #         else:
        #             if x1.id_type != None and x2.id_type != None:
        #                 print(self.memory.line_number , x1 , x2 , "error night")
        #                 self.semantic_analyser.add_error(f"#{self.memory.line_number}: got {x1.id_type} instead of {x2.id_type}")
        # else:
        #     if x1.id_type == x2.id_type:
        #         if x1.is_array == x2.is_array:
        #             pass
        #         else:
        #             print(self.memory.line_number , x1 , x2 , "error night")
        #             self.semantic_analyser.add_error(f"#{self.memory.line_number}: got array instead of int")
        #     else:
        #         if x1.id_type != None and x2.id_type != None:
        #             print(self.memory.line_number , x1 , x2 , "error night")
        #             self.semantic_analyser.add_error(f"#{self.memory.line_number}: got {x1.id_type} instead of {x2.id_type}")


    def negative(self):
        b = self.semantic_stack.pop()
        tmp_address = self.getTemp()
        print("temp_adress ",tmp_address)
        self.memory.program_block.append(f"(SUB, #0, {b}, {tmp_address})")
        self.semantic_stack.append(tmp_address)


    def output(self):
        self.memory.program_block.append(f"(PRINT, {self.semantic_stack.pop()}, , )")

    def end(self):
        self.semantic_stack.pop()

    def whilejump(self, token):
        top = len(self.semantic_stack) - 1
        self.memory.program_block[
            self.semantic_stack[top]] = f"(JPF, {self.semantic_stack[top - 1]},{len(self.memory.program_block) + 1} ,)"
        self.memory.program_block.append(f"(JP, {self.semantic_stack[top - 2]}, , )")
        self.semantic_stack.pop()
        self.semantic_stack.pop()
        self.semantic_stack.pop()

    def label(self, token):
        self.semantic_stack.append(len(self.memory.program_block))

    def save(self, token):
        self.semantic_stack.append(len(self.memory.program_block))
        self.memory.program_block.append("")

    def jpf_save(self, token):
        index1 = self.semantic_stack.pop()
        self.memory.program_block[index1] = f"(JPF, {self.semantic_stack.pop()}, {len(self.memory.program_block) + 1})"
        self.save(token)

    def jp(self, token):
        index1 = self.semantic_stack.pop()
        self.memory.program_block[index1] = f"(JP, {len(self.memory.program_block)}, , )"

    def output_writer(self, final=False):
        file1 = open("report/output.txt", "w+")
        res1 = ""
        i = 0
        for par in self.memory.program_block:
            # res1 += f"{i}  "
            res1 += par
            res1 += '\n'
            i += 1
        file1.write(res1)
        file1.close()

    def return_value_push(self, token):
        self.semantic_stack.append(self.stack.return_value)

    def add_scope(self, type1):
        self.memory.symbol.new_scope()
        self.scope_lists.append_scope(type1)
        pass

    def del_scope(self, type1):
        print("love ", self.memory.tempVarIndex)
        self.memory.symbol.remove_scope()
        self.scope_lists.delete_scope(type1)
        pass

    def add_break_point(self, type1):
        self.scope_lists.add_break_point(type1)

    def fill_break_point(self, type1):
        self.scope_lists.fill_break_point(type1)

    def save_load_variables(self, is_save):
        # print("asd",self.memory.dataVarIndex, self.memory.dataPointer)
        if is_save:
            for d in range(self.memory.dataPointer, self.memory.dataVarIndex, 4):
                self.stack.push(d, "store_data_push")
            for tmp in range(self.memory.tempPointer, self.memory.tempVarIndex, 4):
                self.stack.push(tmp, "store_tmp_push")
            self.stack.save_stack_info()
        else:
            self.stack.load_stack_info()
            for tmp in range(self.memory.tempVarIndex - 4, self.memory.tempPointer - 4, -4):
                self.stack.pop(tmp, "load_tmp_pop")
            for d in range(self.memory.dataVarIndex - 4, self.memory.dataPointer - 4, -4):
                self.stack.pop(d, "load_data_pop")

    # def assign_parameters(self, token):
    #     if not self.main_check:
    #         for i in range(len(self.params) - 1, -1, -1):
    #             tmp = self.getTemp()
    #             self.stack.pop(tmp)
    #             self.semantic_stack.pop()
    #             self.memory.program_block.append(f"(ASSIGN, {tmp}, {self.params[i].address}, )")
    #         self.params = []

    # def push_stack(self, token):
    #     self.stack.push(self.semantic_stack.pop())
    #     if self.is_print:
    #         self.print_params_number += 1

    def function_call(self, token):
        # print(self.semantic_stack)
        self.save_load_variables(True)

        self.memory.program_block.append(f"(ASSIGN, {self.stack.stack_pointer}, {self.stack.last_func_stack_pointer})")

        for arg in range(self.assembler.arg_pointer.pop(), len(self.semantic_stack)):
            self.stack.push(self.semantic_stack.pop(), "push_args")
            # # todo push args

        self.memory.program_block.append(f"(ASSIGN, #{len(self.memory.program_block) + 3}, {self.stack.return_address}, )")
        self.memory.program_block.append(f"(JP, {self.semantic_stack.pop()}, , )")  # jump to function body

        self.memory.program_block.append(f"(ASSIGN, {self.stack.last_func_stack_pointer}, {self.stack.stack_pointer})")

        self.save_load_variables(False)
        return_value = self.getTemp()
        print("return value"  ,return_value)
        self.memory.program_block.append(f"(ASSIGN, {self.stack.return_value}, {return_value}, )")
        self.semantic_stack.append(return_value)

    def param_value(self, token):
        self.get_param_value = True

    def param_value_end(self, token):
        self.get_param_value = False

    def first_function(self, token):
        if token == "(":
            if not self.first_func:
                self.first_func = True
                length = len(self.memory.program_block)
                self.jump_to_main_address = length - 1
                temp = self.memory.program_block[length - 1]
                self.memory.program_block[length - 1] = "this place for jump to main"
                self.memory.program_block.append(temp)
                # self.memory.program_block.append("this place is for jump")

    def check_main(self, token):
        if token == "main":
            self.memory.program_block.append("")
            self.memory.program_block.append("code starts")
            self.memory.dataPointer = self.memory.dataVarIndex
            self.memory.tempPointer = self.memory.tempVarIndex
            self.function_first_detail.append(f"(ASSIGN, #0, 858585, )")
            self.function_first_detail.append(f"(ASSIGN, #0, 868686, )")
            self.function_first_detail.append(f"(ASSIGN, #0,  878787, )")
            self.function_first_detail.append(f"(ASSIGN, #555555,  1000, )")
            for code in self.function_first_detail:
                self.memory.program_block.append(code)
            self.main_check = True
            if self.first_func:
                self.memory.program_block[
                    self.jump_to_main_address] = f"(JP, {len(self.memory.program_block) - len(self.function_first_detail)}, , )"

    def function_address(self):
        # function_address = self.semantic_stack[len(self.semantic_stack) - 1]
        self.function_first_detail.append(
            f"(ASSIGN, #{len(self.memory.program_block)}, {self.semantic_stack.pop()} , )")
        # self.memory.program_block.append(f"function(ASSIGN, #{len(self.memory.program_block)}, {self.semantic_stack.pop()} , )")

    def find_var(self, id):
        return self.memory.symbol.fetch(id)

    def declare_func(self, token=None):
        self.memory.dataPointer = self.memory.dataVarIndex
        self.memory.tempPointer = self.memory.tempVarIndex

        # only when zero init is activated
        self.memory.program_block[-1] = ""

        id_record = self.info[-1]
        id_record.is_function = True
        print(id_record.is_function, 909)
        id_record.address = len(self.memory.program_block) # todo hosein

    def set_exec(self, token=None):
        if not self.assembler.set_exec:
            self.assembler.set_exec = True
            func = self.semantic_stack.pop()
            self.memory.program_block.pop()
            self.semantic_stack.append(len(self.memory.program_block))
            self.memory.program_block.append("")
            self.semantic_stack.append(func)

    def declare(self, token=None):
        self.memory.symbol.set_declaration(True) # todo hosein
        self.last_id_type.append(token)
        if self.assembler.arg_dec:
            self.function_parameters_types.append(token)
            self.function_parameters_is_array.append(True)


    def jump_while(self, token=None):
        head1 = self.semantic_stack.pop()
        head2 = self.semantic_stack.pop()
        self.memory.program_block.append(f"(JP, {self.semantic_stack.pop()}, , )")
        # self.semantic_stack.append(head2)
        # self.semantic_stack.append(head1)
        self.memory.program_block[
            head1] = f"(JPF, {head2}, {len(self.memory.program_block)}, )"

    def declare_id(self, token):
        self.memory.symbol.declare_symbol(token, self.last_id_type[-1])
        x1 = self.find_var(token)
        x1.id_type = self.last_id_type[-1]
        if x1.id_type == "void" and self.scope_lists.is_in_function(): #todo
            self.semantic_analyser.add_error(f"#{self.memory.line_number} : Semantic Error! Illegal type of void for '{x1.token.lexeme}'")

        print(x1)
        self.info.append(x1)
        print(1400, x1)
        id_record = self.find_var(token)   # todo hosein
        print(1401, id_record)
        print([-1])
        print("id_record", id_record)
        # print(self.memory.dataVarIndex)
        id_record.address = self.getDataAdd() # todo hosein
        self.assembler.last_id = token
        # print(self.assembler.arg_dec , token , "hello")
        if self.assembler.arg_dec:
            self.arg_assign(id_record.address)
            self.last_arg_name = token
            self.function_parameters_number += 1
        else:
            self.last_id_name = token
            self.memory.program_block.append(f"(ASSIGN, #0, {id_record.address}, )")
            pass

    def check_void(self, token = None):
        x1 = self.find_var(self.last_id_name)
        print("lasrrr",self.last_id_name)
        if x1.id_type == "void" and not x1.is_function:
            self.semantic_analyser.add_error(f"#{self.memory.line_number} : Semantic Error! Illegal type of void for {x1.token.lexeme}")

    def arg_pass(self, token=None):
        self.assembler.arg_pointer.append(len(self.semantic_stack))
        print("arg_pass1", self.arg_pass_number, self.last_arg_good_name)
        self.arg_pass_number = 0

    def arg_pass_finish(self, token=None):
        print("887")
        print(self.arg_pass_number)
        print(self.last_arg_good_name)
        if self.arg_pass_number !=len(self.last_arg_good_name.args_type):
            if self.last_arg_good_name.token.lexeme == "output":
                # if self.arg_pass_number != 1:
                #     self.semantic_analyser.add_error(
                #         f"#{self.memory.line_number}:semantic error! Mismatch in numbers of arguments of {self.last_arg_good_name.token.lexeme}")
                pass

            else:
                self.semantic_analyser.add_error(f"#{self.memory.line_number} : Semantic Error! Mismatch in numbers of arguments of '{self.last_arg_good_name.token.lexeme}'.")
        else:
            nums1 = self.arg_pass_number
            index = 1
            for i1 in range(nums1):
                tmp1 = "array"
                print(self.last_arg_good_name)
                if self.last_arg_good_name.args_isArray[i1]:
                    tmp1 = "int"
                tmp2 = "int"
                print(self.info[-(nums1 - i1)] , "salamati")
                if self.info[-(nums1 - i1)].is_array:
                    tmp2 = "array"
                if tmp2 != tmp1:
                    self.semantic_analyser.add_error(f"#{self.memory.line_number} : Semantic Error! Mismatch in type of argument {index} of '{self.last_arg_good_name.token.lexeme}'. Expected '{tmp1}' but got '{tmp2}' instead.")
                index += 1
        self.arg_pass_number = -1

    def arg_init(self, token=None):
        self.assembler.arg_dec = True
        # print("arg_init_done")

    def arg_finish(self, token=None):
        self.assembler.arg_dec = False
        x = self.find_var(self.last_id_name)
        x.no_args = self.function_parameters_number
        x.args_type = self.function_parameters_types
        x.args_isArray = self.function_parameters_is_array
        print(x,1500)
        self.function_parameters_types = []
        self.function_parameters_is_array = []
        self.function_parameters_number = 0

    def arg_assign(self, address):
        self.stack.pop(address, "arg_assign")

    def end_code(self):
        id_record = self.find_var("main")
        print(111123332, self.semantic_stack, id_record.address)
        self.memory.program_block[self.semantic_stack.pop()] = f"(JP, {id_record.address}, , )"
        self.output_writer()

    def get_temp_save(self):
        temp1 = self.getTemp()
        self.semantic_stack.append(temp1)
        length = len(self.memory.program_block)
        print(len(self.memory.program_block))
        self.memory.program_block.append(f"(ASSIGN, #{length + 2}, {temp1}, )")
        temp2 = self.getTemp()
        self.semantic_stack.append(temp2)
        self.semantic_stack.append(len(self.memory.program_block))
        self.memory.program_block.append("for jump")

    def assign_jp(self):
        self.memory.program_block.append(f"(ASSIGN, {self.semantic_stack[-1]}, {self.semantic_stack[-2]}, )")
        self.memory.program_block.append(f"(JP, @{self.semantic_stack[-4]}, , )")
        self.semantic_stack.pop()

    def jp_fill_save(self):
        length = len(self.memory.program_block)
        print("")
        self.memory.program_block[self.semantic_stack[-1]] = f"(ASSIGN, #{length + 1}, {self.semantic_stack[-2]}, )"
        self.semantic_stack.pop()
        self.semantic_stack.pop()
        self.semantic_stack.append(length)
        self.memory.program_block.append("")

    def for_(self):
        self.memory.program_block.append(f"(ADD, {self.semantic_stack[-2]}, #2, {self.semantic_stack[-2]})")
        self.memory.program_block.append(f"(JP, @{self.semantic_stack[-2]}, , )")
        length = len(self.memory.program_block)
        self.memory.program_block[self.semantic_stack[-1]] = f"(JP, {length}, , )"
        self.semantic_stack.pop()
        self.semantic_stack.pop()
        # self.semantic_stack.pop()

class Assembler:
    def __init__(self):
        self.arg_dec = False
        self.set_exec = False
        self.arg_pointer = []
        self.data_pointer = 0
        self.temp_pointer = 0
        self.last_id = None
        self.temp_address = 0
        self.data_address = 0
        self.stack_address = 0
        self.program_block = []