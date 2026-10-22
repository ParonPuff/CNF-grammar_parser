from collections.abc import Iterable
from Grammar import Grammar

class LinearGrammar(Grammar):
    """
        class defining linear context-free grammars in Chomsky Normal Form.
    """
    def __init__(self, file):
        self.__nonterminal_to_int = {}
        self.__nonterminal_rules = {}
        self.__terminal_rules = {}
        self.__inverse_nonterminal_rules = {}
        self.__inverse_terminal_rules = {}
        super().__init__(file)

    def count_nonterminals(self) -> int:
        """
        Returns the number of nonterminals in the grammar.
        """
        return len(self.__nonterminal_to_int)

    def __is_terminal(self,symbol:str) -> bool:
        """
        Checks if a symbol is a terminal.
        """
        return symbol.isalpha() and symbol.islower()

    def add_nonterminal(self, nonterminal:str) -> int:
        """
        Adds a nonterminal to the grammar and returns its integer representation.
        """
        if self.__is_terminal(nonterminal):
            raise ValueError(f"symbol {nonterminal} is a terminal, not a nonterminal")

        if nonterminal not in self.__nonterminal_to_int:
            num = len(self.__nonterminal_to_int)

            self.__nonterminal_to_int[nonterminal] = num

            self.__nonterminal_rules[num] = []
            self.__terminal_rules[num] = []
        return self.__nonterminal_to_int[nonterminal]


    def add_rule(self, nonterminal:str, product:list[str]) -> None:
        """
        Adds a rule to the grammar. 
        """
        num_nonterminal = self.__nonterminal_to_int[nonterminal]
        match(len(product)):
            case 1:
                self.__terminal_rules[num_nonterminal].append(product[0])
                if product[0] not in self.__inverse_terminal_rules:
                    self.__inverse_terminal_rules[product[0]] = list[int]()
                self.__inverse_terminal_rules[product[0]].append(num_nonterminal)
            case 2:
                parsed_product = None
                if self.__is_terminal(product[0]) and not self.__is_terminal(product[1]):
                    parsed_product = (product[0], self.add_nonterminal(product[1]))
                elif not self.__is_terminal(product[0]) and self.__is_terminal(product[1]):
                    parsed_product = (self.add_nonterminal(product[0]), product[1])
                else:
                    raise ValueError("Grammar is not linear: rule has two nonterminals")
                self.__nonterminal_rules[num_nonterminal].append(parsed_product)
                if parsed_product not in self.__inverse_nonterminal_rules:
                    self.__inverse_nonterminal_rules[parsed_product] = list[int]()
                self.__inverse_nonterminal_rules[parsed_product].append(num_nonterminal)
            case _:
                raise ValueError(f"Grammar is not linear: rule {nonterminal} -> {product}has more than two symbols on the right-hand side")

    def get_nonterminal_rules(self, nonterminal:int) -> tuple[int,str]|tuple[str,int]:
        """
        Returns the product of nonterminal rules for a given nonterminal.
        """
        return self.__nonterminal_rules[nonterminal]

    def get_terminal_rule(self, nonterminal:int) -> list[str]:
        return self.__terminal_rules[nonterminal]

    def get_nonterminals_for_rhs(self, rhs:Iterable[int]|str) -> list[int]:
        if isinstance(rhs,tuple) and (isinstance(rhs[0],int) and isinstance(rhs[1],int)) and rhs in self.__inverse_nonterminal_rules:
            return self.__inverse_nonterminal_rules[rhs]
        elif isinstance(rhs,str) and rhs in self.__inverse_terminal_rules:
            return self.__inverse_terminal_rules[rhs]
        else:
            return []

    def get_all_nonterminals(self) -> list[int]:
        return range(len(self.__nonterminal_to_int))

    def nonterminal_to_int(self, nonterminal:str) -> int:
        return self.__nonterminal_to_int[nonterminal] if nonterminal in self.__nonterminal_to_int else None