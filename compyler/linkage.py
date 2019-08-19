from registers import CONT
from instructions import (
    emptyInstrSeq,
    makeInstrSeq,
    preserving,
)

RET = 'return'
NEX = 'next'


def compileLinkage(linkage):
    if linkage == RET:
        return makeInstrSeq([CONT], [], ['goto CONTINUE;'])

    if linkage == NEX:
        return emptyInstrSeq

    return makeInstrSeq([], [], [f'goto {linkage};'])


def endWithLink(linkage, instrSeq):
    return preserving(
        [CONT],
        instrSeq,
        compileLinkage(linkage))
