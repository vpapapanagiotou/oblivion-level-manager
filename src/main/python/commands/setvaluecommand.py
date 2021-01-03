from typing import List, NoReturn

from character import Character
from commands.basecommand import BaseCommand
from tools.common import simple_string_check


class SetValueCommand(BaseCommand):
    def __init__(self):
        super().__init__("set-value")

        self.add_alternative_name("setvalue")
        self.add_alternative_name("set-val")
        self.add_alternative_name("setval")
        self.add_alternative_name("set")

    def get_usage_string(self) -> str:
        return self.name + " {level|attribute|skill} [name] value"

    def get_help_string(self) -> List[str]:
        h: str = "Utility to set-up your character after creation. Sub-commands 'attribute' and 'skill' require a " + \
                 "'name' argument (i.e. name of the attribute or skill whose value is being set)."

        return [h]

    def _run(self, character: Character, args: List[str]) -> NoReturn:
        if len(args) != 2 and len(args) != 3:
            raise ValueError(
                "Command 'set-value' takes exactly 2 or 3 arguments: 'level'/'attribute'/'skill', [name,] value")

        if simple_string_check("level", args[0]):
            if len(args) != 2:
                raise ValueError("'set-value level' takes only one extra argument: value")
            try:
                value = character.set_level_value(int(args[1]))
                print("Level is now " + str(value))
            except Exception as e:
                e.args += ("Could not set level:",)
                raise

        elif simple_string_check("attributes", args[0]):
            if len(args) != 3:
                raise ValueError("'set-value attribute' takes two extra arguments: name, value")
            try:
                name, value = character.set_attribute_value(args[1], int(args[2]))
                print("Attribute " + name + " is now " + str(value))
            except Exception as e:
                e.args += ("Could not set attribute:",)
                raise

        elif simple_string_check("skills", args[0]) or simple_string_check("sklls", args[0]):
            if len(args) != 3:
                raise ValueError("'set-value skill' takes two extra arguments: name, value")
            try:
                if _safe_simple_string_check("major", args[2]):
                    name, value = character.set_skill_mode(args[1], True)
                    value = "major" if value else "minor"
                elif _safe_simple_string_check("minor", args[2]):
                    name, value = character.set_skill_mode(args[1], False)
                    value = "major" if value else "minor"
                else:
                    name, value = character.set_skill_value(args[1], int(args[2]))
                print("Skill " + name + " is now " + str(value))
            except Exception as e:
                e.args += ("Could not set skill:",)
                raise

        else:
            raise ValueError("First argument should be 'level', 'attribute', or 'skill'")


def _safe_simple_string_check(base, pattern) -> bool:
    try:
        return simple_string_check(str(base), str(pattern))
    except:
        return False
