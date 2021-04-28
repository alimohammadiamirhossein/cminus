file = open("firstdata.txt", "r")
first = open("first.txt", "w")
terminals = ['ID', ';', '[', 'NUM', ']', '(', ')', 'int', 'void', ',','{', '}', 'break', 'if', 'else', 'while', 'return',
             'for', '=', '<', '==', '+', '-', '*', 'epsilon']
# print(len(terminals))
for i in range(51):
    line = file.readline()
    array = line.split()
    first.write(array[0] + " -> ")
    # print(len(array))
    for j in range(1, len(array)):
        if array[j] == "+":
            print(j , array[0])
            first.write(terminals[j-1]+" ")
    first.write("\n")

first.close()
file.close()