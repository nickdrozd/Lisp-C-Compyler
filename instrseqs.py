from ctext import *

# instructions

###

class SaveInstr(InstrSeq):
	def __init__(self, reg):
		super().__init__([reg], [], [saveText(reg)])

class RestoreInstr(InstrSeq):
	def __init__(self, reg):
		super().__init__([], [reg], [restoreText(reg)])

###

class NumInstr(InstrSeq):
	def __init__(self, expr, target, linkage):
		instr = numText(expr, target)
		super().__init__([], [target], [instr])

###

class VarInstr(InstrSeq):
	def __init__(self, expr, target, linkage):
		instr = lookupText(expr, target)
		super().__init__([env], [target], [instr])

###

class QuoteInstr(InstrSeq):
	def __init__(self, expr, target, linkage):
		instr = parseText(expr, target)
		super().__init__([], [target], [instr])

###

class IfTestInstr(InstrSeq):
	def __init__(self, label):
		instr = ifTestText(label)
		super().__init__([val], [], [instr])

###

class LambdaInstr(InstrSeq):
	def __init__(self, expr, target):
		# TODO: incorporate all lambda stuff here?
		# instr = makeLambdaText(expr, target)
		# super().__init__([env], [target], [instr])








class IfInstr(InstrSeq):
	def __init__(self, compiledCode, labels):
		testCode, thenCode, elseCode = compiledCode
		trueBranch, falseBranch, afterIf = labels




























