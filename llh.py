''' LOW-LEVEL HELPERS '''


from typing import Any
def is_self_evaluating(exp: Any) -> bool:
    return is_num(exp) or is_var(exp)


def is_num(exp: Any) -> bool:
    try:
        return isinstance(int(exp), int)
    except (TypeError, ValueError):
        return False


def is_var(exp: Any) -> bool:
    return isinstance(exp, str)
