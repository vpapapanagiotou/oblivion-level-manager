from typing import List, NoReturn

from character import Character
from commands.basecommand import BaseCommand


class QuitCommand(BaseCommand):
    def __init__(self):
        super().__init__("quit")

        self.add_alternative_name("exit")

    def get_help_string(self) -> List[str]:
        h: str = "Quits this program. No changes are saved."

        return [h]

    def _run(self, character: Character, args: List[str] = None) -> NoReturn:
        exit(0)
