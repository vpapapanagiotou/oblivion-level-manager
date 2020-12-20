from typing import List

from character import Character
from clitools.basecommand import BaseCommand


class IncreaseSkillCommand(BaseCommand):
    def __init__(self):
        BaseCommand.__init__(self, "increase-skill")

        self.add_alternative_name("increase")
        self.add_alternative_name("inc")

    def get_help_string(self) -> List[str]:
        usage: str = "Usage: " + self.name + " [value]"
        h: str = "Increase a skill by 1 point. Argument 'value' can be used to increase (or decrease if negative) by more points."

        return [usage, h]

    def run_command(self, character: Character, args: List[str]):
        if len(args) == 0:
            raise ValueError("No skill name was provided")

        elif len(args) == 1:
            try:
                skill_name, attribute_name = character.increase_skill(args[0])
                print("Skill " + skill_name + " [" + attribute_name + "] increased!")
            except ValueError as e:
                print("Could not increase skill:", e)

        elif len(args) == 2:
            try:
                increase_value: int = int(args[1])
                skill_name, attribute_name = character.increase_skill(args[0], increase_value)
                print("Skill " + skill_name + " [" + attribute_name + "] increased by " + str(increase_value) + "!")
            except ValueError as e:
                print("Could not increase skill:", e)

        else:
            raise ValueError("More than one skill names were provided. Additional names will be ignored")
