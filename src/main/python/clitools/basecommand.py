from typing import List

from character import Character
from tools.checks import is_typed_list
from tools.common import print_exception
from tools.namedobject import NamedObject


class BaseCommand(NamedObject):
    def __init__(self, name: str):
        assert isinstance(name, str)

        super().__init__(name)

        self.alternative_names: List[str] = [name.lower()]

    def add_alternative_name(self, name: str):
        assert isinstance(name, str)

        self.alternative_names.append(name.lower())

    def is_command(self, command_name: str) -> bool:
        assert isinstance(command_name, str)

        return command_name in self.alternative_names

    def run(self, character: Character, args: List[str] = None) -> None:
        assert isinstance(character, Character)
        assert is_typed_list(args, str, True)

        try:
            self._run(character, args)
        except Exception as e:
            print_exception(e)
            raise  # debug

    def _run(self, character: Character, args: List[str]) -> None:
        raise NotImplementedError("Command not implemented: " + self.name)

    def get_help_string(self) -> List[str]:
        raise NotImplementedError("Command not implemented: " + self.name)
