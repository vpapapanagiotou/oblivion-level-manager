from traceback import print_tb
from typing import List

from tools.checks import is_typed_list
from tools.formatting import format_error_message


def find(b: List[bool]) -> List[int]:
    """
    Find the indices of true values (equivalent to MATLAB's find function).

    :param b: A boolean array
    :return: The list of indices
    """
    assert is_typed_list(b, bool)

    idx = list()
    for i, bi in enumerate(b):
        if bi:
            idx.append(i)

    return idx


def simple_string_check(base: str, pattern: str) -> bool:
    """
    Very loose string comparison: checks if pattern is a prefix of base. Upper/lower case is not taken into account.

    :param base: The base string
    :param pattern: The pattern string to search for in base (as a prefix)
    :return: Whether strings match
    """
    assert isinstance(base, str)
    assert isinstance(pattern, str)
    assert 2 < len(base)
    assert 2 < len(pattern)

    n = len(pattern)
    return base.lower()[:n] == pattern.lower()


def print_exception(e: Exception, message: str = ""):
    if message == "":
        error_message: str = str(e)
    else:
        error_message: str = message + "\n" + str(e)

    print(format_error_message(error_message))
    # Uncomment the following for debugging
    # print_exception_for_debugging(e, message)


def print_exception_for_debugging(e: Exception, message: str = ""):
    print('---- EXCEPTION ----')
    print("type:", type(e))
    print("args:", e.args)
    print("exception:", e)
    print("message:", message)
    print("stracktrace:")
    print_tb(e.__traceback__)
    raise


def centered_header(header: str, length: int = None) -> str:
    assert isinstance(header, str)
    assert isinstance(length, int) or length is None

    header = "--- " + header + " ---"
    nheader: int = len(header)

    if nheader > length:
        return header

    nright: int = int((length - nheader) / 2)
    nleft: int = length - nright - nheader

    return ("-" * nright) + header + ("-" * nleft)


def tabulated_with_centered_header(tabulated: str, header: str) -> str:
    assert isinstance(tabulated, str)
    assert isinstance(header, str)

    idx: int = tabulated.find("\n")
    cheader: str = centered_header(header, idx)

    return cheader + "\n" + tabulated
