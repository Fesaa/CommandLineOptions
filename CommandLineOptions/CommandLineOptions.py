import sys, re
from typing import List, Dict

from .exceptions import InvalidArgument, InvalidLayout, InvalidOption, InvalidArgumentType, MissingRequiredOption
from .option import CommandLineOption
from .enums import SplitOption

class CommandLineOptions:

    def __init__(self, options: List[CommandLineOption] = None, show_info: bool= True, split_layout: SplitOption = SplitOption.DEFAULT) -> None:
        if options:
            self.options = {option.name: option for option in options}
        else:
            self.options = None
        
        self.show_info = show_info
        self.split_layout = split_layout
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
    
    def default_dict(self):
        return {option.name: option.default_argument for option in self.options.values()}
    
    def _argument_processor(self) -> list:
        args = sys.argv[1::]

        out = []

        if '--options' in args:
            args.pop(args.index('--options'))
            print("\n".join(str(option) for option in self.options.values()))
            if len(args) == 0:
                return sys.exit()
        
        if self.split_layout.value is SplitOption.DEFAULT:
            for entry in args:
                if split := re.match(r'\w*(=|:)\w*', entry):
                    option_args = entry.split(split.group(1))
                    out.append((option_args[0], option_args[1]))
                else:
                    raise InvalidLayout(self.split_layout)
        
        elif self.split_layout is SplitOption.DASH:
            for index, entry in enumerate(args):
                if entry.startswith('--') and index + 1 < len(args) and not args[index + 1].startswith('--'):
                    out.append((entry.removeprefix('--'), args[index + 1]))
                elif args[index - 1].startswith('--'):
                    pass
                else:
                    raise InvalidLayout(self.split_layout)
        
        """ elif self.split_layout is SplitOption.PARENTHESES:
            for entry in args:
                if entry.endswith(')'):
                    out.append((entry.split('(')[0], entry.split('(')[1].removesuffix(')')))
                else:
                    raise InvalidLayout(self.split_layout) """
        
        return out

    def on_start(self) -> Dict[str, CommandLineOption]:

        all_options = self._argument_processor()

        print(all_options)

        for entry in all_options:

            option = entry[0]
            argument = entry[1]

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
                        argument = True if argument.lower() == 'true' else False

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

        missing_required_options = [j for j in self.options.values() if j.required and j.argument is None]
        print(missing_required_options)

        for rule in self.rules:
            if rule[0] in missing_required_options and rule[1] in missing_required_options:
                 MissingRequiredOption(missing_required_options)
            else:
                if rule[0] in missing_required_options:
                    missing_required_options.pop(missing_required_options.index(rule[1]))
                elif rule[1] in missing_required_options:
                    missing_required_options.pop(missing_required_options.index(rule[1]))

        if missing_required_options == []:

            if self.show_info:
                print(str(self))

            return {option_name: option.argument for option_name, option in self.options.items()}
        else:
            raise MissingRequiredOption(missing_required_options)