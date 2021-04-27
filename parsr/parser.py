from anytree import Node, RenderTree


class Parser:
    def __init__(self, scanner, parse_table):
        self.scanner = scanner
        self.parse_table = parse_table
        self.current_token = ""
        self.current_token_details = ""
        self.stack = [['♤', 'Terminal'], ['S', 'Non-Terminal']]
        self.nodes = []
        self.tree_str = ""

    def parsing(self):
        self.get_new_token()
        node1 = -1
        while len(self.stack) > 0:
            A = self.stack.pop()
            node_ = self.find_node(A[0])
            if node_ == -1:
                node_ = Node(A[0])
            if node1 == -1:
                node1 = node_
            print(A, '     ', self.current_token)
            if A[1] == "Terminal":
                if A[0] == self.current_token:
                    self.get_new_token()
                elif A[0] == 'ε':
                    pass
                else:
                    print("error", self.current_token_details)
            elif self.parse_table[A[0]][self.current_token][0][0] == 'empty':
                self.get_new_token()
                self.stack.append(A)
                print("empty", self.current_token_details)
            elif self.parse_table[A[0]][self.current_token][0][0] == 'sync':
                print("sync", self.current_token_details)
            else:
                if node_ in self.nodes:
                    self.nodes.remove(node_)
                self.add_to_stack(self.parse_table[A[0]][self.current_token], node_)
        self.tree_str_maker(node1)

    def tree_str_maker(self, node1):
        file_ = open("report/parser/parse_tree.txt", "w+", encoding='utf-8')
        result = ""
        for pre, fill, node in RenderTree(node1):
            if node.name == 'ε':
                result += f"{pre}epsilon\n"
            else:
                result += f"{pre}{node.name}\n"
        file_.write(result)
        file_.close()

    def get_new_token(self):
        self.current_token_details = self.scanner.get_token()
        self.current_token = self.current_token_details[2]

    def add_to_stack(self, list1, node2):
        for element in list1:
            x = Node(element[0], parent=node2)
            self.nodes.append(x)
        for i in range(len(list1) - 1, -1, -1):
            self.stack.append(list1[i])

    def find_node(self, name2):
        for element2 in self.nodes:
            if element2.name == name2:
                return element2
        return -1
