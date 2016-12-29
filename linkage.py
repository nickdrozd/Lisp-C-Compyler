from registers import *
from instructions import *
from ctext import *

ret = 'return'
nex = 'next'

def compileLinkage(linkage):
	if linkage == ret:
		return InstrSeq([cont], [], [gotoText('CONTINUE')])
	elif linkage == nex:
		return InstrSeq([], [], [])
	else:
		return InstrSeq([], [], [gotoText(linkage)])


def endWithLink(linkage, instrSeq):
	return preserving([cont], instrSeq, 
						compileLinkage(linkage))

# preserving?