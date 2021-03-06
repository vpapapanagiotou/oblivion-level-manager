from typing import List, NoReturn

from character import Character
from commands.basecommand import BaseCommand


class LevelUpCommand(BaseCommand):
    def __init__(self):
        super().__init__("level-up")

        self.add_alternative_name("levelup")
        self.add_alternative_name("level")
        self.add_alternative_name("up")

    def get_usage_string(self) -> str:
        return self.name + " att1 att2 att3"

    def get_help_string(self) -> List[str]:
        h: str = "Level up your character by one level. Command arguments are the three, unique attributes that " + \
                 "you want to improve during the leveling up."

        return [h]

    def _run(self, character: Character, args: List[str]) -> NoReturn:
        character.level_up(args)
