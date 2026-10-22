
from parsing import Parser
from abc import ABC
from LinearGrammar import LinearGrammar
class LinearParser(Parser, ABC):
    """
    Abstract base class for context-free parsers.
    This class extends the Parser class and provides a framework for context-free parsing algorithms.
    """

    def __init__(self, grammar: LinearGrammar):
        if not isinstance(grammar, LinearGrammar):
            raise ValueError("grammar is not in Linear Grammar format")
        self.grammar = grammar
        super().__init__(grammar) 