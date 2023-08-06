import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

VERSION = '1.1.50'
PACKAGE_NAME = 'wogDev'
AUTHOR = 'Oren Jacobovitz'
AUTHOR_EMAIL = 'oj.gmbox@gmail.com'
#URL = 'https://github.com/you/your_package'

LICENSE = 'Apache License 2.0'
DESCRIPTION = 'World of Games'
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'currency_converter'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=README,
      #long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      #packages=["wog_pkg"],
      packages=find_packages(),
      #include_package_data=True
      #entry_points={
       #       "console_scripts": [
       #     "realpython=reader.__main__:main",
       #     ]
       # },
      #url=URL,
      install_requires=INSTALL_REQUIRES
      #packages=find_packages()
)