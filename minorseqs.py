from instructions import InstrSeq
from ctext import *
from registers import *

class TestGotoSeq(InstrSeq):
	def __init__(self, label):
		super().__init__(statements=[ifTestGotoText(label)])

class BranchSeq(InstrSeq):
	def __init__(self, label):
		super().__init__(statements=[branchText(label)])

