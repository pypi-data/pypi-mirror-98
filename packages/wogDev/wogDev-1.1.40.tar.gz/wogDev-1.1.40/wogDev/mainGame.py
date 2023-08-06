import utils
from .utils import get_user_name, welcome, load_game, number_to_game
from .Factory import Factory


def main():
    user_name = get_user_name()
    welcome(user_name)
    game, level = load_game()
    obj_game = Factory.create_game(number_to_game[game], user_name, level, game)
    obj_game.print_data()
    obj_game.play


if __name__ == '__main__':
    main()
