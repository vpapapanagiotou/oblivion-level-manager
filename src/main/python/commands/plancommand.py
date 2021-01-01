from typing import List, NoReturn

from character import Character
from commands.basecommand import BaseCommand


class PlanCommand(BaseCommand):
    def __init__(self):
        super().__init__("plan")

    def get_help_string(self) -> List[str]:
        usage: str = "Usage: " + self.name + " att1 att2 [att3]"
        h: str = "Set a plan for current level. You can choose 2 or 3 attributes to plan a level (you should only " + \
                 "choose 2 attributes if you plan to level-up Luck). If you have already set a plan, it will be" + \
                 "replaced."

        return [usage, h]

    def _run(self, character: Character, args: List[str]) -> NoReturn:
        attribute_names: List[str] = character.set_plan(args)

        print("Set plan for attributes: " + ", ".join(attribute_names))
