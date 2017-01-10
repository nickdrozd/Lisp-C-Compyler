from instructions import *
from ctext import *
from registers import *
from labels import *

# instructions

def LabelSeq(instrText):
	def Seq(label):
		return makeInstrSeq([], [], [instrText(label)])
	return Seq

TestGotoSeq = LabelSeq(ifTestGotoText)
BranchSeq = LabelSeq(branchText)

###

def SimpleSeq(instrText, needed):
	def Seq(expr, target, linkage):
		instr = instrText(expr)
		seq = makeInstrSeq(needed, [target], [instr])
		return endWithLink(linkage, seq)
	return Seq

NumSeq = SimpleSeq(numText, [])
VarSeq = SimpleSeq(lookupText, [env])
QuoteSeq = SimpleSeq(parseText, [])

###

def IfTestSeq(label):
	return makeInstrSeq([val], [], [ifTestText(label)])






###

# class LambdaSeq(InstrSeq):
# 	def __init__(self, target, linkage, lispParams, bodySeq):
# 		# labels
# 		labels, branches = makeLambdaLabels()
# 		funcEntry, afterLambda = labels
# 		funcEntryBranch, afterLambdaBranch = branches

# 		lambdaLink = afterLambda if linkage == nex else linkage

# 		makeSeq = LambdaMakeSeq(target, funcEntry, lambdaLink)
# 		entrySeq = LambdaEntrySeq(funcEntry, lispParams, bodySeq)

# 		super().__init__()
# 		for seq in makeSeq, entrySeq, afterLambdaBranch:
# 			self.append(seq)

# ###

# class AssDefSeq(InstrSeq):
# 	def __init__(self, variable, valueCode, target, linkage):
# 		super().__init__()
# 		self.append(valueCode)
# 		cmdSeq = AssDefCmdSeq(self.cmd, variable, target)
# 		# leave ass/def val as return val
# 		self.preserving([env], cmdSeq)
# 		self.endWithLink(linkage)

# class AssDefCmdSeq(InstrSeq):
# 	def __init__(self, cmd, var, target):
# 		super().__init__([env, val], [target], 
# 						[assDefText(cmd)(var)])

# class AssSeq(AssDefSeq):
# 	def __init__(self, variable, valueCode, target, linkage):
# 		self.cmd = assCmd
# 		super().__init__(variable, valueCode, target, linkage)

# class DefSeq(AssDefSeq):
# 	def __init__(self, variable, valueCode, target, linkage):
# 		self.cmd = defCmd
# 		super().__init__(variable, valueCode, target, linkage)























