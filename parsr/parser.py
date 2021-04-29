from anytree import Node, RenderTree
from parsr.initialize import Initializer
from parsr.state import State, Terminal, NonTerminal


# class Parser:
#     def __init__(self, scanner, parse_table):
#         self.scanner = scanner
#         self.parse_table = parse_table
#         self.current_token = ""
#         self.current_token_details = ""
#         self.stack = [['♤', 'Terminal'], ['Declarationlist', 'Non-Terminal']]
#         self.nodes = []
#         self.tree_str = ""
#
#     def parsing(self):
#         self.get_new_token()
#         node1 = -1
#         while self.current_token != '♤':
#             A = self.stack.pop()
#             node_ = self.find_node(A[0])
#             if node_ == -1:
#                 node_ = Node(A[0])
#             if node1 == -1:
#                 node1 = node_
#             if A[1] != "Terminal":
#                 print(self.parse_table[A[0]][self.current_token], '     ', self.current_token,'   ', A)
#             if A[1] == "Terminal":
#                 if A[0] == self.current_token:
#                     self.get_new_token()
#                 elif A[0] == 'ε':
#                     pass
#                 else:
#                     print("error", self.current_token_details)
#             elif self.parse_table[A[0]][self.current_token][0][0] == 'empty':
#                 self.get_new_token()
#                 self.stack.append(A)
#                 print("empty", self.current_token_details)
#             elif self.parse_table[A[0]][self.current_token][0][0] == 'sync':
#                 print("sync", self.current_token_details)
#             else:
#                 if node_ in self.nodes:
#                     self.nodes.remove(node_)
#                 self.add_to_stack(self.parse_table[A[0]][self.current_token], node_)
#         self.tree_str_maker(node1)
#
#     def tree_str_maker(self, node1):
#         file_ = open("report/parse_tree.txt", "w+", encoding='utf-8')
#         result = ""
#         for pre, fill, node in RenderTree(node1):
#             if node.name == 'ε':
#                 result += f"{pre}epsilon\n"
#             else:
#                 result += f"{pre}{node.name}\n"
#         file_.write(result)
#         file_.close()
#
#     def get_new_token(self):
#         self.current_token_details = self.scanner.get_token()
#         print(12, self.current_token_details)
#         self.current_token = self.current_token_details[2]
#         if self.current_token_details[1] == "ID":
#             self.current_token = self.current_token_details[1]
#         elif self.current_token_details[1] == "NUM":
#             self.current_token = self.current_token_details[1]
#
#     def add_to_stack(self, list1, node2):
#         for element in list1:
#             x = Node(element[0], parent=node2)
#             self.nodes.append(x)
#         for i in range(len(list1) - 1, -1, -1):
#             self.stack.append(list1[i])
#
#     def find_node(self, name2):
#         for element2 in self.nodes:
#             if element2.name == name2:
#                 return element2
#         return -1


# we have to make self.lookahead a global variable or to return self.lookahead in match function
class Parser:
    def __init__(self, scanner, parse_table, Initializer):
        self.scanner = scanner
        self.parse_table = parse_table
        self.initializer = Initializer
        self.lookahead = scanner.get_token()
        file = open("report/parse_tree.txt", "w+", encoding='utf-8')
        errors = open("report/errors.txt", "w+", encoding='utf-8')
        node1 = Node("XX")
        self.Procedure("Program",  1, scanner, 0, file, errors, node1)
        end_node = Node("$", parent=node1.children[0])
        result = ""
        i = 1
        for pre, fill, node in RenderTree(node1.children[0]):
            if node.name == 'ε':
                result += f"{pre}epsilon\n"
            else:
                result += f"{pre}{node.name}\n"
        # print(result)
        file.write(result)
        file.close()
        errors.close()

    def Procedure(self, nonTerminal,  lineNumber, scannar1, tabs, file,
                  errors, parent):  # we have to have line number
        i = 2
        if self.lookahead[1] == "NUM" or self.lookahead[1] == "ID":
            i = 1
        node1 = Node(nonTerminal, parent=parent)
        if self.parse_table[nonTerminal][self.lookahead[i]][0][0] != "empty":  # checks if it is not empty
            if self.parse_table[nonTerminal][self.lookahead[i]][0][0] == "ε":
                node1 = Node("epsilon", parent=parent)
                # print(nonTerminal)
                # print(self.parse_table[nonTerminal])
                # return
            elif self.parse_table[nonTerminal][self.lookahead[i]][0][0] == "sync":
                # errors.write("missing %s on line %s \n", (nonTerminalObject.first[0], lineNumber))
                errors.write("missing on line %s \n" % (self.lookahead[0]))
            else:
                for x in self.parse_table[nonTerminal][self.lookahead[i]]:
                    temp = x[0]
                    temp1 = x[1]
                    if temp1 == "Non-Terminal":
                        self.Procedure(temp, lineNumber, scannar1, tabs + 1, file, errors, node1)
                    else:
                        self.Match(temp, lineNumber, scannar1, tabs + 1, file, errors, node1)
        else:  # if it is empty
            errors.write("illegal %s on line %s \n" % (self.lookahead, lineNumber))
            self.lookahead = scannar1.get_token()
            self.Procedure(nonTerminal, lineNumber, scannar1, tabs + 1, file, errors, node1)

    def Match(self, terminal, lineNumber, scanner, tabs, file, errors, parent):
        i = 2
        if self.lookahead[1] == "NUM" or self.lookahead[1] == "ID":
            i = 1
        node_name = self.lookahead[1] +", "+ self.lookahead[2]
        node1 = Node(f"({node_name})", parent=parent)
        if self.lookahead[i] == terminal:
            # for i in range(tabs):
                # file.write("\t".rstrip('\n'))
            # file.write("%s \n" % (terminal))
            self.lookahead = scanner.get_token()
        else:
            errors.write("missing %s on line %s \n" % (terminal, lineNumber))