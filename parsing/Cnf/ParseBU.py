from parsing.Cnf.ContextFreeParser import ContextFreeParser
class ParseBU(ContextFreeParser):
    def parse(self, input_str: str) -> bool:
        """
        Parse `input_str` using the CYK algorithm.
        Returns True if the start symbol (index 0) derives the entire string.
        """
        n = len(input_str)
        V = self.grammar.count_nonterminals()
        self.reset_counter()

        # table[A][i][j] == True if nonterminal A derives input_str[i..j], inclusive
        table = [[[False] * n for _ in range(n)] for _ in range(V)]

        # 1) Base case: length-1 substrings (i == j)
        for i, ch in enumerate(input_str):
            generators = self.grammar.get_nonterminals_for_rhs(ch) or []
            for A in generators:
                table[A][i][i] = True
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
                            if table[B][start][split] and table[C][split + 1][end]:
                                table[A][start][end] = True
                                self.counter += 1  # one binary rule application
                                # Once A derives this span, move to next A
                                break
                        if table[A][start][end]:
                            break

        # 3) Acceptance: start symbol (index 0) covers full span
        return table[0][0][n - 1]