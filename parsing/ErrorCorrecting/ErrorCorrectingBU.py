
from parsing.Cnf.ContextFreeParser import ContextFreeParser
from parsing.ErrorCorrecting.ErrorCorrection import ErrorCorrection
import numpy as np
class ErrorCorrectingParseBU(ContextFreeParser,ErrorCorrection):
    def __init__(self, grammar):
        """
        Initialize the CYK parser with a given grammar.
        """
        self.table = None
        ContextFreeParser.__init__(self,grammar)
        ErrorCorrection.__init__(self)# reset the error correction attributes

    def parse(self, input_str: str) -> int:
        """
        Parse `input_str` using the CYK algorithm.
        Returns True if the start symbol (index 0) derives the entire string.
        """
        ErrorCorrection.__init__(self)# reset the error correction attributes
        n = len(input_str)
        V = self.grammar.count_nonterminals()
        self.reset_counter()
        # table[A][i][j] == True if nonterminal A derives input_str[i..j], inclusive
        self.table = [[[np.inf] * n for _ in range(n)] for _ in range(V)]

        for A in range(V):
            if len(self.grammar.get_terminal_rule(A)) > 0:
                for i in range(n):
                    self.table[A][i][i] = 1 # cost of changing a single character to A

        # 1) Base case: length-1 substrings (i == j)
        for i, ch in enumerate(input_str):
            generators = self.grammar.get_nonterminals_for_rhs(ch)or []
            for A in generators:
                self.table[A][i][i] = 0
                self.counter += 1  # one terminal rule application

        # 2) Build up for spans of length 2..n
        for span in range(2, n + 1):
            for start in range(n - span + 1):
                end = start + span - 1

                # Try each nonterminal A
                for A in range(V):
                    # Check each binary rule A -> B C
                    for B, C in self.grammar.get_nonterminal_rules(A):
                        # Try all split points between start and end
                        for split in range(start, end):
                            if self.table[B][start][split] != np.inf and self.table[C][split + 1][end] != np.inf:
                                self.table[A][start][end] = min(self.table[A][start][end], self.table[B][start][split] + self.table[C][split + 1][end])
                                self.counter += 1  # one binary rule application
                        if self.table[A][start][end] == 0:
                            #print("table[A][start][end]: ", table[A][start][end])
                            break

        self._possible_to_correct = np.min(self.table[0]) != np.inf
        return self._possible_to_correct

    ## Error correction methods

    def get_corrected_string(self):
        """
        Return the corrected string.
        """
        if not self._possible_to_correct:
            return None
        if self._corrected_string is None:
            self._corrected_string = self.__produce_corrected()
        return self._corrected_string

    def get_amount_of_deletions(self):
        """
        Return the amount of deletions.
        """
        if not self._possible_to_correct:
            return None
        if self._corrected_string is None:
            self.get_corrected_string()
        return self._amount_of_deletions

    def get_amount_of_substitutions(self):
        """
        Return the amount of substitutions.
        """
        if not self._possible_to_correct:
            return None
        if self._corrected_string is None:
            self.get_corrected_string()
        return self._amount_of_substitutions

    def __produce_corrected(self):
  
        n = len(self.table[0][0])

        def get_cost(pos):
            i,j = pos
            return self.table[0][i][j] + n-(j - i + 1)

        def reconstruct(A, start, end):
            if start == end:
                return self.grammar.get_terminal_rule(A)
            
            for B, C in self.grammar.get_nonterminal_rules(A):
                for split in range(start, end):
                    if self.table[B][start][split] + self.table[C][split + 1][end] == self.table[A][start][end]:
                        return reconstruct(B, start, split) + reconstruct(C, split + 1, end)
            
            raise ValueError("No valid production found for the given span.")

        # Find the minimum cost substring
        min_pos = (0,n-1)
        for i in range(n):
            for j in reversed(range(i, n)): #priority to longer substrings
                if get_cost(min_pos) > get_cost((i,j)):
                    min_pos = (i,j) 

        i,j = min_pos
        self._amount_of_deletions = n-(j-i+1)
        self._amount_of_substitutions = self.table[0][i][j]
        return "".join(reconstruct(0, i, j))