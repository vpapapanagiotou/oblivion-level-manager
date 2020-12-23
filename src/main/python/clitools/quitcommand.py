from typing import List

from character import Character
from clitools.basecommand import BaseCommand
from tools.checks import is_typed_list


class QuitCommand(BaseCommand):
    def __init__(self):
        BaseCommand.__init__(self, "quit")

        self.add_alternative_name("exit")

    def get_help_string(self) -> List[str]:
        h: str = "Quits this program. No changes are saved."

        return [h]

    def _run(self, character: Character, args: List[str] = None):
        exit(0)
