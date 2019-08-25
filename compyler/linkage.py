from registers import CONT
from instructions import (
    InstrSeq,
    preserving,
)

RET = 'return'
NEX = 'next'


def compileLinkage(linkage):
    if linkage == RET:
        return InstrSeq([CONT], [], ['goto CONTINUE;'])

    if linkage == NEX:
        return InstrSeq([], [], [])

    return InstrSeq([], [], [f'goto {linkage};'])


def endWithLink(linkage, instrSeq):
    return preserving(
        [CONT],
        instrSeq,
        compileLinkage(linkage))
