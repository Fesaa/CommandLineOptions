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
        self.rules = []
    
    def __str__(self) -> str:
        if self.options:
            return "\n".join([str(option) for option in self.options.values() if option.argument != option.default_argument])
        else:
            return ""
    
    def add_option(self, option: CommandLineOption) -> None:
        if self.options:
            self.options[option.name] = option
        else:
            self.options = {option.name: option}
        
        return option
    
    def add_dependency(self, option1: CommandLineOption, option2: CommandLineOption):
        self.rules.append([option1, option2])
    
    def on_start(self) -> Dict[str, CommandLineOption]:

        all_options = sys.argv[1::]

        if '--options' in all_options:
            all_options.pop(all_options.index('--options'))
            print("\n".join(option for option in self.options.values()))
            if len(all_options) == 0:
                return sys.exit()

        for option in all_options:
            if split := re.match(r'\w*(=|:)\w*', option):
                option_args = option.split(split.group(1))
                option = option_args[0]
                argument = option_args[1]

                if option in self.options.keys():

                    command_line_option = self.options[option]
                    
                    if re.match(self.options[option].regex, argument):

                        if command_line_option.return_type is str:
                            argument = argument

                        elif command_line_option.return_type is int:
                            if argument.isdigit():
                                argument = int(argument)
                            else:
                                raise InvalidArgumentType(command_line_option)

                        elif command_line_option.return_type is float:
                            try:
                                argument = float(argument)
                            except ValueError:
                                raise InvalidArgumentType(command_line_option)

                        elif command_line_option.return_type is bool:
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
                                try:
                                    temp.append(float(arg))
                                except ValueError:
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

        for rule in self.rules:
            if rule[0] in missing_required_options and rule[1] in missing_required_options:
                 MissingRequiredOption(missing_required_options)
            else:
                missing_required_options.pop(missing_required_options.index(rule[1] if rule[1] in missing_required_options else rule[0]))

        if missing_required_options == []:

            if self.show_info:
                print(str(self))

            return {option_name: option.argument for option_name, option in self.options.items()}
        else:
            raise MissingRequiredOption(missing_required_options)