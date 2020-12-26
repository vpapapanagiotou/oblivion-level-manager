from typing import List, TypeVar

from tools.checks import is_typed_list
from tools.common import simple_string_check, find


class NamedObject:
    def __init__(self, name: str):
        self.name: str = name

    def __str__(self) -> str:
        return self.get_name()

    def __eq__(self, other) -> bool:
        if issubclass(other.__class__, NamedObject):
            return other.get_name() == self.get_name()
        else:
            return False

    def is_named(self, name: str, strict: bool = False) -> bool:
        assert isinstance(name, str)

        if strict:
            return self.get_name() == name
        else:
            return simple_string_check(self.get_name(), name)

    def get_name(self) -> str:
        return self.name


def find_by_name(lst: List[NamedObject], name: str) -> List[int]:
    assert is_typed_list(lst, NamedObject)
    assert isinstance(name, str)

    return find([obj.is_named(name) for obj in lst])


def find_unique_by_name(lst: List[NamedObject], name: str, objects_name: str = None) -> int:
    # Type check for lst and name is done by 'find_by_name'
    assert len(lst) > 0
    assert isinstance(objects_name, str) or objects_name is None

    idx: List[int] = find_by_name(lst, name)

    if len(idx) == 1:
        return idx[0]

    if objects_name is None:
        objects_name = str(lst[0].__class__)

    if len(idx) == 0:
        raise ValueError("Cannot find " + objects_name + " matching: " + name)

    if len(idx) > 1:
        found: str = ", ".join([lst[i].name for i in idx])
        raise ValueError("Multiple " + objects_name + " found matching: " + name + " (" + found + ")")


NamedObjectChild = TypeVar("NamedObjectChild", bound=NamedObject)


def get_unique_by_name(lst: List[NamedObjectChild], name: str, objects_name: str = None) -> NamedObjectChild:
    # Type checking for lst, name, and objects_name is performed by 'find_by_name'
    assert len(lst) > 0

    idx = find_unique_by_name(lst, name, objects_name)

    return lst[idx]


def get_unique_by_names(lst: List[NamedObjectChild], names: List[str],
                        objects_name: str = None) -> List[NamedObjectChild]:
    # Type checking for lst and objects_name is performed by 'get_unique_by_name'
    assert is_typed_list(names, str)

    idxs: List[int] = [find_unique_by_name(l, name) for name in names]
    assert len(set(idxs)) == len(lst)

    return [lst[idx] for idx in idxs]
