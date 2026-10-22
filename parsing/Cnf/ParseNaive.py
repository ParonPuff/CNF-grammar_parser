from parsing.Cnf.ContextFreeParser import ContextFreeParser
class ParseNaive(ContextFreeParser):

    def parse(self,in_string):
        self.reset_counter()
        self.__in_string = in_string
        return self.__naiveRecurse(0, 0, len(in_string)-1)

    def __naiveRecurse(self,nonterminal, start_idx, end_idx):
        self.counter += 1

        if start_idx == end_idx:
            generating_nonterminals = self.grammar.get_nonterminals_for_rhs(str(self.__in_string[start_idx])) or []
            if nonterminal in generating_nonterminals:
                return True
            else:
                return False

        for (A, B) in self.grammar.get_nonterminal_rules(nonterminal):
            for split_idx in range(start_idx,end_idx):
                if self.__naiveRecurse(A,start_idx,split_idx) and self.__naiveRecurse(B,split_idx+1,end_idx):
                    return True

        return False
