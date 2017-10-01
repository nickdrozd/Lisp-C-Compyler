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
    for expr in expr_seq:
        parsed = parse(expr)
        compiled = comp_exp(parsed)
        code = statements(compiled)

        for line in code:
            comp_code += line + ' \\' + '\n'
    comp_code += 'goto DONE;'

    comp_code += '\n\n'

    def is_last_label(label):
        labels_len = len(LABELS)
        label_index = LABELS.index(label)
        return label_index == labels_len - 1

    comp_code += '#define COMP_CONT(REG) \\' + '\n'
    for label in LABELS:
        last_label = is_last_label(label)
        label_check = (
            'if (GETLABEL(REG) == _' + label +
            ') ' + 'goto ' + label + ';' +
            ('' if last_label else ' \\' + '\n')
        )
        comp_code += label_check

    comp_code += '\n\n'

    comp_code += '#define ALL_COMPILED_LABELS \\' + '\n'
    # i = 0
    for label in LABELS:
        undscr_label = '_' + label
        if is_last_label(label):
            listed_label = undscr_label
        else:
            listed_label = undscr_label + ', \\' + '\n'
            # comma_label = undscr_label + ', '
            # if i < 2:
            #   listed_label = comma_label
            #   i += 1
            # else:
            #   listed_label = comma_label + '\\' + '\n'
            #   i = 0

        comp_code += listed_label

    comp_code += '\n\n' + '#endif' + '\n'

    return comp_code


def write_lispinc_header():
    with open('comp_code.h', 'w') as comp_code:
        comp_code.write(
            make_lispinc_header(LIBRARY))


if __name__ == '__main__':
    write_lispinc_header()
