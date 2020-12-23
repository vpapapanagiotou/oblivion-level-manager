from typing import List

from tabulate import tabulate

from tools.checks import is_typed_list
from tools.common import simple_string_check
from tools.namedobject import NamedObject, find_unique_by_name


class Skill(NamedObject):
    def __init__(self, name: str, is_major: bool = False, value: int = 5):
        assert isinstance(name, str)
        assert isinstance(is_major, bool)
        assert isinstance(value, int)

        super(Skill, self).__init__(name)

        self.is_major: bool = is_major
        self.value: int = value
        self.level_ups: int = 0
        self.attribute: Attribute = None

    def is_skill(self, name: str):
        return simple_string_check(self.name, name)

    def increase(self, value: int = 1):
        self.level_ups += value


def get_skills_increase(skills: List[Skill]) -> int:
    assert is_typed_list(skills, Skill)

    return sum([skill.level_ups for skill in skills])


def get_major_skills_increase(skills: List[Skill]) -> int:
    assert is_typed_list(skills, Skill)

    return sum([skill.level_ups for skill in skills if skill.is_major])


def get_minor_skills_increase(skills: List[Skill]) -> int:
    assert is_typed_list(skills, Skill)

    return sum([skill.level_ups for skill in skills if not skill.is_major])


class Attribute(NamedObject):
    def __init__(self, name: str, value: int = 50, skills: List[Skill] = []):
        assert isinstance(name, str)
        assert isinstance(value, int)
        # no need to check skills for correct type because it is checked by 'set_skills'

        super().__init__(name)

        self.value: int = value
        self.skills: List[Skill] = []

        self.set_skills(skills)

    def has_skill(self, name: str) -> bool:
        # Type check is handled by 'is_named'

        return any([skill.is_named(name) for skill in self.skills])

    def append_skill(self, skill: Skill):
        assert isinstance(skill, Skill)
        assert skill.attribute is None

        self.skills.append(skill)
        skill.attribute = self

    def set_skills(self, skills: List[Skill]):
        assert is_typed_list(skills, Skill, True)

        if skills is None or len(skills) == 0:
            self.skills = []
        else:
            for skill in skills:
                self.append_skill(skill)

    def get_attribute_gain(self) -> int:
        n = get_skills_increase(self.skills)
        if n == 0:
            return 1
        elif 1 <= n <= 4:
            return 2
        elif 5 <= n <= 7:
            return 3
        elif 8 <= n <= 9:
            return 4
        elif 10 <= n:
            return 5


class Character(NamedObject):
    def __init__(self, name: str, level: int = 1):
        assert isinstance(name, str)
        assert isinstance(level, int)

        super().__init__(name)

        self.level: int = level
        self.attributes: List[Attribute] = [
            Attribute("Strength", skills=[Skill("Blade"), Skill("Blunt"), Skill("Hand to Hand")]),
            Attribute("Endurance", skills=[Skill("Armorer"), Skill("Block"), Skill("Heavy Armor")]),
            Attribute("Speed", skills=[Skill("Athletics"), Skill("Acrobatics"), Skill("Light Armor")]),
            Attribute("Agility", skills=[Skill("Security"), Skill("Sneak"), Skill("Marksman")]),
            Attribute("Personality", skills=[Skill("Mercantile"), Skill("Speechcraft"), Skill("Illusion")]),
            Attribute("Intelligence", skills=[Skill("Alchemy"), Skill("Conjuration"), Skill("Mysticism")]),
            Attribute("Willpower", skills=[Skill("Alteration"), Skill("Destruction"), Skill("Restoration")]),
            Attribute("Luck")
        ]
        self.skills: List[Skill] = []

        for attribute in self.attributes:
            self.skills.extend(attribute.skills)

        self.planned_attributes: List[Attribute] = []

    def get_name(self) -> str:
        return self.name + "_lvl" + str(self.level).zfill(2)

    def increase_skill(self, skill_name: str, value: int = 1) -> (str, str):
        assert isinstance(skill_name, str)
        assert isinstance(value, int)

        idx: int = find_unique_by_name(self.skills, skill_name)
        skill = self.skills[idx]
        skill.increase(value)

        return skill.name, skill.attribute.name

    def can_level_up(self) -> bool:
        return get_major_skills_increase(self.skills) >= 10

    def level_up(self, attribute_names: List[str]) -> None:
        assert is_typed_list(attribute_names, str)
        assert len(attribute_names) == 3

        attribute_idxs: List[int] = []
        for attribute_name in attribute_names:
            idx = find_unique_by_name(self.attributes, attribute_name)
            attribute_idxs.append(idx)
        assert len(set(attribute_idxs)) == 3

        if not self.can_level_up():
            raise RuntimeError("Cannot level up yet")

        table = []
        for idx in attribute_idxs:
            table.append([self.attributes[idx].get_name(), self.attributes[idx].get_attribute_gain()])
        print("Will level up with the following attributes:")
        print(tabulate(table))

        self.level += 1

        for idx in attribute_idxs:
            self.attributes[idx].value += self.attributes[idx].get_attribute_gain()

        for skill in self.skills:
            skill.value += skill.level_ups
            skill.level_ups = 0

    def set_plan(self, attribute_names: List[str]) -> None:
        assert is_typed_list(attribute_names, str)

        self.planned_attributes: List[Attribute] = []
        for attribute_name in attribute_names:
            idx: int = find_unique_by_name(self.attributes, attribute_name)
            self.planned_attributes.append(self.attributes[idx])

    def get_max_skill_increase(self, skill: Skill):
        assert isinstance(skill, Skill)

        if skill.attribute not in self.planned_attributes:
            return 0

        if skill.is_major:
            d1: int = 10 - get_major_skills_increase(self.skills)
        else:
            d1: int = 10 * (len(self.planned_attributes) - 1) - get_minor_skills_increase(self.skills)

        d2: int = 10 - get_skills_increase(skill.attribute.skills)

        return min(d1, d2)

    def set_level_value(self, value: int) -> int:
        assert isinstance(value, int)

        self.level = value

        return self.level

    def set_attribute_value(self, attribute_name: str, value: int) -> (str, int):
        assert isinstance(attribute_name, str)
        assert isinstance(value, int)

        idx = find_unique_by_name(self.attributes, attribute_name)
        self.attributes[idx].value = value

        return self.attributes[idx].get_name(), self.attributes[idx].value

    def set_skill_value(self, skill_name: str, value: int) -> (str, int):
        assert isinstance(skill_name, str)
        assert isinstance(value, int)

        idx = find_unique_by_name(self.skills, skill_name)
        self.skills[idx].value = value

        return self.skills[idx].get_name(), self.skills[idx].value

    def set_skill_mode(self, skill_name: str, is_major: bool = True) -> (str, bool):
        assert isinstance(skill_name, str)
        assert isinstance(is_major, bool)

        idx = find_unique_by_name(self.skills, skill_name)
        self.skills[idx].is_major = is_major

        return self.skills[idx].get_name(), self.skills[idx].is_major
