from Grammar import Grammar
from LinearGrammar import LinearGrammar
class CnfGrammar(Grammar):
    def __init__(self): 
        self.__nonterminal_to_int = {}
        self.__nonterminal_rules = {}
        self.__terminal_rules = {}
        self.__inverse_nonterminal_rules = {}
        self.__inverse_terminal_rules = {}
    @classmethod
    def from_file(cls, file:str):
        obj = cls()
        Grammar.__init__(obj,file)
        return obj

    @classmethod
    def from_linear_grammar(cls,grammar:LinearGrammar):
        # Initialize internal structures
        obj = cls()
        # Invert LinearGrammar's nonterminal mapping: name -> int, and create reverse
        lin_map = grammar._LinearGrammar__nonterminal_to_int
        int_to_lin = {v: k for k, v in lin_map.items()}

        # 1. Add all original nonterminals to CNF grammar
        for nt in int_to_lin.values():
            obj.add_nonterminal(nt)

        # 2. Copy terminal rules (A -> a)
        for lin_idx, nt in int_to_lin.items():
            for term in grammar.get_terminal_rule(lin_idx):
                obj.add_rule(nt, [term])

        # 3. Create CNF-friendly nonterminals for terminals in mixed rules
        term_map = {}
        
        # 4. Convert each linear rule (A -> aB or A -> Ba)
        for lin_idx, nt in int_to_lin.items():
            for prod in grammar.get_nonterminal_rules(lin_idx):
                left, right = prod
                # If left is terminal
                if isinstance(left, str):
                    term, nt2_idx = left, right
                    # Introduce T_term -> term if not exists
                    if term not in term_map:
                        t_nt = f"T_{term}"
                        term_map[term] = t_nt
                        obj.add_nonterminal(t_nt)
                        obj.add_rule(t_nt, [term])
                    else:
                        t_nt = term_map[term]
                    # A -> T_term B
                    obj.add_rule(nt, [t_nt, int_to_lin[nt2_idx]])
                else:
                    # right must be terminal
                    nt1_idx, term = left, right
                    if term not in term_map:
                        t_nt = f"T_{term}"
                        term_map[term] = t_nt
                        obj.add_nonterminal(t_nt)
                        obj.add_rule(t_nt, [term])
                    else:
                        t_nt = term_map[term]
                    # A -> B T_term
                    obj.add_rule(nt, [int_to_lin[nt1_idx], t_nt])
        #print(f"Cnf grammar: \n\t{obj}")
        return obj
    def __str__(self) -> str:
        result = ""
        for nonterminal, num in self.__nonterminal_to_int.items():
            result += f"{nonterminal} -> "
            if len(self.__terminal_rules[num]) > 0:
                result += " | ".join(self.__terminal_rules[num])
            if len(self.__nonterminal_rules[num]) > 0:
                result += " | ".join([f"{chr(prod[0]+65)} {chr(prod[1])}" for prod in self.__nonterminal_rules[num]])
            result += "\n"
        return result

    def count_nonterminals(self) -> int:
        return len(self.__nonterminal_to_int)

    def __is_terminal(self,symbol:str) -> bool:
        return symbol.isalpha() and symbol.islower()

    def add_nonterminal(self, nonterminal:str) -> int:

        if self.__is_terminal(nonterminal):
            raise ValueError(f"symbol {nonterminal} is a terminal, not a nonterminal")
        if nonterminal not in self.__nonterminal_to_int:
            num = len(self.__nonterminal_to_int)

            self.__nonterminal_to_int[nonterminal] = num

            self.__nonterminal_rules[num] = []
            self.__terminal_rules[num] = []
        return self.__nonterminal_to_int[nonterminal]

    def add_rule(self, nonterminal:str, product:list[str]) -> None:

        num_nonterminal = self.__nonterminal_to_int[nonterminal]
        match(len(product)):
            case 1:
                self.__terminal_rules[num_nonterminal].append(product[0])
                if product[0] not in self.__inverse_terminal_rules:
                    self.__inverse_terminal_rules[product[0]] = list[int]()
                self.__inverse_terminal_rules[product[0]].append(num_nonterminal)
            case 2:
                int_product = (self.add_nonterminal(product[0]), self.add_nonterminal(product[1]))
                self.__nonterminal_rules[num_nonterminal].append(int_product)
                if int_product not in self.__inverse_nonterminal_rules:
                    self.__inverse_nonterminal_rules[int_product] = list[int]()
                self.__inverse_nonterminal_rules[int_product].append(num_nonterminal)
            case _:
                raise ValueError("Grammar not in CNF: rule has incorrect number of symbols on the right-hand side")

    def get_nonterminal_rules(self, nonterminal:int) -> list[tuple[int]]:
        return self.__nonterminal_rules[nonterminal]
    
    def get_terminal_rule(self, nonterminal:int) -> list[str]:
        return self.__terminal_rules[nonterminal]

    def get_nonterminals_for_rhs(self, rhs:tuple[int,int]|str) -> list[int]:
        if isinstance(rhs,tuple) and (isinstance(rhs[0],int) and isinstance(rhs[1],int)) and rhs in self.__inverse_nonterminal_rules:
            return self.__inverse_nonterminal_rules[rhs]
        elif isinstance(rhs,str) and rhs in self.__inverse_terminal_rules:
            return self.__inverse_terminal_rules[rhs]
        else:
            return []

    def get_all_nonterminals(self) -> list[int]:
        return range(len(self.__nonterminal_to_int))
