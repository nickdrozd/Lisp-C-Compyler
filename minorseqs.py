from instructions import InstrSeq
from ctext import *
from registers import *

class BranchSeq(InstrSeq):
	def __init__(self, label):
		super().__init__(statements=[branchText(label)])

