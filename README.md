# C-mnius Compiler

**a Python3 based one-pass compiler for a very simplified C**

## Token Types and Grammar

The tokens in the below table can be recognized by the compiler:
**Token Type** | **Description**
:-------------:|:--------------:
NUM | Any string matching [0-9]+
ID | Any string matching: [A-Za-z][A-Za-z0-9]*
KEYWORD | if, else, void, int, while, break, switch, default, case, return
SYMBOL | ; : , [ ] ( ) { } + - * = < ==
COMMENT | Any string between a /* and a */ OR any string after a // and before a \n or EOF
WHITESPACE | blank (ASCII 32), \n (ASCII 10), \r (ASCII 13), \t (ASCII 9), \v (ASCII 11), \f (ASCII 12)

The grammar that this compiler uses is in [grammar.txt](https://github.com/alimohammadiamirhossein/cminus/blob/main/parsr/grammar.txt).

## First Phase : Scanner
Scanner is the part of the compiler that reads the input file character by character and recognizes tokens.
In this project, the preassumption is that a file called "input.txt" contains the code and is in the same directory as [compiler.py](https://github.com/alimohammadiamirhossein/cminus/blob/main/main.py). 

For additional information and how to use please refer to [here](https://github.com/alimohammadiamirhossein/cminus/edit/main/README.md).

## Second Phase : Parser
Parser is the part of the compiler that recognizes the grammar used by the input.

This project implements a LL1 parser. Additional information and how to use can be viewed in [README of Parser](https://github.com/alimohammadiamirhossein/cminus/edit/main/README.md).
