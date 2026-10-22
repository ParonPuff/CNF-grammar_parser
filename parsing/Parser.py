from Grammar import Grammar
from abc import ABC, abstractmethod
"""
A datatype Parser which is provided with a grammar to be parsed as an argument, and which pro-
vides parsing methods such as parseNaive, parseBU, and parseTD. The methods should take the
string to be parsed as an argument, and should of course return a truth value indicating whether
the input string was found to belong to the language or not. In addition, the parser should contain
a counter which is initialized to zero when parsing starts. The iterative parser (i.e., the standard
bottom-up CYK parser) increments the counter with each execution of the innermost loop. Simi-
larly, the recursive variants increment the counter each time a recursive call is made. In this way,
the counter gives an estimate of the number of operations that have been executed when parsing has
finished. This yields an abstract measure of how much work the algorithm has performed and can
later on be compared to the physical time measurements in order to see whether the two types of
measurements support the same conclusions
"""

class Parser(ABC):
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.counter = 0
        pass
    def reset_counter(self):
        self.counter = 0
    @abstractmethod
    def parse(self,in_string):
        pass
