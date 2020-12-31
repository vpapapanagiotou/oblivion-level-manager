import pickle
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import List

from character import Character
from clitools.basecommand import BaseCommand
from clitools.helpcommand import HelpCommand
from clitools.increaseskillcommand import IncreaseSkillCommand
from clitools.levelupcommand import LevelUpCommand
from clitools.printcommand import PrintCommand
from clitools.quitcommand import QuitCommand
from clitools.savecommand import SaveCommand
from clitools.setvaluecommand import SetValueCommand
from tools.common import print_exception

start_message: str = """
The Elder Scrolls IV: Oblivion
   ~~~~ Level Manager ~~~~


Type 'help' for a list of commands."""


class OblivionLevelManagerCLI:
    def __init__(self, character: Character):
        assert isinstance(character, Character)

        self.character: Character = character

        help_command: HelpCommand = HelpCommand()
        self.commands: List[BaseCommand] = [PrintCommand(), SetValueCommand(), IncreaseSkillCommand(), LevelUpCommand(),
                                            SaveCommand(), QuitCommand(), help_command]
        help_command.generate_help(self.commands)

    def start(self):
        print(start_message)

        while True:
            try:
                self._run_cli_iteration()
            except Exception as e:
                print_exception(e,
                                "An unknown exception has occurred. It is possible that the command failed and the character may be at a 'broken' state. You should avoid saving if you are unsure what happened.")
                raise  # debug

    def _run_cli_iteration(self):
        user_input: List[str] = []
        try:
            user_input = input("\n> ").split()
        except Exception as e:
            print_exception(e, "Error: not valid command: " + " ".join(user_input))
            return

        if len(user_input) == 0:
            return

        command_name = user_input[0]
        command_args = user_input[1:]

        for command in self.commands:
            if command.is_command(command_name):
                command.run(character, command_args)
                return

        print("Command not found: " + command_name)


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument('--path', default=",", type=str, help="Path to load/save the character files")
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

    cli: OblivionLevelManagerCLI = OblivionLevelManagerCLI(character)
    cli.start()
