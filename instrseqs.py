from instructions import *
from ctext import *
from registers import *
from labels import LabelSeq, appLinkLabelsBranches
from linkage import *

# instructions

TestGotoSeq = LabelSeq(ifTestGotoText)

###

def SimpleSeq(instrText, needed):
	def Seq(expr, target, linkage):
		instr = instrText(expr)
		seq = InstrSeq(needed, [target], [instr])
		return endWithLink(linkage, seq)
	return Seq

NumSeq = SimpleSeq(numText, [])
VarSeq = SimpleSeq(lookupText, [env])
QuoteSeq = SimpleSeq(parseText, [])

###

def IfTestSeq(label):
	return InstrSeq([val], [], [ifTestText(label)])

###

def LambdaMakeSeq(target, entryLabel, lambdaLink):
	seq = InstrSeq([env], [target], [
			makeLambdaText(entryLabel, target), 
		])

	return endWithLink(lambdaLink, seq)

def LambdaEntrySeq(lispParams, bodySeq):
	stmnts = [
		funcEnvText, 
		parseParamsText(lispParams), 
		extendEnvText
	] + bodySeq.statements

	return InstrSeq([func, arglist], [env, unev], stmnts)

###

def PrimCallSeq(target, linkage):
	instr = applyPrimText(target)
	seq = InstrSeq([func, arglist], [target], [instr])
	return endWithLink(linkage, seq)

###

def TestFuncSeq(testText):
	def seq(label):
		return InstrSeq([func], [], [testText(label)])
	return seq

TestPrimitiveSeq = TestFuncSeq(isPrimitiveTestText)
TestCompoundSeq = TestFuncSeq(isCompoundTestText)

def FuncTestsSeq(primitiveLabel, compoundLabel):
	return appendInstrSeqs(
			TestPrimitiveSeq(primitiveLabel), 
			TestCompoundSeq(compoundLabel))

###

def NullArglSeq():
	return InstrSeq([], [arglist], [nullArglText])

def ConsValNullSeq():
	return InstrSeq([val], [arglist], [consValNullText])

def ConsValArglSeq():
	return InstrSeq([val, arglist], [arglist], [consValArglText])

###

def FuncAppLinkSeq(funcType):
	funcTypeStmnts = {
		'compiled' : [assValFuncLabelText, gotoValText], 
		'compound' : [saveCont, gotoCompound]
	}

	try:
		stmnts = funcTypeStmnts[funcType]
	except:
		raise Exception('Bad funcType: {}'.format(funcType))

	return InstrSeq([func], allRegs, stmnts)

def AssContSeq(linkage):
	return InstrSeq([], [cont], [assContText(linkage)])

def FuncReturnSeq(target, linkage):
	return InstrSeq([val], [target], 
					[valtoTargText(target), 
					gotoText(linkage)])


def ValNotRetSeq(funcType, target, linkage):
	# ignore target
	return appendInstrSeqs(
				AssContSeq(linkage), 
				FuncAppLinkSeq(funcType))

def NotValNotRetSeq(funcType, target, linkage):
	labels, branches = appLinkLabelsBranches()
	funcReturn, = labels
	funcReturnBranch, = branches

	return appendInstrSeqs(
				AssContSeq(funcReturn),
				FuncAppLinkSeq(funcType),  
				funcReturnBranch, 
				FuncReturnSeq(target, linkage))

def ValRetSeq(funcType, target, linkage):
	# seq needs cont, but not excplicitly
	AddContSeq = InstrSeq([cont], [], [])
	
	# ignore target and linkage
	return appendInstrSeqs(
				FuncAppLinkSeq(funcType), 
				AddContSeq)


























