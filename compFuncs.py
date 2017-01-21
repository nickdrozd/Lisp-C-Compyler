from parse import schemify # move to ctext?

from instructions import *
from instrseqs import *
from labels import *

from primitives import primitives
from registers import *

from compExp import compExp

#----------------------------------#

def compNum(expr, target, linkage):
	return NumSeq(expr, target, linkage)


def compVar(expr, target, linkage):
	return VarSeq(expr, target, linkage)


def compQuote(expr, target, linkage):
	_, text = expr
	lispText = schemify(text)

	return QuoteSeq(lispText, target, linkage)


def compAssDef(instrType):
	"instrType is string: 'ass' or 'def'"

	def transformSugarDef(exp):
		if type(exp[1]) is str:
			return exp

		_, [func, *args], *body = exp
		lambdaExp = ['lambda', args] + body
		return ['define', func, lambdaExp]
		
	def comp(expr, target, linkage):
		expr = transformSugarDef(expr)

		_, variable, value = expr
		valueCode = compExp(value, val, nex)

		seqType = AssDefSeq(instrType)
		instrSeq = seqType(variable, target)

		return preserving([env], 
					valueCode, 
					instrSeq).endWithLink(linkage)

		# return endWithLink(linkage, 
		# 		preserving([env], 
		# 			valueCode, 
		# 			instrSeq))

	return comp

compAss = compAssDef('ass')
compDef = compAssDef('def')


def compIf(expr, target=val, linkage=nex):
	_, ifTest, ifThen, ifElse = expr

	labels, branches = ifLabelsBranches()
	trueLabel, falseLabel, afterIfLabel = labels
	trueBranch, falseBranch, afterIfBranch = branches

	thenLink = afterIfLabel if linkage == nex else linkage

	testCode = compExp(ifTest, val, nex)
	thenCode = compExp(ifThen, target, linkage)
	elseCode = compExp(ifElse, target, thenLink)

	gotoTrueSeq = TestGotoSeq(trueLabel)

	# is afterIfBranch needed when linkage == ret?

	return preserving([env, cont],
			appendInstrSeqs(
				testCode, 
				gotoTrueSeq), 
			appendInstrSeqs(
				parallelInstrSeqs(
					appendInstrSeqs(
						falseBranch, 
						elseCode), 
					appendInstrSeqs(
						trueBranch, 
						thenCode)), 
				afterIfBranch))


def compBegin(expr, target=val, linkage=nex):
	_, *seq = expr
	return compSeq(seq, target, linkage)


def compSeq(seq, target=val, linkage=nex):
	*allButLast, lastExp = seq
	returnSeq = InstrSeq()
	for exp in allButLast:
		returnSeq = preserving([env, cont], 
				compExp(exp, target, nex), 
						returnSeq)

	return preserving([env, cont], 
				returnSeq, 
				compExp(lastExp, target, linkage))


def compLambda(expr, target=val, linkage=nex):
	_, params, *body = expr
	lispParams = schemify(params)

	labels, branches = lambdaLabelsBranches()
	funcEntry, afterLambda = labels	
	funcEntryBranch, afterLambdaBranch = branches

	lambdaLink = afterLambda if linkage == nex else linkage

	bodySeq = compSeq(body, val, ret)
	
	makeLambdaSeq = LambdaMakeSeq(target, funcEntry, lambdaLink)
	funcEntrySeq = LambdaEntrySeq(lispParams, bodySeq)

	return appendInstrSeqs(
				tackOnInstrSeq(
					makeLambdaSeq,
					appendInstrSeqs( 
						funcEntryBranch, 
						funcEntrySeq)), 
				afterLambdaBranch)


def compApp(expr, target=val, linkage=nex):
	function, *arguments = expr

	funcCode = compExp(function, target=func)
		
	argCodes = [compExp(arg) for arg in arguments]
	argListCode = constructArglist(argCodes)

	# this assumes that primitives won't be redefined
	if function in primitives:
		funcCallCode = PrimCallSeq(target, linkage)
	else:
		funcCallCode = compFuncCall(target, linkage)

	return preserving([env, cont], 
				funcCode, 
				preserving([func, cont], # redundant cont save?
					argListCode, 
					funcCallCode))


# def constructArglist(argCodes):
# 	if not argCodes:
# 		return NullArglSeq()

# 	# else
# 	lastArg, *restArgs = reversed(argCodes)
# 	lastArgSeq = appendInstrSeqs(
# 					lastArg, 
# 					ConsValNullSeq())
	
# 	consedArgs = InstrSeq()
# 	for argCode in restArgs:
# 		consedArgs = preserving(
# 					[env], 
# 					consedArgs, 
# 					preserving(
# 						[arglist], 
# 						argCode, 
# 						ConsValArglSeq()))

# 	return preserving(
# 				[env], 
# 				lastArgSeq, 
# 				consedArgs)



def constructArglist(argCodes):
	if not argCodes:
		return NullArglSeq()

	# else:
	lastArg, *restArgs = reversed(argCodes)
	instrSeq = ConsValNullSeq()
	codeToGetLastArg = appendInstrSeqs(
						lastArg, 
						instrSeq)

	if not restArgs:
		return codeToGetLastArg
	else:
		return preserving([env], 
				codeToGetLastArg,
				codeToGetRestArgs(restArgs))


def codeToGetRestArgs(argCodes):
	nextArg, *restArgs = argCodes
	instrSeq = ConsValArglSeq()
	codeForNextArg = preserving([arglist], 
						nextArg, 
						instrSeq)

	if not restArgs:
		return codeForNextArg
	else:
		return preserving([env], 
				codeForNextArg,
				codeToGetRestArgs(restArgs))


def compFuncCall(target, linkage):
	labels, branches = funcLabelsBranches()

	primitive, compound, compiled, afterCall = labels

	(primitiveBranch, compoundBranch, 
	 	compiledBranch, afterCallBranch) = branches

	endLabel = afterCall if linkage == nex else linkage

	testSeqs = FuncTestsSeq(primitive, compound)

	# calling compFuncApp twice generates two different endLabels
	compoundLink = compFuncApp(target, endLabel, 'compound')
	compiledLink = compFuncApp(target, endLabel, 'compiled')

	primitiveLink = PrimCallSeq(target, linkage)

	return appendInstrSeqs(
			testSeqs, 
			parallelInstrSeqs(
				appendInstrSeqs(
					compiledBranch, 
					compiledLink), 
				appendInstrSeqs(
					compoundBranch, 
					compoundLink), 
				appendInstrSeqs(
					primitiveBranch, 
					primitiveLink)), 
			afterCallBranch)


def compFuncApp(target, linkage, funcType):
	conditions = {
		(True, True) : 
			ValRetSeq, 
		(True, False) : 
			ValNotRetSeq, 
		(False, False) :
			NotValNotRetSeq
	}

	try:
		linkSeq = conditions[(
					target == val, 
					linkage == ret
				)]
	except:
		raise Exception('bad function call', 'compFuncApp')

	return linkSeq(funcType, target, linkage)


