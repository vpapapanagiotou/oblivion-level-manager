from typing import List

from character import Character
from clitools.basecommand import BaseCommand
from tools.namedobject import find_by_name


class LevelUpCommand(BaseCommand):
    def __init__(self):
        BaseCommand.__init__(self, "level-up")

        self.add_alternative_name("levelup")
        self.add_alternative_name("level")
        self.add_alternative_name("up")

    def get_help_string(self) -> List[str]:
        usage: str = "Usage: " + self.name + " att1 att2 att3"
        h: str = "Level up your character by one level. Command arguments are the three, unique attributes that you want to increase during the leveling up."

        return [usage, h]

    def run_command(self, character: Character, args: List[str]):
        character.level_up(args)
