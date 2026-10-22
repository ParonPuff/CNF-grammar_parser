from parsing.Cnf.ContextFreeParser import ContextFreeParser

class ParseTD(ContextFreeParser):
    def parse(self,in_string):
        self.reset_counter()
        self.__in_string = in_string
        str_len = len(in_string)
        self.__memo = [[[None for _ in range(str_len)] for _ in range(str_len)] for _ in range(self.grammar.count_nonterminals())]
        return self.__naiveRecurse(0, 0, len(in_string)-1)


    def __naiveRecurse(self,nonterminal, start_idx, end_idx):
        self.counter += 1
        if self.__memo[nonterminal][start_idx][end_idx] is not None: #check if already computed
            return self.__memo[nonterminal][start_idx][end_idx]
        if start_idx == end_idx:
            possible_generators = self.grammar.get_nonterminals_for_rhs(self.__in_string[start_idx]) or []
            if nonterminal in possible_generators:
                self.__memo[nonterminal][start_idx][end_idx] = True #cache the result
                return True
            else:
                self.__memo[nonterminal][start_idx][end_idx] = False #cache the result
                return False

        for (A, B) in self.grammar.get_nonterminal_rules(nonterminal):
            for split_idx in range(start_idx,end_idx):
                if self.__naiveRecurse(A,start_idx,split_idx) and self.__naiveRecurse(B,split_idx+1,end_idx):
                    self.__memo[nonterminal][start_idx][end_idx] = True #cache the result
                    return True

        self.__memo[nonterminal][start_idx][end_idx] = False #cache the result
        return False