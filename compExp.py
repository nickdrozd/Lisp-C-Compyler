'''
TODO:
	* documentation
	* generic instruction generator?
	* instrSeq class
	* remove llh?
	* rename 'infos'
	* move out keyword_groups (how?)
'''

from registers import *
from keywords import *
from primitives import primitives

from instructions import *
from linkage import *

from labels import *
from parse import schemify, parse
from macros import transformMacros
from llh import *

from instrseqs import *

#----------------------------------#

def compExp(expr, target=val, linkage=nex):
	expr = transformMacros(expr)
	if isSelfEvaluating(expr):
		compType = compVar if isVar(expr) else compNum
	else:
		try:
			tag, *_ = expr
			compType = keyword_comps[tag]
		except:
			compType = compApp
	return compType(expr, target, linkage)

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

		return endWithLink(linkage, 
				preserving([env], 
					valueCode, 
					instrSeq))

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

	testCodeGoto = appendInstrSeqs(testCode, gotoTrueSeq) 
	thenCodeLabeled = appendInstrSeqs(trueBranch, thenCode)
	elseCodeLabeled = appendInstrSeqs(falseBranch, elseCode)

	# is afterIfBranch needed when linkage == ret?

	return preserving([env, cont],
		testCodeGoto, 
		appendInstrSeqs(
			parallelInstrSeqs(
				elseCodeLabeled, 
				thenCodeLabeled), 
			afterIfBranch))


# def compIf(expr, target=val, linkage=nex):
# 	labels = ['TRUE_BRANCH', 'FALSE_BRANCH', 'AFTER_IF']

# 	branches, infos = labelsAndBranches(labels)

# 	[trueBranch, falseBranch, afterIf] = branches
# 	[trueBranchInfo, falseBranchInfo, afterIfInfo] = infos
	
# 	thenLink = afterIf if linkage == nex else linkage

# 	(_, ifTest, ifThen, ifElse) = expr

# 	testCode = compExp(ifTest, val, nex)
# 	thenCode = compExp(ifThen, target, linkage)
# 	elseCode = compExp(ifElse, target, thenLink)

# 	isTrueInstr = "if (isTrue(val)) "
# 	gotoTrueInstr = "goto %(trueBranch)s;" % locals()
# 	instrList = [isTrueInstr + gotoTrueInstr]
# 	testGotoSeq = InstrSeq([val], [], instrList)

# 	thenCodeLabeled = appendInstrSeqs(trueBranchInfo, thenCode)
# 	elseCodeLabeled = appendInstrSeqs(falseBranchInfo, elseCode)

# 	elseThenSeq = parallelInstrSeqs(elseCodeLabeled, thenCodeLabeled)
# 	testGotosThenElseSeq = appendInstrSeqs(testGotoSeq, elseThenSeq, afterIfInfo)

# 	preserved = [env, cont]
# 	return preserving(preserved, testCode, testGotosThenElseSeq)


def compBegin(expr, target=val, linkage=nex):
	_, *seq = expr
	return compSeq(seq, target, linkage)


def compSeq(seq, target=val, linkage=nex):
    returnSeq, regs = InstrSeq(), [env, cont]
    for exp in reversed(seq):
        returnSeq = preserving(
        	regs, 
        	compExp(exp, target, linkage), 
        	returnSeq)
    return returnSeq


# def compLambda(expr, target=val, linkage=nex):
# 	labels = ('ENTRY', 'AFTER_LAMBDA')

# 	branches, infos = labelsAndBranches(labels)
# 	funcEntry, afterLambda = branches	
# 	funcEntryInfo, afterLambdaInfo = infos

# 	lambdaLink = afterLambda if linkage == nex else linkage
# 	lambdaBody = compLambdaBody(expr, funcEntryInfo)
	
# 	instr = "%(target)s = COMPOBJ(_%(funcEntry)s, env);" % locals()
# 	instrSeq = InstrSeq([env], [target], [instr])

# 	instrLinked = endWithLink(lambdaLink, instrSeq)
# 	tackedOn = tackOnInstrSeq(instrLinked, lambdaBody)
# 	appended = appendInstrSeqs(tackedOn, afterLambdaInfo)

# 	return appended


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
		makeLambdaSeq, 
		funcEntryBranch, 
		funcEntrySeq, 
		afterLambdaBranch		
	)


# def compLambdaBody(expr, funcEntryInfo):
# 	_, params, *body = expr
# 	lispParams = schemify(params)

# 	assignFuncEnv = "env = COMPENVOBJ(func);"
# 	parseParams = 'unev = parse("%(lispParams)s\\n");' % locals()
# 	extendFuncEnv = "env = extendEnv(unev, arglist, env);" # %(params)s ?

# 	instrList = [funcEntryInfo, assignFuncEnv, 
# 					parseParams, extendFuncEnv]

# 	instrSeq = InstrSeq([env, func, arglist], 
# 				[env], instrList)
# 	bodySeq = compSeq(body, val, ret)
# 	appended = appendInstrSeqs(instrSeq, bodySeq)

# 	return appended


def compApp(expr, target=val, linkage=nex):
	function, *arguments = expr

	funcCode = compExp(function, target=func)
		
	argCodes = [compExp(arg) for arg in arguments]
	argListCode = constructArglist(argCodes)

	# print(expr, 'argListCode')
	# print(argListCode)
	# print()

	# this assumes that primitives won't be redefined
	if function in primitives:
		funcCallCode = PrimCallSeq(target, linkage)
	else:
		funcCallCode = compFuncCall(target, linkage)

	# print(funcCallCode.statements)
	# print()

	# for stmnt in funcCallCode.statements:
	# 	print(stmnt)
	# print()

	return preserving(
			[env, cont], 
			funcCode, 
			preserving(
				[func, cont], # redundant cont save?
				argListCode, 
				funcCallCode
			)
		)


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
	codeToGetLastArg = appendInstrSeqs(lastArg, instrSeq)

	if not restArgs:
		return codeToGetLastArg
	else:
		return preserving([env], codeToGetLastArg,
					codeToGetRestArgs(restArgs))


def codeToGetRestArgs(argCodes):
	nextArg, *restArgs = argCodes
	instrSeq = ConsValArglSeq()
	codeForNextArg = preserving([arglist], 
							nextArg, instrSeq)

	if not restArgs:
		return codeForNextArg
	else:
		return preserving([env], codeForNextArg,
					codeToGetRestArgs(restArgs))


def compFuncCall(target, linkage):
	labels, branches = funcLabelsBranches()

	primitive, compound, compiled, afterCall = labels

	(primitiveBranch, compoundBranch, 
	 	compiledBranch, afterCallBranch) = branches

	endLabel = afterCall if linkage == nex else linkage

	testSeqs = FuncTestsSeq(primitive, compound)

	# calling compFuncApp twice generates two different endLabels
	funcTypes = 'compound', 'compiled'
	compoundLink, compiledLink = [
		compFuncApp(target, endLabel, funcType)
			for funcType in funcTypes]

	primitiveLink = PrimCallSeq(target, linkage)

	branchLinks = (
		(compiledBranch, compiledLink), 
		(compoundBranch, compoundLink), 
		(primitiveBranch, primitiveLink)
	)

	labeled = [appendInstrSeqs(branch, link)
				for (branch, link) in branchLinks]

	(compiledLabeled, compoundLabeled, 
		primitiveLabeled) = labeled

	compoundPrimPara = parallelInstrSeqs(
						compoundLabeled, 
						primitiveLabeled)
	compiledPara = parallelInstrSeqs(compiledLabeled, compoundPrimPara)

	return appendInstrSeqs(testSeqs, compiledPara, afterCallBranch)


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
					linkage == ret)]
	except:
		raise Exception('bad function call', 'compFuncApp')

	return linkSeq(funcType, target, linkage)


# def compFuncApp(target, linkage, funcType):
# 	"funcType as string: 'compiled' or 'compound'"
# 	valTarg = target == val
# 	retLink = linkage == ret

# 	assignVal = "val = COMPLABOBJ(func);"
# 	gotoVal = "goto COMP_LABEL;"
# 	compiledList = [assignVal, gotoVal]

# 	saveCont = "save(cont);"
# 	gotoCompound = "goto APPLY_COMPOUND;"
# 	compoundList = [saveCont, gotoCompound]

# 	isCompiled = funcType == 'compiled'

# 	# typical function call, eg (f 5)
# 	if valTarg and not retLink:
# 		# common instructions
# 		assignCont = "cont = LABELOBJ(_%(linkage)s);" % locals()

# 		funcList = compiledList if isCompiled else compoundList
# 		instrList = [assignCont] + funcList
			
# 		return InstrSeq([func], allRegs, instrList)


# 	# target is func, eg in ((f 4) 5)
# 	elif not valTarg and not retLink:
# 		labels, branches = appLinkLabelsBranches()
# 		funcReturn, = labels
# 		funcReturnBranch, = branches

# 		assignCont = "cont = LABELOBJ(_%(funcReturn)s);" % locals()

# 		funcList = compiledList if isCompiled else compoundList

# 		assignTarget = "%(target)s = val;" % locals()
# 		gotoLinkage = "goto %(linkage)s;" % locals()

# 		returnList = [funcReturnBranch, assignTarget, gotoLinkage]

# 		instrList = [assignCont] + funcList + returnList

# 		return InstrSeq([func], allRegs, instrList)


# 	# this gets called, but I don't understand when
# 	elif valTarg and retLink:
# 		instrList = compiledList if isCompiled else compoundList

# 		return InstrSeq([func, cont], allRegs, instrList)

# 	else:
# 		raise Exception('bad function call', 'compFuncApp')

#----------------------------------#

def makeKeywords():
	keyword_groups = {
		define_keys : compDef, 
		ass_keys : compAss, 
		lambda_keys : compLambda, 
		if_keys : compIf, 
		begin_keys : compBegin, 
		quote_keys : compQuote
	}

	keyword_comps = {}

	for group in keyword_groups:
		for key in group:
			keyword_comps[key] = keyword_groups[group]

	return keyword_comps.keys(), keyword_comps

keywords, keyword_comps = makeKeywords()

