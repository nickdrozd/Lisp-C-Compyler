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

from labels import branchesAndInfos
from parse import schemify
from macros import transformMacros
from llh import *

#----------------------------------#

def compExp(expr, target=val, linkage=nex):
	expr = transformMacros(expr)
	if isSelfEvaluating(expr):
		compType = compVar if isVar(expr) else compNum
	else:
		try:
			compType = keyword_comps[getTag(expr)]
		except:
			compType = compApp
	return compType(expr, target, linkage)

#----------------------------------#

def compNum(expr, target, linkage):
	instr = "%(target)s = NUMOBJ(%(expr)s);" % locals()
	instrSeq = makeInstrSeq([], [target], [instr])
	return endWithLink(linkage, instrSeq)

def compVar(expr, target, linkage):
	instr = "%(target)s = lookup(NAMEOBJ(\"%(expr)s\"), env);" % locals()
	instrSeq = makeInstrSeq([env], [target], [instr])
	return endWithLink(linkage, instrSeq)

def compQuote(expr, target, linkage):
	text = quotedText(expr)
	lispText = schemify(text)

	instr = '%(target)s = parse("%(lispText)s\\n");' % locals()
	instrSeq = makeInstrSeq([], [target], [instr])
	return endWithLink(linkage, instrSeq)

def compAssDef(varSel, valSel, CFunc):
	'''
	CFunc is string
	'''
	def comp(expr, target, linkage):
		var = varSel(expr)
		valueCode = compExp(valSel(expr), val, nex)

		# leave ass/def val as return val
		instr = CFunc + "(NAMEOBJ(\"%(var)s\"), val, env);" % locals()
		instrSeq = makeInstrSeq([env, val], [target], [instr])

		preserved = preserving([env], valueCode, instrSeq)
		return endWithLink(linkage, preserved)

	return comp

def compAss(expr, target, linkage):
	comp = compAssDef(assVar, assVal, 'setVar')
	return comp(expr, target, linkage)

def compDef(expr, target, linkage):
	expr = transformSugarDef(expr)
	comp = compAssDef(defVar, defVal, 'defineVar')
	return comp(expr, target, linkage)

def compIf(expr, target=val, linkage=nex):
	labels = ['TRUE_BRANCH', 'FALSE_BRANCH', 'AFTER_IF']

	branches, infos = branchesAndInfos(labels)

	[trueBranch, falseBranch, afterIf] = branches
	[trueBranchInfo, falseBranchInfo, afterIfInfo] = infos
	
	thenLink = afterIf if linkage == nex else linkage

	(ifTest, ifThen, ifElse) = ifClauses(expr)

	testCode = compExp(ifTest, val, nex)
	thenCode = compExp(ifThen, target, linkage)
	elseCode = compExp(ifElse, target, thenLink)

	isTrueInstr = "if (isTrue(val)) "
	gotoTrueInstr = "goto %(trueBranch)s;" % locals()
	instrList = [isTrueInstr + gotoTrueInstr]
	testGotoSeq = makeInstrSeq([val], [], instrList)

	thenCodeLabeled = appendInstrSeqs(trueBranchInfo, thenCode)
	elseCodeLabeled = appendInstrSeqs(falseBranchInfo, elseCode)

	elseThenSeq = parallelInstrSeqs(elseCodeLabeled, thenCodeLabeled)
	testGotosThenElseSeq = appendInstrSeqs(testGotoSeq, elseThenSeq, afterIfInfo)

	preserved = [env, cont]
	return preserving(preserved, testCode, testGotosThenElseSeq)

def compBegin(expr, target=val, linkage=nex):
	expr = beginActions(expr)
	return compSeq(expr, target, linkage)

def compSeq(seq, target=val, linkage=nex):
	first = firstExp(seq)
	if isLastExp(seq):
		return compExp(first, target, linkage)
	else:
		compFirst = compExp(first, target, nex)
		rest = restExps(seq)
		compRest = compSeq(rest, target, linkage)
		preserved = [env, cont]
		return preserving(preserved, compFirst, compRest)


def compLambda(expr, target=val, linkage=nex):
	labels = ('ENTRY', 'AFTER_LAMBDA')

	branches, infos = branchesAndInfos(labels)
	funcEntry, afterLambda = branches	
	funcEntryInfo, afterLambdaInfo = infos

	lambdaLink = afterLambda if linkage == nex else linkage
	lambdaBody = compLambdaBody(expr, funcEntryInfo)
	
	instr = "%(target)s = COMPOBJ(_%(funcEntry)s, env);" % locals()
	instrSeq = makeInstrSeq([env], [target], [instr])

	instrLinked = endWithLink(lambdaLink, instrSeq)
	tackedOn = tackOnInstrSeq(instrLinked, lambdaBody)
	appended = appendInstrSeqs(tackedOn, afterLambdaInfo)

	return appended

def compLambdaBody(expr, funcEntryInfo):
	params = lambdaParams(expr)
	lispParams = schemify(params)

	assignFuncEnv = "env = COMPENVOBJ(func);"
	parseParams = 'unev = parse("%(lispParams)s\\n");' % locals()
	extendFuncEnv = "env = extendEnv(unev, arglist, env);" # %(params)s ?

	instrList = [funcEntryInfo, assignFuncEnv, 
					parseParams, extendFuncEnv]

	instrSeq = makeInstrSeq([env, func, arglist], 
				[env], instrList)
	bodySeq = compSeq(lambdaBody(expr), val, ret)
	appended = appendInstrSeqs(instrSeq, bodySeq)

	return appended


def compApp(expr, target=val, linkage=nex):
	function = operator(expr)
	funcCode = compExp(function, target=func)
		
	arguments = operands(expr)
	argCodes = [compExp(arg) for arg in arguments]
	argListCode = constructArglist(argCodes)

	if function in primitives:
		primCall = "%(target)s = applyPrimitive(func, arglist);" % locals()
		primCallSeq = makeInstrSeq([func, arglist], [target], [primCall])
		funcCallCode = endWithLink(linkage, primCallSeq)
	else:
		funcCallCode = compFuncCall(target, linkage)

	arglPresFunc = preserving([func, cont], 
						argListCode, funcCallCode)

	return preserving([env, cont], 
				funcCode, arglPresFunc)

def constructArglist(argCodes):
	argCodes = argCodes[::-1]

	if len(argCodes) == 0:
		instr = "arglist = NULLOBJ;"
		return makeInstrSeq([], [arglist], [instr])
	# else:
	instr = "arglist = CONS(val, NULLOBJ);"
	instrSeq = makeInstrSeq([val], [arglist], [instr])
	lastArg = argCodes[0]
	codeToGetLastArg = appendInstrSeqs(lastArg, instrSeq)

	restArgs = argCodes[1:]
	if len(restArgs) == 0:
		return codeToGetLastArg
	else:
		return preserving([env], codeToGetLastArg,
					codeToGetRestArgs(restArgs))


def codeToGetRestArgs(argCodes):
	nextArg = argCodes[0]
	instr = "arglist = CONS(val, arglist);"
	instrSeq = makeInstrSeq([val, arglist], 
					[arglist], [instr])
	codeForNextArg = preserving([arglist], 
							nextArg, instrSeq)

	restArgs = argCodes[1:]
	if len(restArgs) == 0:
		return codeForNextArg
	else:
		return preserving([env], codeForNextArg,
					codeToGetRestArgs(restArgs))


def compFuncCall(target, linkage):
	labels = (
		'PRIMITIVE', 'COMPOUND', 
		'COMPILED', 'AFTER_CALL'
	)

	branches, infos = branchesAndInfos(labels)

	(primitiveBranch, compoundBranch, 
	 	compiledBranch, afterCall) = branches

	(primitiveBranchInfo, compoundBranchInfo, 
	 	compiledBranchInfo, afterCallInfo) = infos

	endLabel = afterCall if linkage == nex else linkage

	def makeTestGotoSeq(testString, label):
		test = "if (%(testString)s(func)) " % locals()
		goto = "goto %(label)s;" % locals()
		instrList = [test + goto]
		return makeInstrSeq([func], [], instrList)

	testPrimitiveSeq = makeTestGotoSeq('isPrimitive', primitiveBranch)
	testCompoundSeq = makeTestGotoSeq('isCompound', compoundBranch)
	testSeqs = appendInstrSeqs(testPrimitiveSeq, testCompoundSeq)

	applyPrimitive = "%(target)s = applyPrimitive(func, arglist);" % locals()
	applyPrimitiveSeq = makeInstrSeq([func, arglist], 
					[target], [applyPrimitive])

	# calling compFuncApp twice generates two different endLabels
	funcTypes = ('compound', 'compiled')
	compFuncApps = [
		compFuncApp(target, endLabel, funcType)
			for funcType in funcTypes]
	(compoundLink, compiledLink) = compFuncApps

	primitiveLink = endWithLink(linkage, applyPrimitiveSeq)

	branchLinks = (
		(compiledBranchInfo, compiledLink), 
		(compoundBranchInfo, compoundLink), 
		(primitiveBranchInfo, primitiveLink)
	)

	labeled = [appendInstrSeqs(branch, link)
				for (branch, link) in branchLinks]

	(compiledLabeled, compoundLabeled, 
		primitiveLabeled) = labeled

	compoundPrimPara = parallelInstrSeqs(compoundLabeled, primitiveLabeled)
	compiledPara = parallelInstrSeqs(compiledLabeled, compoundPrimPara)

	return appendInstrSeqs(testSeqs, compiledPara, afterCallInfo)


# funcType as string: 'compiled' or 'compound'
def compFuncApp(target, linkage, funcType):
	valTarg = target == val
	retLink = linkage == ret

	assignVal = "val = COMPLABOBJ(func);"
	gotoVal = "goto COMP_LABEL;"
	compiledList = [assignVal, gotoVal]

	saveCont = "save(cont);"
	gotoCompound = "goto APPLY_COMPOUND;"
	compoundList = [saveCont, gotoCompound]

	isCompiled = funcType == 'compiled'

	# typical function call, eg (f 5)
	if valTarg and not retLink:
		# common instructions
		assignCont = "cont = LABELOBJ(_%(linkage)s);" % locals()

		funcList = compiledList if isCompiled else compoundList
		instrList = [assignCont] + funcList
			
		return makeInstrSeq([func], allRegs, instrList)


	# target is func, eg in ((f 4) 5)
	elif not valTarg and not retLink:
		labels = ('FUNC_RETURN',)
		branches, infos = branchesAndInfos(labels)
		(funcReturn,) = branches
		(funcReturnInfo,) = infos

		assignCont = "cont = LABELOBJ(_%(funcReturn)s);" % locals()

		funcList = compiledList if isCompiled else compoundList

		assignTarget = "%(target)s = val;" % locals()
		gotoLinkage = "goto %(linkage)s;" % locals()

		returnList = [funcReturnInfo, assignTarget, gotoLinkage]

		instrList = [assignCont] + funcList + returnList

		return makeInstrSeq([func], allRegs, instrList)


	# this gets called, but I don't understand when
	elif valTarg and retLink:
		instrList = compiledList if isCompiled else compoundList

		return makeInstrSeq([func, cont], allRegs, instrList)

	else:
		Exception('bad function call', 'compFuncApp')

#----------------------------------#

def make_keyword_groups():
	return {
		define_keys : compDef, 
		ass_keys : compAss, 
		lambda_keys : compLambda, 
		if_keys : compIf, 
		begin_keys : compBegin, 
		quote_keys : compQuote
	}

def make_keywords():
	keyword_groups = make_keyword_groups()
	keyword_comps = {}

	for group in keyword_groups:
		for key in group:
			keyword_comps[key] = keyword_groups[group]

	return keyword_comps.keys(), keyword_comps

keywords, keyword_comps = make_keywords()

