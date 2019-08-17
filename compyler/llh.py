''' LOW-LEVEL HELPERS '''

def isSelfEvaluating(exp):
    return isNum(exp) or isVar(exp)

# numbers

def isNum(exp):
    try:
        return isinstance(exp, int)
    except (TypeError, ValueError):
        return False

# variables

def isVar(exp):
    return isinstance(exp, str)
