class Parser:
    def __init__(self, scanner, parse_table):
        self.scanner = scanner
        self.parse_table = parse_table
        self.current_token = ""
        self.current_token_details = ""
        self.stack = [['♤','Terminal'],['S', 'Non-Terminal']]

    def parsing(self):
        self.get_new_token()
        while len(self.stack) > 0:
            A = self.stack.pop()
            print(A,'     ', self.current_token)
            if A[1] == "Terminal":
                if A[0] == self.current_token:
                    self.get_new_token()
                elif A[0] == 'ε':
                    pass
                else:
                    print("err")
            elif self.parse_table[A[0]][self.current_token][0][0] == 'empty':
                self.get_new_token()
                self.stack.append(A)
                print("empty")
            elif self.parse_table[A[0]][self.current_token][0][0] == 'sync':
                print("sync")
            else:
                self.add_to_stack(self.parse_table[A[0]][self.current_token])

    def get_new_token(self):
        self.current_token_details = self.scanner.get_token()
        self.current_token = self.current_token_details[2]

    def add_to_stack(self, list1):
        for i in range(len(list1) - 1, -1, -1):
            self.stack.append(list1[i])
