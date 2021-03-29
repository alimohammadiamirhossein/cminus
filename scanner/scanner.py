from file_reader import FileReader
from regex import Regex

fr = FileReader(path="input.txt")
regex_ = Regex()
current_state = regex_.state_zero

while not fr.is_last_line:
    if fr.current_char == len(fr.backup_line) - 1:
        fr.load_backup_line()
    x = fr.forward_read()
    current_state = current_state.get_next_state(x)


