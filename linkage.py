from registers import *
from instructions import *

ret = 'return'
nex = 'next'

def compileLinkage(linkage):
	if linkage == ret:
		return InstrSeq([cont], [], ['goto CONTINUE;'])
	elif linkage == nex:
		return InstrSeq()
	else:
		return InstrSeq([], [], ['goto %(linkage)s;' % locals()])


def endWithLink(linkage, instrSeq):
	return preserving([cont], instrSeq, 
						compileLinkage(linkage))