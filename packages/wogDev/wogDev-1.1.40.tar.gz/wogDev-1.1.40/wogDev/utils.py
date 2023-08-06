number_to_game = {1: "Memory Game", 2: "Guess Game", 3: "Currency Roulette"}


def welcome(name):
    print(f"Hello {name},\n"
          f"_________________\n"
          f"and welcome to the World of Games (WoG).\nHere you can find many cool games to play.\n\n")


def load_game():
    headline_1 = 'World of Games:\n' \
                 '---------------\n' \
                 '1. Memory Game      - a sequence of numbers will appear for 1 second and you have to guess it back.\n' \
                 '2. Guess Game       - guess a number and see if you chose like the computer.\n' \
                 '3. Currency Roulette- try and guess the value of a random amount of USD in ILS.\n' \
                 'Please choose a game to play:'
    re_headline_1 = "Please choose a game to play:"
    game_to_play = input_number(headline_1, re_headline_1, 1, 3)

    headline_2 = "Please choose game difficulty from 1 to 5:"
    re_headline_2 = "Please choose the level to play:"
    level = input_number(headline_2, re_headline_2, 1, 5)
    return game_to_play, level


def is_digit(check_input):
    if check_input.isdigit():
        return True
    return False


def get_user_name():
    nickname = input("Before we start to play, Please enter your nickname: ")
    return nickname


def input_number(headline, re_headline, start_range, end_range, message=""):
    check_data = True
    once = True
    while check_data:
        if once:
            data_input = input(headline)
            once = False
        else:
            data_input = input(re_headline)
        while not is_digit(data_input):
            print(f'Not valid data!! Need to choose between {start_range} to {end_range}.')
            data_input = input(re_headline)
        acceptable_values = list(range(start_range, end_range + 1))
        data_input = int(data_input)
        if data_input not in acceptable_values:
            print(f'You choose "{data_input}" but its not in range!!')
            print(f'Need to choose between {start_range} to {end_range}.')
            continue
        else:
            check_data = False
            return data_input


def input_number_old(headline, re_headline, start_range, end_range, message=""):
    once = 1
    while True:
        try:
            if once:
                data_input = int(input(headline))
                once = 0
            else:
                data_input = int(input(re_headline))
            acceptable_values = list(range(start_range, end_range + 1))
            if data_input not in acceptable_values:
                # repeat input
                print(f"The {data_input} you choose not in range!!")
                print(f"Please choose {message} between {start_range} to {end_range}..")
                continue
        except ValueError:
            print(f"Not valid number !!")
            print(f"Please choose {message} from {start_range} to {end_range}:")
            once = 0
            continue
        return data_input
