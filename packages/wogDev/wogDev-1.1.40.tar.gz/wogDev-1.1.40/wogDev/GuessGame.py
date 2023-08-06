from .wog_abs import WoG
from .utils import number_to_game, is_digit
import random


class GuessGame(WoG):

    def __init__(self, user_name, difficulty, game):
        self.name = user_name
        self.level = difficulty
        self.game = game
        return

    secret_number = 0
    data_num_from_user = 0

    def print_data(self):
        print(f'GuessGame: {self.name} choose to play "{number_to_game[self.game]}" '
              f'with difficulty level of {self.level}.')

    @property
    def short_explanation_before_the_game(self):
        print(f'Starting to play Guess Game.... ')
        print(f'The purpose is to guess the number the computer chose. ')
        print(f' ******************************************************')
        print(f' * Important: chose only numbers in range "1" to "{self.level}". *')
        print(f' ******************************************************')
        print(f'\n')

    @property
    def generate_number(self):
        self.secret_number = random.randint(1, self.level)
        # print(f'secret_number = {self.secret_number}')

    def get_guess_from_user(self):
        data_num = input(f'Guess number between 1 to {self.level}: ')
        if not is_digit(data_num):
            print(f'You typed not valid number: "{data_num}"!! Need to type only number.')
            print(f'Game Over for you :( ')
            return False
        # print('data_num: ', data_num)
        # print(type(data_num))
        self.data_num_from_user = int(data_num)
        if self.data_num_from_user not in range(1,self.level):
            print(f'You typed number not in range "1" to "{self.level}"!! Need to type only number in that range.')
            print(f'Game Over for you :( ')
            return False
        return True

    @property
    def compare_data(self):
        # print(f'compare: {self.secret_number}, {self.data_num_from_user}')
        if self.data_num_from_user == self.secret_number:
            return True
        else:
            return False

    @property
    def play(self):
        self.short_explanation_before_the_game
        self.generate_number
        n = input('press any key when you will ready to start.\nTo quit press "q". ')
        if n == 'q':
            print(f'You choose to quit game ... ')
            return False
        if not self.get_guess_from_user():
            return False
        if self.compare_data:
            print(f'Good job {self.name}, you managed to guess the number :)')
            return True
        else:
            print(f'{self.name}, you did not manage to guess the number. The secret number was {self.secret_number}')
            return False

