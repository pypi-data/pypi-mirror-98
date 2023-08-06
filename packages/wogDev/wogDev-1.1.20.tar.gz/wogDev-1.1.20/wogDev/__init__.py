

from .utils import get_user_name, welcome, load_game, number_to_game ,is_digit
from .Factory import Factory
from .wog_abs import WoG
from .MemoryGame import MemoryGame
from .GuessGame import GuessGame
from .CurrencyRGame import CurrencyRGame

#__all__ = ['get_user_name', 'Factory', 'GuessGame', 'mainGame',
#           'MemoryGame', 'utils', 'wog_abs']

#from .__main__ import main
#import mainGame
#from setuptools import setup, find_packages

#setup(
#    name='wog_pkg',
#      version='0.2.0',
#      description='World of Games'N,
#      long_description=(HERE / "README.txt").read_text(),
#      #long_description_content_type=LONG_DESC_TYPE,
#      author='Oren Jacobovitz',
#      license='Apache License 2.0',
#      author_email='oj.gmbox@gmail.com',
#      #url=URL,
#      #install_requires=INSTALL_REQUIRES,
#      packages=find_packages()
#)