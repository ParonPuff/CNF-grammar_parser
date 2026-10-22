from parsing.Linear.LinearParser import LinearParser

class LinearParseBU(LinearParser):
    """
    Bottom-up parser for linear grammars.
    This class extends the LinearParser class and implements a bottom-up parsing algorithm.
    """

    def parse(self, w: str) -> bool:
        n = len(w)
        V = self.grammar.count_nonterminals()
        # DP table[A][i][j] == True if nonterminal A => w[i:j] (i inclusive, j exclusive)
        table = [[[False] * (n+1) for _ in range(n+1)] for _ in range(V)]
        self.reset_counter()

        # Step 1: terminal-only rules A -> t
        for A in range(V):
            for t in self.grammar.get_terminal_rule(A):
                # match single character spans
                for i, ch in enumerate(w):
                    if ch == t:
                        table[A][i][i+1] = True
                        self.counter += 1

        # Step 2: length >= 2 spans
        for length in range(2, n+1):
            for i in range(n - length + 1):
                j = i + length
                # for each nonterminal A
                for A in range(V):
                    # check each linear production
                    for prod in self.grammar.get_nonterminal_rules(A):
                        # prod is (terminal, B) or (B, terminal)
                        X, Y = prod
                        if isinstance(X, str) and isinstance(Y, int):
                            # prefix case: A -> X B
                            if w[i] == X and table[Y][i+1][j]:
                                table[A][i][j] = True
                                self.counter += 1
                                break
                        elif isinstance(X, int) and isinstance(Y, str):
                            # suffix case: A -> B Y
                            if w[j-1] == Y and table[X][i][j-1]:
                                table[A][i][j] = True
                                self.counter += 1
                                break
                    # if derived, no need to check other productions
                    if table[A][i][j]:
                        break

        # accept if start symbol covers full string
        start_idx = 0
        return table[start_idx][0][n]
