from registers import *
from instructions import *

ret = 'return'
nex = 'next'


def compileLinkage(linkage):
    if linkage == ret:
        return makeInstrSeq([cont], [], ['goto CONTINUE;'])

    if linkage == nex:
        return emptyInstrSeq

    return makeInstrSeq([], [], [f'goto {linkage};'])


def endWithLink(linkage, instrSeq):
    return preserving(
        [cont],
        instrSeq,
        compileLinkage(linkage))
