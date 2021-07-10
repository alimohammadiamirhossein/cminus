from collections import namedtuple
from enum import Enum

class IDRecord:
    def __init__(self, token=None, element_type=None, no_args=None, id_type=None, scope=None, address=None):
        self.token = token
        self.element_type = element_type
        self.is_function = False
        self.no_args = no_args
        self.is_array = False
        self.args_type = []
        self.args_isArray = []
        self.id_type = id_type
        self.scope = scope
        self.address = address

    def __str__(self):
        return f"{self.token.lexeme}:" \
               f"{self.token},add{self.address}:type {self.id_type}:scope {self.scope.scope_number}: " \
               f"numbers {self.no_args}: args_type {self.args_type} " \
               f": is array {self.is_array} : is arg array {self.args_isArray}"


class Scope:
    def __init__(self, parent=None, scope_number = 1):
        self.stack = []
        self.stack_array = []
        self.parent = parent
        self.scope_number = scope_number

    def append(self, token, force=False, has_lexeme=False, id_record_type=None):
        if force:
            if id_record_type:
                return self.__append(token, id_record_type)
            else:
                return self.__append(token)
        if has_lexeme:
            id_record = self.get_IDrecord(token)
        else:
            id_record = self.get_IDrecord(token.lexeme)
        if id_record:
            return id_record
        else:
            if id_record_type:
                return self.__append(token, id_record_type)
            else:
                return self.__append(token)

    def __append(self, token, id_type=None):
        id_record = IDRecord(token, None, None, id_type=id_type, scope=self, address=None)
        self.stack.append(id_record)
        return id_record

    def get_IDrecord(self, lexeme):
        # print("sss", lexeme, self.scope_number)
        for record in self.stack:
            if record.token.lexeme == lexeme :
                return record
        if self.parent:
            return self.parent.get_IDrecord(lexeme)
        return None

    def get_IDrecord_from_address(self, address):
        # print("sss", lexeme, self.scope_number)
        for record in self.stack:
            if record.address == address:
                return record
        if self.parent:
            return self.parent.get_IDrecord_from_address(address)
        return None

    def __str__(self):
        to_string = ""
        for record in self.stack:
            to_string += record

    def get_stack(self):
        for x in self.stack:
            print(x.token.lexeme, x.address, end=' stack ')


class SymbolTable:
    keyword = ["if", "else", "void", "int", "while", "break", "switch", "default", "case", "return"]

    def __init__(self):
        self.is_declaration = False
        self.scopes = []
        self.ids = []
        self.scopes.append(Scope())
        self.is_first = True
        self.last_semantic_id = None
        self.second_scope_info = None

    def new_scope(self):
        if self.is_first:
            self.is_first = False
        self.scopes.append(Scope(self.scopes[-1], self.scopes[-1].scope_number+1))
        self.second_scope_info = Scope(self.scopes[-1], self.scopes[-1].scope_number+1)
        print("add1", len(self.scopes), self.scopes[-1].parent.get_stack())

    def remove_scope(self):
        self.second_scope_info = Scope(self.scopes[-1], self.scopes[-1].scope_number+1)
        print('remove', len(self.scopes))
        self.scopes.pop()

    def get_current_scope(self):
        if len(self.scopes) > 0:
            self.second_scope_info = Scope(self.scopes[-1], self.scopes[-1].scope_number+1)
        return self.scopes[-1]

    def add_symbol(self, token):
        if token.lexeme in self.keyword:
            temp = token.lexeme
            print("debug add_symbol" , token)
            if token == None:
                print("bad token")
            return Token(TokenType.KEYWORD, token.lexeme)
        self.get_current_scope().append(token, self.is_declaration)
        self.set_declaration(False)
        return token

    def declare_symbol(self, lexeme, id_type=None):
        token = Token(TokenType.ID, lexeme)
        self.get_current_scope().append(token, True)

    def fetch(self, lexeme):
        # print("lexeme" , lexeme)
        scope = self.get_current_scope()
        for id in scope.stack:
            print(id)
        return  scope.get_IDrecord(lexeme)

    def fetch_from_address(self , address):
        return self.get_current_scope().get_IDrecord_from_address(address)

    def set_declaration(self, state):
        self.is_declaration = state

    def __str__(self):
        s = ""
        for i, t in enumerate(self.keyword + self.ids):

            s += f"{i}.\t{t}\n"
        return s




class TokenType(Enum):
    NULL = 0
    ID = 1
    EMPTY = 5
    BUG = 7
    NOTBUG = 8
    FINISH = 9
    NOTFINISH = 10
    PARSER = 11
    KEYWORD = 2
    NUM = 3
   # 1111101       }



Token = namedtuple('Token', 'type lexeme')