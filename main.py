from scanner.scanner import Scanenr
from parsr.grammar import Grammar
from parsr.initialize import Initializer
from parsr.parser import Parser
import filecmp

initialize = Initializer()
g = Grammar('parsr/', initialize)
parse_table = g.get_parse_table()
# for x in parse_table.keys():
#     print(x, ":", parse_table[x])

scannar1 = Scanenr("input.txt")
# Parser(scannar1, parse_table).parsing()
Parser(scannar1,parse_table,initialize)

# while True:
#     token = scannar1.get_token()
#     # print(token)
#     if token[2] == "♤":
#         break

# reading files
f1 = open("report/parse_tree.txt", "r")
f2 = open("parsr/parse_tree3.txt", "r")

i = 0

for line1 in f1:
    i += 1

    for line2 in f2:

        # matching line1 from both files
        if line1 == line2:
            # print IDENTICAL if similar
            print("Line ", i, ": IDENTICAL")
        else:
            print("Line ", i, ":")
            # else print that line from both files
            print("\tFile 1:", line1, end='')
            print("\tFile 2:", line2, end='')
        break

# closing files
f1.close()
f2.close()



# f1 = "report/parse_tree.txt"
# f2 = "parsr/parse_tree3.txt"
#
# result = filecmp.cmp(f1, f2)
# print(result)
