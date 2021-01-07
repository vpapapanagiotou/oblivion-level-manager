from typing import List

from tabulate import tabulate

from tools.checks import is_typed_list
from tools.namedobject import NamedObject, find_unique_by_name, get_unique_by_name, get_unique_by_names


class Skill(NamedObject):
    def __init__(self, name: str, is_major: bool = False, value: int = 5):
        assert isinstance(name, str)
        assert isinstance(is_major, bool)
        assert isinstance(value, int)

        super().__init__(name)

        self.is_major: bool = is_major
        self.value: int = value
        self.level_ups: int = 0
        self.attribute: Attribute = None

    def increase(self, value: int = 1):
        self.level_ups += value


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
        # Type checking is performed by 'get_unique_by_names'
        attributes: List[Attribute] = get_unique_by_names(self.attributes, attribute_names)
        assert len(attributes) == 3

        if not self.can_level_up():
            raise RuntimeError("Cannot level up yet")

        table = [[attribute.get_name(), attribute.get_attribute_gain()] for attribute in attributes]
        print("Will level up with the following attributes:")
        print(tabulate(table))

        self.level += 1

        for attribute in attributes:
            attribute.value += attribute.get_attribute_gain()

        for skill in self.skills:
            skill.value += skill.level_ups
            skill.level_ups = 0

    def set_plan(self, attribute_names: List[str]) -> List[str]:
        # Type checking is performed by 'get_unique_by_names'
        attributes: List[Attribute] = get_unique_by_names(self.attributes, attribute_names)
        assert len(attributes) == 2 or len(attributes) == 3

        self.planned_attributes: List[Attribute] = attributes

        return [attribute.get_name() for attribute in attributes]

    def get_remaining_skill_increase(self, skill: Skill):
        assert isinstance(skill, Skill)

        if skill.attribute not in self.planned_attributes:
            return 0

        # Limit by major skill increase
        if skill.is_major:
            d1: int = 10 - get_major_skills_increase(self.skills)
        else:
            d1: int = 10

        # Limit by attribute skill increase
        d2: int = 10 - get_skills_increase(skill.attribute.skills)

        # Limit by max skill level
        d3: int = 100 - skill.value

        return min(d1, d2, d3)

    def set_level_value(self, value: int) -> int:
        assert isinstance(value, int)

        self.level = value

        return self.level

    def set_attribute_value(self, attribute_name: str, value: int) -> (str, int):
        assert isinstance(attribute_name, str)
        assert isinstance(value, int)

        attribute: Attribute = get_unique_by_name(self.attributes, attribute_name)
        attribute.value = value

        return attribute.get_name(), attribute.value

    def set_skill_value(self, skill_name: str, value: int) -> (str, int):
        assert isinstance(skill_name, str)
        assert isinstance(value, int)

        skill: Skill = get_unique_by_name(self.skills, skill_name)
        skill.value = value

        return skill.get_name(), skill.value

    def set_skill_mode(self, skill_name: str, is_major: bool = True) -> (str, bool):
        assert isinstance(skill_name, str)
        assert isinstance(is_major, bool)

        skill: Skill = get_unique_by_name(self.skills, skill_name)
        skill.is_major = is_major

        return skill.get_name(), skill.is_major


def get_skills_increase(skills: List[Skill]) -> int:
    assert is_typed_list(skills, Skill)

    return sum([skill.level_ups for skill in skills])


def get_major_skills_increase(skills: List[Skill]) -> int:
    assert is_typed_list(skills, Skill)

    return sum([skill.level_ups for skill in skills if skill.is_major and skill.value < 100])


def get_minor_skills_increase(skills: List[Skill]) -> int:
    assert is_typed_list(skills, Skill)

    return sum([skill.level_ups for skill in skills if not skill.is_major])
