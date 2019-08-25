'''
makeLispincHeader produces a header file of compiled
code ready for inclusion in the lispinc interpreter
(github.com/nickdrozd/lispinc). It will write to the
file comp_code.h, and will overwrite it if such a file
already exists.
'''


from parse import parse
from compExp import compExp
from labels import LABELS
from library import LIBRARY


HEADER = '''/*
    This code is compiler-generated!
    It may be ugly, but it sure is fast!
    Can you figure out how it works?

    https://github.com/nickdrozd/Lisp-C-Compyler
*/

#ifndef COMP_CODE_GUARD
#define COMP_CODE_GUARD

#define COMPILED_CODE_BODY \\
'''


def makeLispincHeader(exprSeq):
    with open('comp_code.h', 'w') as comp_code:
        comp_code.write(HEADER)

        for expr in exprSeq:
            for stmt in compExp(parse(expr)).stmts:
                comp_code.write(stmt + ' \\\n')

        comp_code.write('goto DONE;')

        comp_code.write('\n\n')

        def isLastLabel(label):
            labelsLen = len(LABELS)
            labelIndex = LABELS.index(label)
            return labelIndex == labelsLen - 1

        comp_code.write('#define COMP_CONT(REG)' + ' \\\n')

        for label in LABELS:
            comp_code.write(
                f'if (GETLABEL(REG) == _{label}) goto {label};'
                + ('' if isLastLabel(label) else ' \\\n')
            )

        comp_code.write('\n\n')

        comp_code.write('#define ALL_COMPILED_LABELS' + ' \\\n')

        for label in LABELS:
            comp_code.write(
                f'_{label}'
                + ('' if isLastLabel(label) else ',' + ' \\\n'))

        comp_code.write('\n\n')

        comp_code.write('#endif' + '\n')


if __name__ == '__main__':
    makeLispincHeader(LIBRARY)
