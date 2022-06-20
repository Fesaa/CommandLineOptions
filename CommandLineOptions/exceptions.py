from typing import Iterable, List
from colorama import Fore, Style

from .option import CommandLineOption
from .enums import SplitOption

class MissingRequiredOption(Exception):

    def __init__(self, options: List[CommandLineOption], *args: object) -> None:
        super().__init__(*args)
        self.options = options

    def __str__(self) -> str:
        s = "\n".join([str(option) for option in self.options])
        return f'Missing CommandLineOption:{s}.'

class InvalidLayout(Exception):

    def __init__(self, split_option: SplitOption, *args):
        super().__init__(args)
        self.split_option = split_option

    def __str__(self):
        return f'CommandLineOptions must be given in the form {Fore.CYAN}{self.split_option}{Style.RESET_ALL}.'

class InvalidOption(Exception):

    def __init__(self, given_option: str ,options: Iterable[CommandLineOption], *args: object) -> None:
        super().__init__(*args)
        self.options = options
        self.given_option = given_option
    
    def __str__(self) -> str:
        s = "\n".join([str(option.name) for option in self.options])
        return f'{self.given_option} is not a valid CommandLineOption.\nThe accepted options are:\n {s}.'

class InvalidArgument(Exception):
    
    def __init__(self, given_argument: str, option: CommandLineOption, *args: object) -> None:
        super().__init__(*args)
        self.option = option
        self.given_argument = given_argument
    
    def __str__(self) -> str:
        return f'{self.given_argument} did not match {self.option.name}\'s regex string: {self.option.regex}.'

class InvalidArgumentType(Exception):

    def __init__(self, option: CommandLineOption,*args: object) -> None:
        super().__init__(*args)
        self.option = option

    def __str__(self) -> str:
        return f'Type and Regex string to not match. Please check your initiation for {self.option.name}'\
               f'\nRegex: {self.option.regex}\nType: {self.option.return_type}'
