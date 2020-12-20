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

    def decrease(self, value: int = 1):
        self.level_ups -= value

    def get_name(self):
        if self.is_major:
            return self.name + "*"
        else:
            return self.name


class SkillOwner:
    def __init__(self, skills: List[Skill] = None):
        assert is_typed_list(skills, Skill, True)

        if skills is None:
            skills = list()

        self.skills: List[Skill] = skills

    def get_skills_increase(self):
        return sum([skill.level_ups for skill in self.skills])

    def get_major_skills_increase(self):
        return sum([skill.level_ups for skill in self.skills if skill.is_major])

    def get_minor_skills_increase(self):
        return sum([skill.level_ups for skill in self.skills if not skill.is_major])


class Attribute(NamedObject, SkillOwner):
    def __init__(self, name: str, value: int = 50):
        assert isinstance(name, str)
        assert isinstance(value, int)

        NamedObject.__init__(self, name)
        SkillOwner.__init__(self)

        self.value: int = value

    def assign_skill(self, skill: Skill):
        assert isinstance(skill, Skill)
        assert skill.attribute is None

        self.skills.append(skill)
        skill.attribute = self

    def set_skills(self, skills: List[Skill]):
        assert is_typed_list(skills, Skill)

        for skill in skills:
            self.assign_skill(skill)

    def is_attribute(self, name: str) -> bool:
        return simple_string_check(self.name, name)

    def has_skill(self, name: str) -> bool:
        return any([simple_string_check(skill.name, name) for skill in self.skills])

    def get_attribute_gain(self) -> int:
        n = self.get_skills_increase()
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


class Character(NamedObject, SkillOwner):
    def __init__(self, name: str, level: int = 1):
        assert isinstance(name, str)
        assert isinstance(level, int)

        NamedObject.__init__(self, name)
        SkillOwner.__init__(self)

        self.level: int = level

        skl_blade: Skill = Skill("Blade")
        skl_blunt: Skill = Skill("Blunt")
        skl_hand2hand: Skill = Skill("Hand to Hand")

        skl_armorer: Skill = Skill("Armorer")
        skl_block: Skill = Skill("Block")
        skl_heavyarmor: Skill = Skill("Heavy armor")

        skl_athletics: Skill = Skill("Athletics")
        skl_acrobatics: Skill = Skill("Acrobatics")
        skl_lightarmor: Skill = Skill("Light armor")

        skl_security: Skill = Skill("Security")
        skl_sneak: Skill = Skill("Sneak")
        skl_marksman: Skill = Skill("Marksman")

        skl_mercantile: Skill = Skill("Mercantile")
        skl_speechcraft: Skill = Skill("Speechcraft")
        skl_illusion: Skill = Skill("Illusion")

        skl_alchemy: Skill = Skill("Alchemy")
        skl_conjuration: Skill = Skill("Conjuration")
        skl_mysticism: Skill = Skill("Mysticism")

        skl_alteration: Skill = Skill("Alteration")
        skl_destruction: Skill = Skill("Destruction")
        skl_restoration: Skill = Skill("Restoration")

        att_strength: Attribute = Attribute("Strength")
        att_strength.set_skills([skl_blade, skl_blunt, skl_hand2hand])

        att_endurance: Attribute = Attribute("Endurance")
        att_endurance.set_skills([skl_armorer, skl_block, skl_heavyarmor])

        att_speed: Attribute = Attribute("Speed")
        att_speed.set_skills([skl_athletics, skl_acrobatics, skl_lightarmor])

        att_agility: Attribute = Attribute("Agility")
        att_agility.set_skills([skl_security, skl_sneak, skl_marksman])

        att_personality: Attribute = Attribute("Personality")
        att_personality.set_skills([skl_mercantile, skl_speechcraft, skl_illusion])

        att_intelligence: Attribute = Attribute("Intelligence")
        att_intelligence.set_skills([skl_alchemy, skl_conjuration, skl_mysticism])

        att_willpower: Attribute = Attribute("Willpower")
        att_willpower.set_skills([skl_alteration, skl_destruction, skl_restoration])

        att_luck: Attribute = Attribute("Luck")

        self.attributes: List[Attribute] = [att_strength, att_endurance, att_speed, att_agility, att_personality,
                                            att_intelligence, att_willpower, att_luck]

        for attribute in self.attributes:
            self.skills.extend(attribute.skills)

    def get_name(self) -> str:
        return self.name + "_lvl" + str(self.level).zfill(2)

    def increase_skill(self, skill_name: str, value: int = 1) -> (str, str):
        assert isinstance(skill_name, str)

        idx: int = find_unique_by_name(self.skills, skill_name)
        skill = self.skills[idx]
        skill.increase(value)

        return skill.name, skill.attribute.name

    def can_level_up(self) -> bool:
        return self.get_major_skills_increase() >= 10

    def level_up(self, attribute_names: List[str]):
        if not self.can_level_up():
            raise RuntimeError("Cannot level up yet")

        assert is_typed_list(attribute_names, str)
        assert len(attribute_names) == 3

        attribute_idxs: List[int] = []
        for attribute_name in attribute_names:
            idx = find_unique_by_name(self.attributes, attribute_name)
            attribute_idxs.append(idx)

        assert len(set(attribute_idxs)) == 3, "Exactly 3 unique attribute names must be provided"

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

    def set_skill_mode(self, skill_name: str, is_major: bool) -> (str, bool):
        assert isinstance(skill_name, str)
        assert isinstance(is_major, bool)

        idx = find_unique_by_name(self.skills, skill_name)
        self.skills[idx].is_major = is_major

        return self.skills[idx].get_name(), self.skills[idx].is_major
