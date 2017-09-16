from registers import *
from instructions import *

ret = 'return'
nex = 'next'


def compile_linkage(linkage):
    if linkage == ret:
        return make_instr_seq([cont], [], ['goto CONTINUE;'])

    elif linkage == nex:
        return empty_instr_seq

    return make_instr_seq([], [], ['goto %(linkage)s;' % locals()])


def end_with_link(linkage, instr_seq):
    return preserving(
        [cont],
        instr_seq,
        compile_linkage(linkage)
    )
