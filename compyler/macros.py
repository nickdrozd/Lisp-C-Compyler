def transformOr(exp):
    if len(exp[1:]) == 0:
        return 0

    first = exp[1]
    rest = transformOr(['or'] + exp[2:])
    return ['if', first, 1, rest]

def transformCond(exp):
    _, *condPairs = exp
    if not condPairs:
        return '0'

    firstPair, *restPairs = condPairs

    condition, *consqBody = firstPair
    consequence = ['begin'] + consqBody

    if condition == 'else':
        return consequence

    restTransformed = transformCond(['cond'] + restPairs)

    transformed = ['if', condition, consequence, restTransformed]

    return transformed

def transformLet(exp):
    _, bindings, *body = exp

    # is there a more elegant way to do this?
    variables = [binding[0] for binding in bindings]
    values = [binding[1] for binding in bindings]

    lambdaExp = ['lambda', variables] + body

    return [lambdaExp] + values


macro_transformers = {
    'let' : transformLet,
    'cond' : transformCond,
    'or' : transformOr,
    # 'and' : transformAnd,
    # 'delay' : transformDelay,
}

def isMacro(expr):
    try:
        tag, *_ = expr
    except TypeError:
        return False

    return tag in macro_transformers

def transformMacro(expr):
    tag, *_ = expr
    return macro_transformers[tag](expr)

def transformMacros(expr):
    while isMacro(expr):
        expr = transformMacro(expr)

    return expr
