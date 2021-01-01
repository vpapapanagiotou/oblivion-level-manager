import pickle
from typing import List, NoReturn

from character import Character
from commands.basecommand import BaseCommand


class SaveCommand(BaseCommand):
    def __init__(self):
        super().__init__("save")

    def _run(self, character: Character, args: List[str]) -> NoReturn:
        pickle.dump(character, open(character.get_name() + ".pickle", "wb"))

    def get_help_string(self) -> List[str]:
        h: str = "Saves the character to a (pickle) file. A different file is created for each character level. If " + \
                 "a file exists for a given level, it is overwriten."

        return [h]
