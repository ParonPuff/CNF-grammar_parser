from parsing import Parser
from abc import ABC, abstractmethod
from CnfGrammar import CnfGrammar
import config
class ContextFreeParser(Parser, ABC):
    """
    Abstract base class for context-free parsers.
    This class extends the Parser class and provides a framework for context-free parsing algorithms.
    """

    def __init__(self, grammar: CnfGrammar):
        if not isinstance(grammar, CnfGrammar):
            if config.verbose:
                print("grammar is not in CNF, converting to CNF")
            grammar = CnfGrammar.from_linear_grammar(grammar)
        self.grammar = grammar
        super().__init__(grammar) 
