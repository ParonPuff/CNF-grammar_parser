from abc import ABC, abstractmethod
from collections.abc import Iterable
"""
An abstract datatype Grammar that can be subclassed by specifying the rules of a context-free gram-
mar in Chomsky normal form. The class should allow efficient access to the rules, where efficiency
should be judged relative to the way in which the rules are accessed in the CYK algorithm. In par-
ticular, it is probably a good idea to represent the terminal rules separately from the nonterminal
ones. Moreover, I suggest to translate the nonterminals into integers while initializing the internal
data structures. In this way, one may for example represent a right-hand side as a pair of integers,
and can implement the set of nonterminal rules as an array of arrays of right-hand sides. Then, if a
given nonterminal i has n nonterminal rules, one can efficiently loop over their right-hand sides as
rule[i][j] for j = 0, . . . , n − 1 (and one can loop over all rules by additionally looping over i)
"""


"""
Nonterminals and terminals are individual ASCII symbols.
• All nonterminals are uppercase letters of the latin alphabet, and all remaining ASCII symbols occur-
ring in the rules are terminals.
• The left-hand side of the first rule is the initial nonterminal.

By these conventions, the input file only has to specify the rules. Each rule is written on a separate line,
a nonterminal followed by a blank and the right-hand side of the rule (i.e., either one terminal or two
nonterminals)

"""

class Grammar(ABC):
    """
    Abstract Grammar class for context-free grammars in Chomsky Normal Form (CNF).
    This class provides the structure for managing rules and efficient access to them.
    """
    def __init__(self, in_file):
        with open(in_file, "r") as grammar_file:
            line = grammar_file.readline()
            while line:
                self.add_nonterminal(line[0])
                current_nonterminal = line[0]
                productions = []
                for c in line[1:]:
                    if c != ' ' and c != '\n':
                        productions.append(c)
                self.add_rule(current_nonterminal, productions) 

                line = grammar_file.readline()
            grammar_file.close()

    @abstractmethod
    def count_nonterminals(self) -> int:
        """
        Returns the number of nonterminals in the grammar.
        """
        pass
    @abstractmethod
    def add_nonterminal(self, nonterminal:str) -> int:
        """
        Adds a nonterminal to the grammar and returns its integer representation.
        """
        pass

    @abstractmethod
    def add_rule(self, nonterminal:str, product:list[str]) -> None:
        """
        Adds a rule to the grammar.
        """
        pass

    @abstractmethod
    def get_nonterminal_rules(self, nonterminal:int) -> Iterable[int]:
        """
        Returns the product of nonterminal rules for a given nonterminal.
        """
        pass

    @abstractmethod
    def get_terminal_rule(self, nonterminal:int) -> list[str]:
        pass

    @abstractmethod
    def get_nonterminals_for_rhs(self, rhs:Iterable[int]|str) -> list[int]|None:
        pass

    @abstractmethod
    def get_all_nonterminals(self) -> list[int]:
        pass
