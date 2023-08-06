from abc import ABC, abstractmethod


class WoG(ABC):

    # abstract methods:
    @abstractmethod
    def print_data(self):
        pass

    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def compare_data(self):
        pass
