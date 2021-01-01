from typing import List, NoReturn

from character import Character
from clitools.basecommand import BaseCommand


class IncreaseSkillCommand(BaseCommand):
    def __init__(self):
        super().__init__("increase-skill")

        self.add_alternative_name("increase")
        self.add_alternative_name("inc-skill")
        self.add_alternative_name("inc")

    def get_help_string(self) -> List[str]:
        usage: str = "Usage: " + self.name + " name [value]"
        h: str = "Increase a skill by 1 point. Argument 'value' can be used to increase (or decrease if negative) " + \
                 "by more points."

        return [usage, h]

    def _run(self, character: Character, args: List[str]) -> NoReturn:
        if len(args) == 0:
            raise ValueError("No skill name was provided")

        elif len(args) == 1:
            try:
                skill_name, attribute_name = character.increase_skill(args[0])
                print("Skill " + skill_name + " [" + attribute_name + "] increased!")
            except ValueError as e:
                e.args += ("Could not increase skill",)
                raise

        elif len(args) == 2:
            try:
                increase_value: int = int(args[1])
                skill_name, attribute_name = character.increase_skill(args[0], increase_value)
                print("Skill " + skill_name + " [" + attribute_name + "] increased by " + str(increase_value) + "!")
            except ValueError as e:
                e.args += ("Could not increase skill",)
                raise

        else:
            raise ValueError("More than one skill names were provided. Additional names will be ignored")
