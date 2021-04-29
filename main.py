from scanner.scanner import Scanenr
from parsr.grammar import Grammar
from parsr.initialize import Initializer
from parsr.parser import Parser

initialize = Initializer()
g = Grammar('parsr/', initialize)
parse_table = g.get_parse_table()
for x in parse_table.keys():
    print(x, ":", parse_table[x])

scannar1 = Scanenr("input.txt")
# Parser(scannar1, parse_table).parsing()
Parser(scannar1,parse_table,initialize)

# while True:
#     token = scannar1.get_token()
#     # print(token)
#     if token[2] == "♤":
#         break


