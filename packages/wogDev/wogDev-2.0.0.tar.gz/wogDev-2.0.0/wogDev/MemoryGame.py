from .wog_abs import WoG
from .utils import number_to_game, is_digit
import random
import time
import os
import collections


class MemoryGame(WoG):

    def __init__(self, user_name, difficulty, game):
        self.name = user_name
        self.level = difficulty
        self.game = game
        return

    random_list = []
    list_from_user = []

    def print_data(self):
        print(f'MemoryGame: {self.name} choose to play "{number_to_game[self.game]}" '
              f'with difficulty level of {self.level}.')

    @property
    def short_explanation_before_the_game(self):
        print(f'Starting to play Memory Game.... ')
        print(f'The purpose of memory game is to remember the random numbers that shown and then write them back. ')
        print(f' ****************************************************')
        print(f' * Important: Type only numbers separated by space. *')
        print(f' ****************************************************')
        print(f'\n')

    @property
    def generate_sequence(self):
        self.random_list = random.sample(range(1, 101), self.level)
        # print(type(self.random_list), type(self.random_list[0]))

    def get_data_from_user(self):
        data_list = input('Enter numbers separated by space ')
        data_list = data_list.split()
        # check number of elements
        if len(data_list) != self.level:
            print(f'Your list of numbers contain {len(data_list)} element, it should contain {self.level} element!!')
            print(f'Game Over for you :( .')
            return False
        # print list
        # print('list: ', data_list)
        # print(type(data_list), type(data_list[0]))
        # convert each item to int type and check if digit
        for i in range(len(data_list)):
            # convert each item to int type
            if not is_digit(data_list[i]):
                print(f'Your item number {i + 1} is not valid number: "{data_list[i]}"!! Need to type only numbers .')
                print(f'Game Over for you :( .')
                return False
            data_list[i] = int(data_list[i])
        self.list_from_user = data_list
        # print('list2: ', self.list_from_user)
        # print(type(self.list_from_user), type(self.list_from_user[0]))
        return True

    @property
    def compare_data(self):
        if collections.Counter(self.random_list) == collections.Counter(self.list_from_user):
            return True
        else:
            return False

    @property
    def play(self):
        self.short_explanation_before_the_game
        self.generate_sequence
        n = input('press any key when you will ready to start.\nTo quit press "q". ')
        if n == 'q':
            print(f'You choose to quit game ... ')
            return False
        print(f'Look and remember : {self.random_list}')
        # wait 0.7 second
        time.sleep(0.7)
        os.system('cls')
        if not self.get_data_from_user():
            return False
        if self.compare_data:
            print(f'Good job, you managed to remember all the numbers :)')
            return True
        else:
            print(f'Too bad, you could not remember all the numbers. {self.name}, you need to keep practicing :(')
            return False
