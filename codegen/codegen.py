from codegen.scope import ScopeLists
from codegen.stack import Stack
from codegen.tables import tables

class Memory:
    def __init__(self, symbol_table, dataVar=0, tempVar=0):
        self.program_block = []
        self.symbol = symbol_table
        self.tempVarIndex = tempVar
        self.dataVarIndex = dataVar
        self.tempPointer = tempVar
        self.dataPointer = dataVar


class CodeGen:

    def __init__(self, symbol):
        self.semantic_stack = []
        self.memory = Memory(symbol)
        self.stack = Stack(self.memory.program_block, 1000, 858585, 868686, 878787)
        self.memory.dataVarIndex = 500
        self.memory.dataPointer = 500
        self.memory.tempVarIndex = 0
        self.memory.tempPointer = 0
        self.scope_lists = ScopeLists(self.memory)
        self.get_param_value = False
        self.assembeler = Assembler()
        self.assembler.data_address = 500
        self.assembler.stack_address = 1000
        self.assembler.temp_address = 900


        self.params = []
        self.first_func = False
        self.jump_to_main_address = 0
        self.main_check = False
        self.is_print = False
        self.print_params_number = 0
        self.function_first_detail = []

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
        token = token[2]
        print(token, actionName)
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
        elif actionName == "check_main":
            self.check_main(token)



        elif actionName == "declare_func":
            self.declare_func(token)
        elif actionName == "set_exec":
            self.set_exec(token)
        elif actionName == "jump_while":
            self.jump_while(token)
        elif actionName == "arg_pass":
            self.arg_pass(token)
        elif actionName == "arg_init":
            self.arg_pass(token)
        elif actionName == "arg_finish":
            self.arg_pass(token)
        elif actionName == "arg_assign":
            self.arg_pass(token)




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

        print(self.semantic_stack)
        # print(actionName)
        print(self.memory.program_block, token)
        # print(self.symbol.symbol_table)
        # print(token)
        # print(11111111111111111111111111111111111)
        self.output_writer()

    # here we have the function of actions
    def pid(self, token):
        if token == "output":
            self.is_print = True
            self.print_params_number = 0
        else:
            x = self.memory.symbol.find_symbol(token)
            self.semantic_stack.append(x.address)

    def pnum(self, token):
        self.semantic_stack.append(f"#{token}")

    def parray(self, token=None):
        len1 = self.semantic_stack.pop()
        tmp_address = self.getTemp()
        array_start_address = self.semantic_stack.pop()
        self.memory.program_block.append(f"(MULT, #4, {len1}, {tmp_address})")
        self.memory.program_block.append(f"(ADD, #{array_start_address}, {tmp_address}, {tmp_address})")
        self.semantic_stack.append(f"@{tmp_address}")

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
        len1 = self.semantic_stack.pop()
        address1 = self.semantic_stack.pop()
        len1 = int(len1[1:])
        len1 -= 1
        for i in range(len1):
            self.getDataAdd()
            self.memory.program_block.append(f"(ASSIGN, #0, {address1 + 4}, )")
            address1 += 4

    def assign(self, token=None):
        value = self.semantic_stack.pop()
        self.getTemp()
        assign_par = self.semantic_stack.pop()
        self.memory.program_block.append(f"(ASSIGN, {value}, {assign_par}, )")
        self.semantic_stack.append(assign_par)

    def op_push(self, token):
        self.semantic_stack.append(token)

    def jump_return_address(self, token):
        self.memory.program_block.append(f"(JP, @{self.stack.return_address}, , )")

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
        self.memory.program_block.append(f"({op}, {a}, {b}, {tmp_address})")
        self.semantic_stack.append(tmp_address)

    def negative(self):
        b = self.semantic_stack.pop()
        tmp_address = self.getTemp()
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

    def output_writer(self):
        file1 = open("report/output.txt", "w+")
        res1 = ""
        i = 0
        for par in self.memory.program_block:
            res1 += f"{i}\t"
            res1 += par
            res1 += '\n'
            i += 1
        file1.write(res1)
        file1.close()

    def return_value_push(self, token):
        self.semantic_stack.append(self.stack.return_value)

    def add_scope(self, type1):
        tables.get_symbol_table().new_scope()
        self.scope_lists.append_scope(type1)
        pass

    def del_scope(self, type1):
        tables.get_symbol_table().remove_scope()
        self.scope_lists.delete_scope(type1)
        pass

    def add_break_point(self, type1):
        self.scope_lists.add_break_point(type1)

    def save_load_variables(self, is_save):
        if is_save:
            for d in range(self.memory.dataPointer, self.memory.dataVarIndex, 4):
                self.stack.push(d)
            for tmp in range(self.memory.tempPointer, self.memory.tempVarIndex, 4):
                self.stack.push(tmp)
            self.stack.save_stack_info()
        else:
            self.stack.load_stack_info()
            for tmp in range(self.memory.tempVarIndex - 4, self.memory.tempPointer - 4, -4):
                self.stack.pop(tmp)
            for d in range(self.memory.dataVarIndex - 4, self.memory.dataPointer - 4, -4):
                self.stack.pop(d)

    def assign_parameters(self, token):
        if not self.main_check:
            for i in range(len(self.params) - 1, -1, -1):
                tmp = self.getTemp()
                self.stack.pop(tmp)
                self.semantic_stack.pop()
                self.memory.program_block.append(f"(ASSIGN, {tmp}, {self.params[i].address}, )")
            self.params = []

    def push_stack(self, token):
        self.stack.push(self.semantic_stack.pop())
        if self.is_print:
            self.print_params_number += 1

    def function_call(self, token):
        if self.is_print:
            self.semantic_stack.append(99999999)  # just for expresion end
            self.is_print = False
            array_tmp = []
            for i in range(self.print_params_number):
                tmp1 = self.getTemp()
                self.stack.pop(tmp1)
                array_tmp.append(tmp1)
            for i in range(self.print_params_number - 1, -1, -1):
                self.memory.program_block.append(f"(PRINT, {array_tmp[i]}, , )")
        else:
            # self.save_load_variables(True)
            # todo push args
            self.memory.program_block.append(
                f"(ASSIGN, #{len(self.memory.program_block) + 2}, {self.stack.return_address}, )")
            self.memory.program_block.append(f"(JP, @{self.semantic_stack.pop()}, , )")  # jump to function body
            # self.save_load_variables(False)
            return_value = self.getTemp()
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

    @staticmethod
    def find_var(id):
        return tables.get_symbol_table().fetch(id)

    def declare_func(self, token=None):
        self.assembler.data_pointer = self.assembler.data_address
        self.assembler.temp_pointer = self.assembler.temp_address

        # only when zero init is activated
        self.assembler.program_block[-1] = ""

        id_record = self.find_var(self.assembler.last_id.lexeme) # todo hosein
        id_record.address = len(self.assembler.program_block) # todo hosein


    def set_exec(self, token=None):
        if not self.assembler.set_exec:
            self.assembler.set_exec = True
            func = self.semantic_stack.pop()
            self.memory.program_block.pop()
            self.semantic_stack.append(len(self.assembler.program_block))
            self.memory.program_block.append("")
            self.semantic_stack.append(func)

    @staticmethod
    def declare(Token=None):
        tables.get_symbol_table().set_declaration(True) # todo hosein


    def jump_while(self, token=None):
        head1 = self.semantic_stack.pop()
        head2 = self.semantic_stack.pop()
        self.assembler.program_block.append(f"(JP, {self.semantic_stack.pop()}, , )")
        self.semantic_stack.append(head2)
        self.semantic_stack.append(head1)
        self.assembler.program_block[
            head1] = f"(JPF, {head2}, {len(self.memory.program_block)}, )"

    def declare_id(self, token):
        id_record = self.find_var(token.lexeme)   # todo hosein
        id_record.address = self.get_data_var() # todo hosein
        self.assembler.last_id = token
        if self.assembler.arg_dec:
            self.arg_assign(id_record.address)
        else:
            self.assembler.program_block.append(f"(ASSIGN, #0, {id_record.address}, )")
            pass

    def arg_pass(self, token=None):
        self.assembler.arg_pointer.append(len(self.semantic_stack))

    def arg_init(self, token=None):
        self.assembler.arg_dec = True

    def arg_finish(self, token=None):
        self.assembler.arg_dec = False

    def arg_assign(self, address):
        self.stack.pop(address)

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


