from scanner.file_reader import FileReader
from scanner.regex import Regex
from scanner.state import FinalState, State, ErrorState
from scanner.file_writer import FileWriter
from scanner.interval import Interval, OtherTypeInterval


class Scanenr:
    def __init__(self, address):
        self.fr = FileReader(path=address)
        self.fw = FileWriter()
        self.regex_ = Regex()
        # self.current_state = self.regex_.state_zero

    def get_token(self):
        current_state = self.regex_.state_zero
        while not self.fr.is_last_line:
            if self.fr.current_char == len(self.fr.backup_line) - 1:
                self.fr.load_backup_line()
            if not self.fr.is_last_line:
                x = self.fr.forward_read()
            else:
                x = "♤"

            if current_state.stateID == "0" and x == "♤":
                break
            current_state = current_state.get_next_state(x)
            if isinstance(current_state, FinalState):
                if current_state.is_backward() and x != "♤":
                    self.fr.backward_read()
                token = self.fr.return_token()  # it must'nt delete
                if current_state.stateID != 'f' and current_state.stateID != 'c':
                    state_id = current_state.__str__()
                    if x == "♤":
                        token = current_state.str1
                    if state_id == "KEYWORD":
                        self.fw.add_symbol_to_symbol_table(token)
                        if not State.is_keyword(token):
                            state_id = "ID"
                    self.fw.tokens_writer(self.fr.current_line, state_id, token)
                    return self.fr.current_line, state_id, token

                current_state = self.regex_.state_zero
            if isinstance(current_state, ErrorState):
                if current_state.is_backward():
                    self.fr.backward_read()
                ErrorState.noError = False
                errorType = current_state.typeError()
                errorToken = self.fr.return_token()  #
                line_number = self.fr.current_line
                if current_state.stateID == "e2":
                    str_tmp = ""
                    i = -2
                    for char in current_state.str1:
                        if i == 5:
                            str_tmp += "..."
                        i += 1
                        if char == "\n":
                            if i < 6:
                                str_tmp += "\\n"
                            line_number -= 1
                        elif i < 6:
                            str_tmp += char
                    self.fw.lexical_errors(line_number, errorType, str_tmp)
                else:
                    self.fw.lexical_errors(line_number, errorType, errorToken)
                current_state = self.regex_.state_zero

        self.fw.tokens_writer(self.fr.current_line+1, "", "♤")
        return self.fr.current_line, "", "♤"
        self.fw.write_symbol_table()
        self.fw.lexical_error_write()
