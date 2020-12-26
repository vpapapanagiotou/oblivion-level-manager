def is_typed_list(lst: object, obj_type: type, allow_none: bool = False, allow_empty: bool = True) -> bool:
    """
    Check if a variable is a list that contains objects of specific type.

    :param lst: The variable/list to check
    :param obj_type: The type of objects that the list should contain (for the check to return true)
    :param allow_none: When set to true, return true if lst is None
    :param allow_empty: When set to true, return true if lst is empty
    :return: Whether lst is a list that contains only objects of type obj_type
    """
    assert isinstance(lst, object)
    assert isinstance(obj_type, type)
    assert isinstance(allow_none, bool)
    assert isinstance(allow_empty, bool)

    if allow_none and lst is None:
        return True

    if not isinstance(lst, list):
        return False

    if not allow_empty and len(lst) == 0:
        return False

    for obj in lst:
        if not isinstance(obj, obj_type):
            return False

    return True
