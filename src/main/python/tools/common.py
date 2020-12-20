from typing import List

from tools.checks import is_typed_list


def find(b: List[bool]) -> List[int]:
    assert is_typed_list(b, bool)

    idx = list()
    for i, bi in enumerate(b):
        if bi:
            idx.append(i)

    return idx


def simple_string_check(base: str, pattern: str) -> bool:
    assert isinstance(base, str)
    assert isinstance(pattern, str)
    assert 2 < len(base)
    assert 2 < len(pattern) <= len(base)

    n = len(pattern)
    return base.lower()[:n] == pattern.lower()