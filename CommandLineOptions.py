import sys, re
from typing import List, Dict

from .exceptions import InvalidArgument, InvalidLayout, InvalidOption, InvalidArgumentType, MissingRequiredOption
from .option import CommandLineOption

class CommandLineOptions:

    def __init__(self, options: List[CommandLineOption] = None, show_info: bool= True) -> None:
        if options:
            self.options = {option.name: option for option in options}
        else:
            self.options = None
        
        self.show_info = show_info
    
    def __str__(self) -> str:
        if self.options:
            return "\n".join([str(option) for option in self.options.values()])
        else:
            return ""
    
    def add_option(self, option: CommandLineOption) -> None:
        if self.options:
            self.options[option.name] = option
        else:
            self.options = {option.name: option}
    
    def fetch(self, option_name: str) -> CommandLineOption:
        return self.options[option_name]
    
    def on_start(self) -> Dict[str, CommandLineOption]:

        

        for option in sys.argv[1::]:
            if split := re.match(r'\w*(=|:)\w*', option):
                option_args = option.split(split.group(1))
                option = option_args[0]
                argument = option_args[1]

                if option in self.options.keys():

                    command_line_option = self.options[option]
                    
                    if re.match(self.options[option].regex, argument):

                        if isinstance(command_line_option.return_type, str):
                            argument = argument

                        elif isinstance(command_line_option.return_type, int):
                            if argument.isdigit():
                                argument = int(argument)
                            else:
                                raise InvalidArgumentType(command_line_option)

                        elif isinstance(command_line_option.return_type, float):
                            if argument.isdigit():
                                argument = float(argument)
                            else:
                                raise InvalidArgumentType(command_line_option)

                        elif isinstance(command_line_option.return_type, bool):
                            argument = True if argument == 'True' else False

                        elif command_line_option.return_type is List[str]:
                            argument = argument.split(',')
                        
                        elif command_line_option.return_type is List[int]:
                            temp = list()

                            for arg in argument.split(','):
                                if arg.isdigit():
                                    temp.append(int(arg))
                                else:
                                    raise InvalidArgumentType(command_line_option)
                            
                            argument = temp

                        elif command_line_option.return_type is List[float]:
                            temp = list()

                            for arg in argument.split(','):
                                if arg.isdigit():
                                    temp.append(float(arg))
                                else:
                                    raise InvalidArgumentType(command_line_option)
                            
                            argument = temp

                        elif command_line_option.return_type is List[bool]:
                            temp = list()

                            for arg in argument.split(','):
                                if arg.lower() in ['true', 'false']:
                                    temp.append(True if arg.lower() == 'true' else False)
                                else:
                                    raise InvalidArgumentType(command_line_option)
                        
                            argument = temp
                        

                        self.options[option].argument = argument

                    else:
                        raise InvalidArgument(argument, command_line_option)
                else:
                    raise InvalidOption(option, self.options.values())
            else:
                raise InvalidLayout

        missing_required_options = [j for j in self.options.values() if j.required and j.argument is None]
    
        if missing_required_options == []:

            if self.show_info:
                print(str(self))

            return {option_name: option.argument for option_name, option in self.options.items()}
        else:
            raise MissingRequiredOption(missing_required_options)