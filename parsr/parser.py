from anytree import Node, RenderTree
from parsr.initialize import Initializer
from parsr.state import State, Terminal, NonTerminal


#sani kiri
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