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
            self._run_cli_iteration()
            try:
                pass
            except Exception as e:
                print(e)

    def _run_cli_iteration(self):
        user_input = input("\n> ")

        args = user_input.split()
        command_name = args[0].lower()

        for command in self.commands:
            if command.is_command(command_name):
                command.run(self.character, args[1:])
                return

        print("Unknown command: " + command_name)


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    sp = parser.add_subparsers(dest='action')

    parser_new = sp.add_parser('new', help="Create a new character")
    parser_new.add_argument('name', type=str, help="The name of the new character")

    parser_load = sp.add_parser('load', help="Load a character")
    parser_load.add_argument('name', type=str, help="The name of the character to load")
    parser_load.add_argument('--level', default=0, type=int,
                             help="The level of the character to load (default: max available)")

    args: Namespace = parser.parse_args()
    print(args)

    if args.action == 'new':
        p: Path = Path(".")
        file_list = [x for x in p.glob(args.name + "_*.pickle")]

        if len(file_list) != 0:
            print("A character with name '" + args.name + "' already exists. Abort")
            exit(0)

        character: Character = Character(args.name)

    elif args.action == 'load':
        p: Path = Path(".")
        file_list = [x for x in p.glob(args.name + "_*.pickle")]

        if len(file_list) == 0:
            print("No character with name '" + args.name + "' was found. Abort")
            exit(0)

        if args.level < 0:
            print("No non-positive levels are supported. Abort")
            exit(0)

        if args.level == 0:
            max_level: int = 1
            for file in file_list:
                new_level: int = int(file.name[len(args.name) + 4:-7])
                if new_level > max_level:
                    max_level = new_level
            file_name = args.name + "_lvl" + str(max_level).zfill(2) + ".pickle"
        else:
            file_name = args.name + "_lvl" + str(args.level).zfill(2) + ".pickle"

        file: Path = Path(file_name)
        if not file.exists():
            print("Cannot file file '" + file_name + "'. Abort")
            exit(0)

        character: Character = pickle.load(open(file_name, 'rb'))

    elif args.action is None:
        parser.print_usage()
        exit(0)

    else:
        raise ValueError("This should never be reached")

    cli: OblivionLevelManagerCLI = OblivionLevelManagerCLI(character)
    cli.start()
