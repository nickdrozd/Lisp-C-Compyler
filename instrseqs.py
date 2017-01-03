from instructions import *
from ctext import *
from registers import *
from minorseqs import *

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

class IfSeq(InstrSeq):
	def __init__(self, compiledCode, labels):
		super().__init__()

		testCode, thenCode, elseCode = compiledCode
		self.append(testCode)
		# print(self.statements)
		# print(self.needed)
		# print(self.modified)

		trueLabel, falseLabel, afterIfLabel = labels

		# does the test statement go with the test code 
		# or the branches code? it needs val, but we're 
		# given that testCode targets val
		testGotoTrue = ifTestGotoText(trueLabel)
		# print(testGotoTrue)

		trueBranch, falseBranch, afterIfBranch = (
			BranchSeq(label) for label in labels)

		# print(trueBranch)
		# print(falseBranch)
		# print(afterIfBranch)

		# how is this appending to self?
		branchesCode = parallelSeqs(
			testGotoTrue, 
			falseBranch, 
			elseCode, 
			trueBranch, 
			thenCode, 
			afterIfBranch
		)

		# print(branchesCode)

		# self.preserving([env, cont], branchesCode)
		# print(self.statements)
			

###

class LambdaSeq(InstrSeq):
	def __init__(self, expr, target):
		# TODO: incorporate all lambda stuff here?
		instr = makeLambdaText(expr, target)
		super().__init__([env], [target], [instr])










###

class AssDefSeq(InstrSeq):
	def __init__(self, variable, valueCode, target, linkage):
		super().__init__()
		self.append(valueCode)
		cmdSeq = AssDefCmdSeq(self.cmd, variable, target)
		# leave ass/def val as return val
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























