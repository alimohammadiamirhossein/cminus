from scanner.scanner import Scanenr
from parsr.grammar import Grammar
from parsr.initialize import Initializer
from parsr.parser import Parser
from Symbols.symbol_table import SymbolTable
from codegen.codegen import CodeGen

################### parser output is in report/parser #################################################
# amirmahdi hosseinabadi 97110069
# amirhossein alimohammadi 97110166


initialize = Initializer()
g = Grammar('parsr/', initialize)
parse_table = g.get_parse_table()
symbol = SymbolTable()
scannar1 = Scanenr("input.txt", symbol)
codegen = CodeGen(scannar1.fw.symbol_tables)
p = Parser(scannar1, parse_table, initialize, codegen)
codegen.end_code()


def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))

# print(symbol.symbol_table)
# print(symbol.IDs)