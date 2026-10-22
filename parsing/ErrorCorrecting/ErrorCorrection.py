from abc import ABC, abstractmethod
class ErrorCorrection(ABC):
    def __init__(self):
        self._possible_to_correct = False
        self._amount_of_deletions = 0
        self._amount_of_substitutions = 0
        self._corrected_string = None

    @abstractmethod
    def get_corrected_string(self):
        pass

    @abstractmethod
    def get_amount_of_deletions(self):
        pass

    @abstractmethod
    def get_amount_of_substitutions(self):
        pass