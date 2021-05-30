from anytree import Node, RenderTree
from parsr.initialize import Initializer
from parsr.state import State, Terminal, NonTerminal
from codegen.codegen import CodeGen


class Parser:
    def __init__(self, scanner, parse_table, Initializer, CodeGen):
        self.codegen = CodeGen
        self.scanner = scanner
        self.parse_table = parse_table
        self.initializer = Initializer
        self.lookahead = scanner.get_token()
        self.noError = True
        self.is_end = False
        self.is_end_line = -1
        file = open("report/parse_tree.txt", "w+", encoding='utf-8')
        errors = open("report/syntax_errors.txt", "w+", encoding='utf-8')
        node1 = Node("XX")
        self.Procedure("Program",  scanner,  file, errors, node1)
        if not self.is_end:
            end_node = Node("$", parent=node1.children[0])
        result = ""
        i = 1
        for pre, fill, node in RenderTree(node1.children[0]):
            if node.name == 'ε':
                result += f"{pre}epsilon\n"
            else:
                result += f"{pre}{node.name}\n"
        file.write(result)
        file.close()
        if self.noError:
            errors.write("There is no syntax error.\n")
        if self.is_end:
            errors.write(f"#{self.is_end_line+1} : syntax error, unexpected EOF")
        errors.close()

    def Procedure(self, nonTerminal,  scannar1,  file, errors, parent):  # we have to have line number
        i = 2
        if self.lookahead[1] == "NUM" or self.lookahead[1] == "ID":
            i = 1
        if self.parse_table[nonTerminal][self.lookahead[i]][0][0] != "sync" and self.parse_table[nonTerminal][self.lookahead[i]][0][0] != "empty" :
            if not self.is_end:
                node1 = Node(nonTerminal, parent=parent)
        if self.parse_table[nonTerminal][self.lookahead[i]][0][0] != "empty":  # checks if it is not empty
            if self.parse_table[nonTerminal][self.lookahead[i]][0][0] == "ε":
                if not self.is_end:
                    nedex = Node("epsilon", parent=node1)
            elif self.parse_table[nonTerminal][self.lookahead[i]][0][0] == "sync":
                if not self.is_end :
                    errors.write("#%s : Syntax Error, Missing %s \n" % (self.lookahead[0] , nonTerminal))
                    self.noError = False
            else:
                for x in self.parse_table[nonTerminal][self.lookahead[i]]:
                    temp = x[0]
                    temp1 = x[1]
                    if temp1 == "hashtag":
                        self.codegen.checkAction(temp, self.lookahead[i])
                    else :
                        if temp1 == "Non-Terminal":
                            self.Procedure(temp,scannar1,  file, errors, node1)
                        else:
                            self.Match(temp,  scannar1,  file, errors, node1)
                            
        else:
            if not self.is_end :
                errors.write("#%s : syntax error, illegal %s \n" % (self.lookahead[0], self.lookahead[i]))
            self.noError = False
            self.lookahead = scannar1.get_token()
            if self.lookahead[2] != "♤":
                self.Procedure(nonTerminal,  scannar1,  file, errors, parent)
            else:
                self.is_end = True
                self.is_end_line = self.lookahead[0]

    def Match(self, terminal,  scanner,  file, errors, parent):
        i = 2
        if self.lookahead[1] == "NUM" or self.lookahead[1] == "ID":
            i = 1

        if self.lookahead[i] == terminal:
            node_name = self.lookahead[1] +", "+ self.lookahead[2]
            if not self.is_end:
                node1 = Node(f"({node_name}) ", parent=parent)
            self.lookahead = scanner.get_token()
        else:
            if not self.is_end:
                errors.write("#%s : syntax error, missing %s \n" % (self.lookahead[0], terminal))
                self.noError = False