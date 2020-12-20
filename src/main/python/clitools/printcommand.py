from typing import List

from tabulate import tabulate

from character import Character
from clitools.basecommand import BaseCommand


class PrintCommand(BaseCommand):
    def __init__(self):
        BaseCommand.__init__(self, "print-character")

        self.add_alternative_name("print")
        self.add_alternative_name("show-character")
        self.add_alternative_name("show")
        self.add_alternative_name("character")

    def get_help_string(self) -> List[str]:
        usage: str = "Usage: " + self.name
        h: str = "Print a complete view of your character"

        return [usage, h]

    def run_command(self, character: Character, args: List[str]):
        print_summary(character)
        print_attributes(character)
        print_skills(character)


def print_summary(character: Character):
    assert isinstance(character, Character)

    table = []
    table.append(["Level", character.level])
    table.append(["Major skill increases", character.get_major_skills_increase()])
    table.append(["Minor skill increases", character.get_minor_skills_increase()])
    table.append(["Total skill increases", character.get_skills_increase()])
    print("\nCHARACTER " + character.name)
    print(tabulate(table))


def print_attributes(character: Character):
    assert isinstance(character, Character)

    attribute_headers = ("Attribute", "pts", "inc", "skill pts")

    table = []
    for attribute in character.attributes:
        ln = [attribute.name, attribute.value, "+" + str(attribute.get_attribute_gain()), attribute.get_skills_increase()]
        table.append(ln)
    print("\nATTRIBUTES")
    print(tabulate(table, headers=attribute_headers))


def print_skills(character: Character):
    assert isinstance(character, Character)

    skill_headers = ("Skill", "pts@" + str(character.level), "inc", "pts")

    table = []
    for attribute in character.attributes:
        for skill in attribute.skills:
            ln = [skill.get_name(), skill.value, skill.level_ups, skill.value + skill.level_ups]
            table.append(ln)
    print("\nSKILLS")
    print(tabulate(table, headers=skill_headers))
