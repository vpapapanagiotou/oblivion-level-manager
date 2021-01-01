from textwrap import wrap
from typing import List, NoReturn

from tabulate import tabulate

from character import Character
from clitools.basecommand import BaseCommand
from tools.checks import is_typed_list


class HelpCommand(BaseCommand):
    def __init__(self):
        super().__init__("help")

        self.help: str = "not initialized yet"

    def _run(self, character: Character, args: List[str] = None) -> NoReturn:
        assert is_typed_list(args, str)

        print(self.help)

    def get_help_string(self) -> List[str]:
        return ["Shows this help"]

    def generate_help(self, commands: List[BaseCommand]) -> NoReturn:
        assert is_typed_list(commands, BaseCommand)

        table = []
        for command in commands:
            help_pars: List[str] = command.get_help_string()

            if len(command.alternative_names) > 1:
                help_pars.append("Alternative names: " + ", ".join(command.alternative_names[1:]))

            for i in range(len(help_pars)):
                help_pars[i] = "\n".join(wrap(help_pars[i]))

            table.append([command.name, "\n".join(help_pars)])
            table.append([None, None])

        self.help = tabulate(table, tablefmt="plain")
