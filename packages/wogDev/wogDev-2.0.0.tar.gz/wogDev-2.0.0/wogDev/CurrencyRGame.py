from .wog_abs import WoG
import random
from .utils import number_to_game, is_digit
import currency_converter
from currency_converter import CurrencyConverter


class CurrencyRGame(WoG):

    def __init__(self, user_name, difficulty, game):
        self.name = user_name
        self.level = difficulty
        self.game = game
        return

    usd_number = 0  # between 1-100 for user to guess
    total_value_of_money = 0
    current_currency_rate = 0
    start_interval = 0
    end_interval = 0
    user_guess = 0
    dolarToNis = 0

    def print_data(self):
        print(f'CurrencyRGame: {self.name} choose to play "{number_to_game[self.game]}" '
              f'with difficulty level of {self.level}.')

    @property
    def short_explanation_before_the_game(self):
        print(f'Starting to play Currency Roulette Game.... ')
        print(f'The purpose is to guess how match US$ is in ILS.')
        print(f' *********************************')
        print(f' * Important: type only numbers. *')
        print(f' *********************************')
        print(f'\n')

    @property
    def generated_number(self):
        number = random.randint(1, 100)
        self.usd_number = number

    @property
    def generated_number_from_USD_to_ILS(self):
        c = CurrencyConverter()
        self.dolarToNis = c.convert(1, 'USD', 'ILS')
        self.dolarToNis = float(format(self.dolarToNis, '.2f'))
        self.current_currency_rate = self.usd_number * self.dolarToNis

    @property
    def delta_to_check(self, number_to_check):
        start_range = (self.usd_number - (5 - self.level))
        end_range = (self.usd_number - (5 + self.level))
        if number_to_check not in range(start_range, end_range):
            return False
        else:
            return True

    def get_guess_from_user(self):
        guess = input(f'Enter a guess of ILS value for {self.usd_number}$ :')
        if not is_digit(guess):
            print(f'You typed not valid number: "{guess}"!! Need to type only number.')
            print(f'Game Over for you :( ')
            return False
        self.user_guess = float(guess)
        return True

    @property
    def calc_range(self):
        i_range = 5 - self.level
        # print(f'tmp={tmp}, level={self.level}')
        self.start_interval = ((self.usd_number - i_range) * self.dolarToNis)
        # print(f'self.start_interval: {self.start_interval}, self.end_interval {self.end_interval}')
        self.end_interval = ((self.usd_number + i_range) * self.dolarToNis)
        # print(f'self.start_interval: {self.start_interval}, self.end_interval {self.end_interval}')

    @property
    def compare_data(self):
        # print(f'compare: {type(self.user_guess)}, {self.current_currency_rate}')
        # print(f'self.start_interval: {self.start_interval}, self.end_interval {self.end_interval}')
        # print(f'self.start_interval: {type(self.start_interval)}, self.end_interval {type(self.end_interval)}')
        if self.start_interval <= self.user_guess <= self.end_interval:
            print(f'The number {self.user_guess} is in range ({self.start_interval} - {self.end_interval})')
            return True
        else:
            print(f'The number {self.user_guess} is not in range ({self.start_interval} - {self.end_interval})')
            return False

    @property
    def play(self):
        self.short_explanation_before_the_game
        self.generated_number
        self.generated_number_from_USD_to_ILS
        # print(f'self.dolarToNis={self.dolarToNis}, current_currency_rate={self.current_currency_rate}')
        n = input('press any key when you will ready to start.\nTo quit press "q". ')
        if n == 'q':
            print(f'You choose to quit game ... ')
            return False
        if not self.get_guess_from_user():
            return False
        self.calc_range
        if self.compare_data:
            print(f'Good !! manage to guessed "how match is {self.usd_number}$ in ILS."')
            return True
        else:
            print(f'Not bad, next time you might succeed.\n'
                  f'The correct answer is: {self.usd_number}$ is {self.current_currency_rate}Nis')
            return False
