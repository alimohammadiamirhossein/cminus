from scanner.scanner import Scanenr
from parsr.grammar import Grammar
from parsr.initialize import Initializer

scanener1 = Scanenr("input.txt")
while True:
    token = scanener1.get_token()
    # print(token)
    if token[2] == "♤":
        break

initialize = Initializer()
g = Grammar('parsr/', initialize)
