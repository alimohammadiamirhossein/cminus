# follow data

file = open("firstdata.txt", "r" , encoding="utf-8")
first = open("first.txt", "w" , encoding="utf-8")
terminals = ['ID', ';', '[', 'NUM', ']', '(', ')', 'int', 'void', ',','{', '}', 'break', 'if', 'else', 'while', 'return',
             'for', '=', '<', '==', '+', '-', '*', 'ε']


for i in range(51):
    line = file.readline()
    array = line.split()
    first.write(array[0] + " → ")
    # print(len(array))
    for j in range(1, len(array)):
        if array[j] == "+":

            first.write(terminals[j-1]+" ")
    first.write("\n")

first.close()
file.close()

# follow data
file = open("followdata", "r" , encoding="utf-8")
follow = open("follow.txt", "w" , encoding="utf-8")
terminals = ['ID', ';', '[', 'NUM', ']', '(', ')', 'int', 'void', ',','{', '}', 'break', 'if', 'else', 'while', 'return',
             'for', '=', '<', '==', '+', '-', '*', '$']
for i in range(51):
    line = file.readline()
    array = line.split()
    follow.write(array[0] + " → ")
    # print(len(array))
    for j in range(1, len(array)):
        if array[j] == "+":
            follow.write(terminals[j-1]+" ")
    follow.write("\n")

follow.close()
file.close()
