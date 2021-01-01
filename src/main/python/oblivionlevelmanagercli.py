import pickle
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import List, NoReturn

from character import Character
from commands.basecommand import BaseCommand
from commands.helpcommand import HelpCommand
from commands.increaseskillcommand import IncreaseSkillCommand
from commands.levelupcommand import LevelUpCommand
from commands.plancommand import PlanCommand
from commands.printcommand import PrintCommand
from commands.quitcommand import QuitCommand
from commands.savecommand import SaveCommand
from commands.setvaluecommand import SetValueCommand
from tools.common import print_exception
from tools.formatting import format_error_message, format_base, BColors

start_message: str = """
The Elder Scrolls IV: Oblivion
   ~~~~ Level Manager ~~~~


Type 'help' for a list of commands."""

unknown_error_message: str = "An unknown error has occurred. This is most probably a bug."


class OblivionLevelManagerCLI:
    def __init__(self, character: Character):
        assert isinstance(character, Character)

        self.character: Character = character

        help_command: HelpCommand = HelpCommand()
        self.commands: List[BaseCommand] = [PrintCommand(),
                                            SetValueCommand(),
                                            IncreaseSkillCommand(),
                                            LevelUpCommand(),
                                            PlanCommand(),
                                            SaveCommand(),
                                            QuitCommand(),
                                            help_command]

        help_command.generate_help(self.commands)

    def start_interactive(self):
        print(start_message)

        while True:
            # This try is probably redundant because _run_cli_interaction handles exceptions internally
            try:
                self._run_cli_interaction()
            except Exception as e:
                print_exception(e, unknown_error_message)

    def _run_cli_interaction(self) -> NoReturn:
        user_input: str = ""
        try:
            user_input = input("\n> ")
        except Exception as e:
            print_exception(e, unknown_error_message)
            return

        if len(user_input) == 0:
            return

        try:
            self._run_command_str(user_input)
        except Exception as e:
            print_exception(e, unknown_error_message)

    def run_script(self, script: str) -> NoReturn:
        assert isinstance(script, str)

        command_strs: List[str] = script.split(";")

        for command_str in command_strs:
            try:
                self._run_command_str(command_str)
            except Exception as e:
                print_exception(e, unknown_error_message)
                break

    def _run_command_str(self, command_str: str) -> NoReturn:
        """
        Parse and execute a command from a string.

        :param command_str: A full command (with arguments)
        """
        assert isinstance(command_str, str)

        split_command_str: List[str] = command_str.split()
        command_name = split_command_str[0]
        command_args = split_command_str[1:]

        for command in self.commands:
            if command.is_command(command_name):
                command.run(character, command_args)
                return

        raise ValueError("Command not found: " + command_name)


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument('--path', default=".", type=str, help="Path to load/save the character files")
    parser.add_argument('--run', default="", type=str,
                        help="Run a command or list of commands (separated by ;) and exit")

    sp = parser.add_subparsers(dest='action')

    parser_new = sp.add_parser('new', help="Create a new character")
    parser_new.add_argument('name', type=str, help="The name of the new character")

    parser_load = sp.add_parser('load', help="Load a character")
    parser_load.add_argument('name', type=str, help="The name of the character to load")
    parser_load.add_argument('--level', default=0, type=int,
                             help="The level of the character to load (default: max available)")


    args: Namespace = parser.parse_args()

    file_path: Path = Path(args.path)

    if args.action == 'new':
        file_list = [x for x in file_path.glob(args.name + "_*.pickle")]
        if len(file_list) != 0:
            print("A character with name '" + args.name + "' already exists. Abort")
            exit(0)
        character: Character = Character(args.name)

    elif args.action == 'load':
        file_list = [x for x in file_path.glob(args.name + "_*.pickle")]
        if len(file_list) == 0:
            print("No character with name '" + args.name + "' was found. Abort")
            exit(0)
        if args.level < 0:
            print("No non-positive levels are supported. Abort")
            exit(0)
        if args.level == 0:
            level: int = 1
            for file in file_list:
                level = max(level, int(file.name[len(args.name) + 4:-7]))
        else:
            level = args.level
        file: Path = Path(args.name + "_lvl" + str(level).zfill(2) + ".pickle")
        if not file.exists():
            print("Cannot file file '" + file.name + "'. Abort")
            exit(0)
        character: Character = pickle.load(open(file, 'rb'))

    elif args.action is None:
        parser.print_usage()
        exit(0)

    else:
        raise ValueError("This should never be reached")

    try:
        character
    except NameError:
        print(format_error_message("Failed to create a character. Aborting...\n  This is probably a bug"))

    cli: OblivionLevelManagerCLI = OblivionLevelManagerCLI(character)
    if args.run == "":
        cli.start_interactive()
    else:
        cli.run_script(args.run)
