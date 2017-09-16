''' LOW-LEVEL HELPERS '''


def is_self_evaluating(exp):
    return is_num(exp) or is_var(exp)


def is_num(exp):
    try:
        return type(int(exp)) == int
    except:
        return False


def is_var(exp):
    return type(exp) == str
