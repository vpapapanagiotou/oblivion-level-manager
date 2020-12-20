def is_typed_list(x: object, obj_type: type, allow_none: bool = False, allow_empty: bool = True):
    assert isinstance(x, object)
    assert isinstance(obj_type, type)
    assert isinstance(allow_none, bool)
    assert isinstance(allow_empty, bool)

    if allow_none and x is None:
        return True

    if not isinstance(x, list):
        return False

    if not allow_empty and len(x) == 0:
        return False

    for i in x:
        if not isinstance(i, obj_type):
            return False

    return True
