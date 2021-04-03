from scanner.file_reader import FileReader
from scanner.regex import Regex
from scanner.state import FinalState, State, ErrorState
from scanner.file_writer import FileWriter
from scanner.interval import Interval, OtherTypeInterval

fr = FileReader(path="scanner//input.txt")
fw = FileWriter()
regex_ = Regex()
current_state = regex_.state_zero


while not fr.is_last_line:
    if fr.current_char == len(fr.backup_line) - 1:
        fr.load_backup_line()
    if not fr.is_last_line:
        x = fr.forward_read()
    else:
        x = "EOF"
        fw.tokens_writer(fr.current_line+1, "", "EOF")

    current_state = current_state.get_next_state(x)
    if isinstance(current_state, FinalState):
        if current_state.is_backward():
            fr.backward_read()
        token = fr.return_token()  # it must'nt delete
        if current_state.stateID != 'f' and current_state.stateID != 'c':
            state_id = current_state.__str__()
            if state_id == "KEYWORD" and not State.is_keyword(token):
                state_id = "ID"
            fw.tokens_writer(fr.current_line, state_id, token)
        current_state = regex_.state_zero
    if isinstance(current_state, ErrorState):
        ErrorState.noError = False
        errorType = current_state.typeError()
        errorToken = fr.return_token()  #
        line_number = fr.current_line
        if current_state.stateID == "e2":
            str_tmp = "/*"
            i = 0
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
            fw.lexical_errors(line_number, errorType, str_tmp)
        else:
            fw.lexical_errors(line_number, errorType, errorToken)
        current_state = regex_.state_zero

ErrorState.checkNoError()

