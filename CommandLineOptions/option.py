from typing import Any, TypedDict, Union, List
from colorama import Fore, Style

from .enums import RegexOptions

TYPE_TO_STR = {
    str: 'str',
    float: 'float',
    int: 'int',
    bool: 'bool',
    List[str]: 'List[str]',
    List[float]: 'List[float]',
    List[int]: 'List[int]',
    List[bool]: 'List[bool]'

}

class InvalidReturnType(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return 'Return type must be one of the following: [str, float, int, bool, list[str | float | int | bool]'

class OptionDict(TypedDict):
    regex: str
    default_argument: Any
    required: bool
    return_type: Union[str, float, int, bool]

class CommandLineOption:

    def __init__(self, name: str, regex: Union[str, RegexOptions] = r'.*', default_argument: Any = None,
                return_type: Union[str, float, int, bool, List[Union[str, float, int, bool]]] = str,  info: str = None) -> None:
        self.name = name
        self.regex = str(regex)
        self.default_argument = default_argument
        self.required = True if self.default_argument is None else False

        try:
            TYPE_TO_STR[return_type]
        except KeyError:
            raise InvalidReturnType
        else:
            self.return_type = return_type
        self.info = info
        self.argument = self.default_argument

    
    def __iter__(self) -> OptionDict:
        yield from {self.name: {'regex': self.regex, 'default_argument': self.default_argument,
                                'return_type': self.return_type, 'required': self.required}}.items()
    
    def __str__(self) -> str:
        return f'\n{self.info}'\
               f'\n\tMust match: {Fore.BLUE}{self.regex}{Style.RESET_ALL}'\
               f'\n\tDefault: {Fore.YELLOW}{self.default_argument}{Style.RESET_ALL}'\
               f'\n\tReturns a {Fore.MAGENTA}{TYPE_TO_STR[self.return_type]}{Style.RESET_ALL}' \
               f'\n\tRequired: {Fore.GREEN if self.required else Fore.RED}{self.required}{Style.RESET_ALL}'