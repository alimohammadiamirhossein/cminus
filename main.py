from scanner.scanner import Scanenr
from parsr.grammar import Grammar
from parsr.initialize import Initializer
from parsr.parser import Parser

################### parser output is in report/parser #################################################
# amirmahdi hosseinabadi 97110069
# amirhossein alimohammadi 97110166

initialize = Initializer()
g = Grammar('parsr/', initialize)
parse_table = g.get_parse_table()

scannar1 = Scanenr("input.txt")
Parser(scannar1,parse_table,initialize)
