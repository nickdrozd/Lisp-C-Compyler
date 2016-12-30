from ctext import *

# instructions

class InstrSeq:
	def __init__(self, needed=[], 
					modified=[], 
					statements=[]):
		self.needed = set(needed)
		self.modified = set(modified)
		self.statements = statements

	def needs(self, reg):
		return reg in self.needed

	def modifies(self, reg):
		return reg in self.modifies

###

class SaveInstr(InstrSeq):
	def __init__(self, reg):
		super().__init__([reg], [], [saveText(reg)])

class RestoreInstr(InstrSeq):
	def __init__(self, reg):
		super().__init__([], [reg], [restoreText(reg)])

###

class NumInstr(InstrSeq):
	def __init__(self, expr, target):
		instr = numText(expr, target)
		super().__init__([], [target], [instr])

###

class VarInstr(InstrSeq):
	def __init__(self, expr, target):
		instr = varText(expr, target)
		super().__init__([env], [target], [instr])

###

class QuoteInstr(InstrSeq):
	def __init__(self, expr, target):
		instr = quoteText(expr, target)
		super().__init__([], [target], [instr])

###

class IfTestInstr(InstrSeq):
	def __init__(self, label):
		instr = ifTestText(label)
		super().__init__([val], [], [instr])

###

class LambdaInstr(InstrSeq):
	def __init__(self, expr, target):
		instr = lambdaText(expr, target)
		super().__init__([env], [target], [instr])