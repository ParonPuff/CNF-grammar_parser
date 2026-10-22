from parsing.Linear.LinearParser import LinearParser

class LinearParseTD(LinearParser):
    """
    Top-down parser for linear grammars.
    This class extends the LinearParser class and implements a top-down parsing algorithm.
    """

    def parse(self, in_string):
        self.reset_counter()
        self.__in_string = in_string
        n = len(in_string)
        self.__memo = [[[None] * (n+1) for _ in range(n+1)] for _ in range(self.grammar.count_nonterminals())]
        return self.__recurse(0, 0, len(in_string))

    def __recurse(self,A: int, i: int, j: int) -> bool:
            # Check memo
            if self.__memo[A][i][j] is not None:
                return self.__memo[A][i][j]
            # Base case: single terminal span
            if j == i+1:
                for t in self.grammar.get_terminal_rule(A):
                    if self.__in_string[i] == t:
                        self.counter += 1
                        self.__memo[A][i][j] = True
                        return True
                self.__memo[A][i][j] = False
                return False
            # Recursive case: linear productions
            for prod in self.grammar.get_nonterminal_rules(A):
                X, Y = prod
                # prefix: A -> X B
                if isinstance(X, str) and isinstance(Y, int):
                    if self.__in_string[i] == X and self.__recurse(Y, i+1, j):
                        self.counter += 1
                        self.__memo[A][i][j] = True
                        return True
                # suffix: A -> B Y
                elif isinstance(X, int) and isinstance(Y, str):
                    if self.__in_string[j-1] == Y and self.__recurse(X, i, j-1):
                        self.counter += 1
                        self.__memo[A][i][j] = True
                        return True
            # No production matched
            self.__memo[A][i][j] = False
            return False