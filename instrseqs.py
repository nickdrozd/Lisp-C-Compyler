from instructions import InstrSeq
from ctext import *
from registers import *

# instructions

###

class SimpleSeq(InstrSeq):
	def __init__(self, expr, target, linkage):
		instr = self.instrText(expr, target)
		super().__init__([], [target], [instr])
		self.endWithLink(linkage)

class NumSeq(SimpleSeq):
	def __init__(self, expr, target, linkage):
		self.instrText = numText
		super().__init__(expr, target, linkage)

class VarSeq(SimpleSeq):
	def __init__(self, expr, target, linkage):
		self.instrText = lookupText
		super().__init__(expr, target, linkage)
		self.addNeeded(env)

class QuoteSeq(SimpleSeq):
	def __init__(self, expr, target, linkage):
		self.instrText = parseText
		super().__init__(expr, target, linkage)

###

class IfTestSeq(InstrSeq):
	def __init__(self, label):
		instr = ifTestText(label)
		super().__init__([val], [], [instr])

###

class LambdaSeq(InstrSeq):
	def __init__(self, expr, target):
		# TODO: incorporate all lambda stuff here?
		instr = makeLambdaText(expr, target)
		super().__init__([env], [target], [instr])








class IfSeq(InstrSeq):
	def __init__(self, compiledCode, labels):
		testCode, thenCode, elseCode = compiledCode
		trueLabel, falseLabel, afterIfLabel = labels

		testGoto = ifTestGotoText(trueBranch)

		trueBranch, falseBranch, afterIfBranch = (
			branchText(label) for label in labels)







class AssDefSeq(InstrSeq):
	def __init__(self, variable, valueCode, target, linkage):
		super().__init__()
		self.append(valueCode)
		cmdSeq = AssDefCmdSeq(self.cmd, variable, target)
		self.preserving([env], cmdSeq)
		self.endWithLink(linkage)

class AssDefCmdSeq(InstrSeq):
	def __init__(self, cmd, var, target):
		super().__init__([env, val], [target], 
						[assDefText(cmd)(var)])

class AssSeq(AssDefSeq):
	def __init__(self, variable, valueCode, target, linkage):
		self.cmd = assCmd
		super().__init__(variable, valueCode, target, linkage)

class DefSeq(AssDefSeq):
	def __init__(self, variable, valueCode, target, linkage):
		self.cmd = defCmd
		super().__init__(variable, valueCode, target, linkage)























