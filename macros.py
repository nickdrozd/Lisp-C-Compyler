from typing import Any
def transform_or(exp):
    if not exp[1:]:
        return 0

    first = exp[1]
    rest = transform_or(['or'] + exp[2:])
    return ['if', first, 1, rest]


def transform_cond(exp):
    _, *cond_pairs = exp
    if not cond_pairs:
        return '0'

    first_pair, *rest_pairs = cond_pairs

    condition, *consq_body = first_pair
    consequence = ['begin'] + consq_body

    if condition == 'else':
        return consequence

    rest_transformed = transform_cond(['cond'] + rest_pairs)

    transformed = ['if', condition, consequence, rest_transformed]

    return transformed


def transform_let(exp):
    _, bindings, *body = exp

    # is there a more elegant way to do this?
    variables = [binding[0] for binding in bindings]
    values = [binding[1] for binding in bindings]

    lambda_exp = ['lambda', variables] + body

    return [lambda_exp] + values


MACRO_TRANSFORMERS = {
    'let': transform_let,
    'cond': transform_cond,
    'or': transform_or,
    # 'and': transform_and,
    # 'delay': transform_delay,
}


def is_macro(expr: Any) -> bool:
    try:
        tag, *_ = expr
        return tag in MACRO_TRANSFORMERS
    except TypeError:
        return False


def transform_macro(expr):
    tag, *_ = expr
    return MACRO_TRANSFORMERS[tag](expr)


def transform_macros(expr: Any) -> Any:
    while is_macro(expr):
        expr = transform_macro(expr)

    return expr
