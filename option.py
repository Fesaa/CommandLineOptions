from typing import Any, TypedDict, Union, List
from colorama import Fore, Style

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
    default_option: Any
    required: bool
    return_type: Union[str, float, int, bool]

class CommandLineOption:

    def __init__(self, name: str, regex: str = r'.*', default_option: Any = None,
                return_type: Union[str, float, int, bool, List[Union[str, float, int, bool]]] = str,  info: str = None) -> None:
        self.name = name.lower()
        self.regex = regex
        self.default_option = default_option
        self.required = True if self.default_option is None else False

        try:
            TYPE_TO_STR[return_type]
        except KeyError:
            raise InvalidReturnType
        else:
            self.return_type = return_type
        self.info = info
        self.argument = self.default_option
    
    def __iter__(self) -> OptionDict:
        yield from {self.name: {'regex': self.regex, 'default_option': self.default_option,
                                'return_type': self.return_type, 'required': self.required}}.items()
    
    def __str__(self) -> str:
        return f'\n{self.info}'\
               f'\n\tMust match: {Fore.BLUE}{self.regex}{Style.RESET_ALL}'\
               f'\n\tDefault: {Fore.YELLOW}{self.default_option}{Style.RESET_ALL}'\
               f'\n\tReturns a {Fore.MAGENTA}{TYPE_TO_STR[self.return_type]}{Style.RESET_ALL}' \
               f'\n\tRequired: {Fore.GREEN if self.required else Fore.RED}{self.required}{Style.RESET_ALL}'