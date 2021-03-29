from scanner.file_reader import FileReader
from scanner.regex import Regex

fr = FileReader(path="scanner//input.txt")
regex_ = Regex()
current_state = regex_.state_zero


while not fr.is_last_line:
    if fr.current_char == len(fr.backup_line) - 1:
        fr.load_backup_line()
    x = fr.forward_read()
    print(x, end="")
    print(current_state)
    current_state = current_state.get_next_state(x)

