from scanner.scanner import Scanenr

scanener1 = Scanenr("scanner/input.txt")
while True:
    line, state, token = scanener1.get_token()
    print(line, state, token)
    if token == "♤":
        break
