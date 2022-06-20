from enum import Enum

class SplitOption(Enum):
    DEFAULT = "option(=, :)argument"
    DASH = "--option argument"
    #PARENTHESES = "option(argument)"

    def __str__(self) -> str:
        return self.value

class RegexOptions(Enum):
    BOOL = r'\b(False|True)\b'
    DATE = r'^\d{4}[\-\/\s]?((((0[13578])|(1[02]))[\-\/\s]?(([0-2][0-9])|(3[01])))|(((0[469])|(11))[\-\/\s]?(([0-2][0-9])|(30)))|(02[\-\/\s]?[0-2][0-9]))$'
    INT = r'\d*'
    SIMPLE_STR = r'\w*'
    COMPLEX_STR = r'.*'

    def __str__(self) -> str:
        return self.value