'''
make_lispinc_header produces a header file of compiled
code ready for inclusion in the lispinc interpreter
(github.com/nickdrozd/lispinc). It will write to the
file comp_code.h, and will overwrite it if such a file
already exists.
'''


from parse import parse
from comp_exp import comp_exp
from instructions import statements
from labels import LABELS
from library import LIBRARY


LINE_ENDING = ' \\\n'
SECTION_DIVIDER = '\n\n'

INTRO = \
'''/*
    This code is compiler-generated!
    It may be ugly, but it sure is fast!
    Can you figure out how it works?

    https://github.com/nickdrozd/Lisp-C-Compyler
*/'''


def make_lispinc_header():
    return \
'''{}

#ifndef COMP_CODE_GUARD
#define COMP_CODE_GUARD

{}

#endif
'''.format(
    INTRO,
    SECTION_DIVIDER.join([
        make_code_body(),
        make_comp_cont(),
        make_comp_labels(),
    ]),
)


def make_code_body():
    return LINE_ENDING.join([
        '#define COMPILED_CODE_BODY',
        *[
            line
            for expr in LIBRARY
            for line in statements(comp_exp(parse(expr)))
        ],
        'goto DONE;',
    ])


def make_comp_cont():
    return LINE_ENDING.join([
        '#define COMP_CONT(REG)',
        *[
            'if (GETLABEL(REG) == _{}) goto {};'.format(label, label)
            for label in LABELS
        ],
    ])


def make_comp_labels():
    return LINE_ENDING.join([
        '#define ALL_COMPILED_LABELS',
        *[
            '_{},'.format(label)
            for label in LABELS[:-1]
        ],
        '_{}'.format(LABELS[-1]),
    ])


def write_lispinc_header():
    with open('comp_code.h', 'w') as comp_code:
        comp_code.write(
            make_lispinc_header())


if __name__ == '__main__':
    write_lispinc_header()
