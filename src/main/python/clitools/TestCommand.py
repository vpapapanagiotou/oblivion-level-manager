from typing import List, NoReturn

from character import Character
from clitools.basecommand import BaseCommand


class TestCommand(BaseCommand):
    def __init__(self):
        super().__init__("test")

    def get_help_string(self) -> List[str]:
        return []

    def _run(self, character: Character, args: List[str]) -> NoReturn:
        if args[0] == 'error':
            raise ValueError("Intentionally raising an error")
