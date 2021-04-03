from scanner.file_reader import FileReader
from scanner.regex import Regex
from scanner.state import FinalState, State , ErrorState
from scanner.interval import Interval, OtherTypeInterval

fr = FileReader(path="scanner//input.txt")
regex_ = Regex()
current_state = regex_.state_zero

while not fr.is_last_line:
    if fr.current_char == len(fr.backup_line) - 1:
        fr.load_backup_line()
    if not fr.is_last_line:
        x = fr.forward_read()
    else:
        x = "EOF"
    # print(current_state)
    # print("@",current_state, x, "@", current_state.get_next_state(x), end="$")

    current_state = current_state.get_next_state(x)
    if isinstance(current_state, FinalState):
        if current_state.is_backward():
            fr.backward_read()
        token = fr.return_token()  #it must'nt delete
        if current_state.stateID != 'f' and current_state.stateID != 'c':
            print((current_state.__str__(), token))
        current_state = regex_.state_zero
    if isinstance(current_state, ErrorState):
        current_state.typeError()
        # remove bad characters and continue

