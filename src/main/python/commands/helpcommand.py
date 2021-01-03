from textwrap import wrap
from typing import List, NoReturn

from tabulate import tabulate

from character import Character
from commands.basecommand import BaseCommand
from tools.checks import is_typed_list
from tools.formatting import format_base, BColors


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
                help_pars.append(_format_altnames(", ".join(command.alternative_names[1:])))

            for i in range(len(help_pars)):
                help_pars[i] = "\n".join(wrap(help_pars[i]))

            table.append([command.name, _format_usage(command.get_usage_string())])
            table.append([None, "\n".join(help_pars)])
            # table.append([None, None])

        self.help = tabulate(table, tablefmt="plain")


def _format_altnames(alternatives: str) -> str:
    assert isinstance(alternatives, str)

    return format_base("Alternative names: ", BColors.ITALIC) + alternatives


def _format_usage(usage: str) -> str:
    assert isinstance(usage, str)

    return format_base("Usage: ", BColors.ITALIC) + usage