from enum import Enum

from character import Skill
from tools.checks import is_typed_list


class BColors(Enum):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'


def format_base(s: str, fmt) -> str:
    assert isinstance(s, str)
    assert isinstance(fmt, BColors) or is_typed_list(fmt, BColors)

    if isinstance(fmt, BColors):
        fmt = [fmt]

    for f in fmt:
        s = f.value + s + BColors.ENDC.value

    return s


def format_skill(skill: Skill) -> str:
    assert isinstance(skill, Skill)

    name: str = skill.get_name()
    if skill.is_major:
        name = format_base(name, BColors.BOLD)

    return name
