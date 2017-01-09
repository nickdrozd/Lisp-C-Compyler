from instructions import InstrSeq
from ctext import *
from registers import *

# labels

class LabelSeq(InstrSeq):
	def __init__(self, label):
		super().__init__(statements=[self.text(label)])

class TestGotoSeq(LabelSeq):
	def __init__(self, label):
		self.text = ifTestGotoText
		super().__init__(label)

class BranchSeq(LabelSeq):
	def __init__(self, label):
		self.text = branchText
		super().__init__(label)

# lambda

class LambdaMakeSeq(InstrSeq):
	def __init__(self, target, entryLabel, lambdaLink):
		needs = env, 
		mods = target, 
		statements = [
			makeLambdaText(entryLabel, target), 
			gotoText(lambdaLink)
		]
		super().__init__(needs, mods, statements)

class LambdaEntrySeq(InstrSeq):
	def __init__(self, entryLabel, lispParams, bodySeq):
		needs = func, arglist
		mods = env, unev
		statements = [
			branchText(entryLabel), 
			funcEnvText, 
			parseParamsText(lispParams), 
			extendEnvText
		]
		super().__init__(needs, mods, statements)