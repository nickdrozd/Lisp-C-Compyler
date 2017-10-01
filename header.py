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


def make_lispinc_header(expr_seq):
    comp_code = ''

    heading = \
'''/*
    This code is compiler-generated!
    It may be ugly, but it sure is fast!
    Can you figure out how it works?

    https://github.com/nickdrozd/Lisp-C-Compyler
*/

#ifndef COMP_CODE_GUARD
#define COMP_CODE_GUARD

#define COMPILED_CODE_BODY \\
'''

    comp_code += heading

    comp_code += ' \\\n'.join([
        line
        for expr in expr_seq
        for line in statements(comp_exp(parse(expr)))
    ] + ['goto DONE;'])

    comp_code += '\n\n'

    comp_code += '#define COMP_CONT(REG) \\' + '\n'

    comp_code += ' \\\n'.join((
        'if (GETLABEL(REG) == _{}) goto {};'.format(label, label)
        for label in LABELS
    ))

    comp_code += '\n\n'

    comp_code += '#define ALL_COMPILED_LABELS \\' + '\n'

    comp_code += ', \\\n'.join((
        '_{}'.format(label)
        for label in LABELS
    ))

    comp_code += '\n\n' + '#endif' + '\n'

    return comp_code


def write_lispinc_header():
    with open('comp_code.h', 'w') as comp_code:
        comp_code.write(
            make_lispinc_header(LIBRARY))


if __name__ == '__main__':
    write_lispinc_header()
