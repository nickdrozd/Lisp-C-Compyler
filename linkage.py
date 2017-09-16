from registers import CONT
from instructions import make_instr_seq, empty_instr_seq, preserving

RET = 'return'
NEX = 'next'


def compile_linkage(linkage):
    if linkage == RET:
        return make_instr_seq([CONT], [], ['goto CONTINUE;'])

    elif linkage == NEX:
        return empty_instr_seq

    return make_instr_seq([], [], ['goto {};'.format(linkage)])


def end_with_link(linkage, instr_seq):
    return preserving(
        [CONT],
        instr_seq,
        compile_linkage(linkage)
    )
