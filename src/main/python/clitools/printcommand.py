from typing import List, NoReturn

from tabulate import tabulate

from character import Character, get_major_skills_increase, get_minor_skills_increase, get_skills_increase, format_skill
from clitools.basecommand import BaseCommand
from tools.common import simple_string_check, tabulated_with_centered_header
from tools.formatting import format_base, BColors


class PrintCommand(BaseCommand):
    def __init__(self):
        super().__init__("print")

        self.add_alternative_name("show")

    def get_help_string(self) -> List[str]:
        usage: str = "Usage: " + self.name + " [all|character|attributes|skills|plan]"
        h: str = "Print information about your character, attributes, skills, or level-up plan"

        return [usage, h]

    def _run(self, character: Character, args: List[str]) -> NoReturn:
        if len(args) > 1:
            raise ValueError("Too many input arguments")

        if len(args) == 0:
            args = ["all"]

        if simple_string_check("all", args[0]):
            print_summary(character)
            print_attributes(character)
            print_skills(character)
            print_plan(character)
        elif simple_string_check("character", args[0]):
            print_summary(character)
        elif simple_string_check("attributes", args[0]):
            print_attributes(character)
        elif simple_string_check("skills", args[0]):
            print_skills(character)
        elif simple_string_check("plan", args[0]):
            print_plan(character)
        else:
            raise ValueError("Unknown '" + args[0] + "' Can't print")


def print_summary(character: Character) -> NoReturn:
    assert isinstance(character, Character)

    table = [["Level", character.level],
             ["Major skill increases", get_major_skills_increase(character.skills)],
             ["Minor skill increases", get_minor_skills_increase(character.skills)],
             ["Total skill increases", get_skills_increase(character.skills)]]
    print(tabulated_with_centered_header(tabulate(table), "CHARACTER " + character.name))


def print_attributes(character: Character) -> NoReturn:
    assert isinstance(character, Character)

    attribute_headers = ("Attribute", "pts", "inc", "skill pts")

    table = []
    for attribute in character.attributes:
        ln = [attribute.name, attribute.value, "+" + str(attribute.get_attribute_gain()),
              get_skills_increase(attribute.skills)]
        table.append(ln)
    print(tabulated_with_centered_header(tabulate(table, headers=attribute_headers), "ATTRIBUTES"))


def print_skills(character: Character) -> NoReturn:
    assert isinstance(character, Character)

    skill_headers = ("Attribute", "Skill", "pts@" + str(character.level), "inc", "pts")

    table = []
    for attribute in character.attributes:
        if len(attribute.skills) == 0:
            continue
        attribute_table = []
        for skill in attribute.skills:
            ln = ["", format_skill(skill), skill.value, skill.level_ups, skill.value + skill.level_ups]
            attribute_table.append(ln)
        attribute_table[0][0] = format_base(attribute.get_name(), BColors.ITALIC)
        table.extend(attribute_table)
    print(tabulated_with_centered_header(tabulate(table, headers=skill_headers), "SKILLS"))


def print_plan(character: Character) -> NoReturn:
    assert isinstance(character, Character)

    if len(character.planned_attributes) == 0:
        print("No plan has been set")
        return

    plan_headers = ("Attribute", "pts", "Skill", "pts@" + str(character.level), "inc", "rem inc")

    table = []
    for attribute in character.planned_attributes:

        attribute_table = []
        for skill in attribute.skills:
            d: int = character.get_remaining_skill_increase(skill)
            if d > 0:
                dstr: str = str(d)
            elif d == 0:
                dstr: str = format_base(str(d), BColors.WARNING)
            else:
                dstr: str = format_base(str(d), BColors.FAIL)

            attribute_table.append([" ", " ", format_skill(skill), skill.value, skill.level_ups, dstr])
        attribute_table[0][0] = format_base(attribute.get_name(), BColors.ITALIC)
        attribute_table[0][1] = format_base(str(get_skills_increase(attribute.skills)), BColors.ITALIC)
        table.extend(attribute_table)
    print(tabulated_with_centered_header(tabulate(table, headers=plan_headers, colalign=("left", "right",)), "PLAN"))
