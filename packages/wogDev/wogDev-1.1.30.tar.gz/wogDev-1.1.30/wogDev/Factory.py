from .MemoryGame import MemoryGame
from .GuessGame import GuessGame
from .CurrencyRGame import CurrencyRGame


class Factory:

    @staticmethod
    def create_game(name_game, user_name, level, game):
        if name_game == "Memory Game":
            return MemoryGame(user_name, level, game)
        elif name_game == "Guess Game":
            return GuessGame(user_name, level, game)
        elif name_game == "Currency Roulette":
            return CurrencyRGame(user_name, level, game)
        else:
            return None
