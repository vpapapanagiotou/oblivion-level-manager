from typing import List

from character import Character
from tools.checks import is_typed_list
from tools.namedobject import NamedObject


class BaseCommand(NamedObject):
    def __init__(self, name: str):
        assert isinstance(name, str)

        NamedObject.__init__(self, name)

        self.alternative_names: List[str] = list((name.lower(),))

    def add_alternative_name(self, name: str):
        self.alternative_names.append(name.lower())

    def is_command(self, command_name: str) -> bool:
        assert isinstance(command_name, str)

        for alternative_name in self.alternative_names:
            if command_name == alternative_name:
                return True

        return False

    def run(self, character: Character, args: List[str] = None):
        assert isinstance(character, Character)
        assert is_typed_list(args, str, True)

        try:
            self.run_command(character, args)
        except Exception as e:
            if len(e.args) == 0:
                print("There was an error")
            else:
                print(e)

    def run_command(self, character: Character, args: List[str]):
        raise NotImplementedError("Command not implemented: " + self.name)

    def get_help_string(self) -> List[str]:
        # raise NotImplementedError("Command not implemented: " + self.name)
        return ["coming soon"]
