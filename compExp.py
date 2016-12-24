'''
TODO:
	* documentation
	* generic instruction generator?
'''

from registers import *
from primitives import primitives
from instructions import *
from labels import makeLabel, labelInfo
from parse import schemify
from llh import *
from macros import transformMacros



def compExp(expr, target=val, linkage=nex):
	try:
		tag = getTag(expr)
	except:
		compType = compVar if isVar(expr) else compNum
		return compType(expr, target, val)

	expr = transformMacros(expr)

	compType = keyword_comps.get(tag, compApp)
	return compType(expr, target, val)










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
	comp = compAssDef(defVar, defVal, 'defineVar')
	return comp(expr, target, linkage)

def compIf(expr, target=val, linkage=nex):
	trueBranch = makeLabel('TRUE_BRANCH')
	falseBranch = makeLabel('FALSE_BRANCH')
	afterIf = makeLabel('AFTER_IF')
	thenLink = afterIf if linkage == nex else linkage

	trueBranchInfo = labelInfo(trueBranch)
	falseBranchInfo = labelInfo(falseBranch)
	afterIfInfo = labelInfo(afterIf)

	testCode = compExp(ifTest(expr), val, nex)
	thenCode = compExp(ifThen(expr), target, linkage)
	elseCode = compExp(ifElse(expr), target, thenLink)

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
	funcEntry = makeLabel('ENTRY')
	afterLambda = makeLabel('AFTER_LAMBDA')
	afterLambdaInfo = labelInfo(afterLambda)

	lambdaLink = afterLambda if linkage == nex else linkage
	lambdaBody = compLambdaBody(expr, funcEntry)
	
	instr = "%(target)s = COMPOBJ(_%(funcEntry)s, env);" % locals()
	instrSeq = makeInstrSeq([env], [target], [instr])

	instrLinked = endWithLink(lambdaLink, instrSeq)
	tackedOn = tackOnInstrSeq(instrLinked, lambdaBody)
	appended = appendInstrSeqs(tackedOn, afterLambdaInfo)

	return appended

def compLambdaBody(expr, funcEntry):
	params = lambdaParams(expr)
	lispParams = schemify(params)

	funcEntryInfo = labelInfo(funcEntry) 
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
	argCodes = list(map(
					(lambda arg: 
						compExp(arg)),
					arguments))
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
	primitiveBranch = makeLabel("PRIMITIVE")
	compoundBranch = makeLabel("COMPOUND")
	compiledBranch = makeLabel("COMPILED")
	afterCall = makeLabel("AFTER_CALL")

	endLabel = afterCall if linkage == nex else linkage

	primitiveBranchInfo = labelInfo(primitiveBranch)
	compoundBranchInfo = labelInfo(compoundBranch)
	compiledBranchInfo = labelInfo(compiledBranch)
	afterCallInfo = labelInfo(afterCall)

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
	compoundLink = compFuncApp(target, endLabel, 'compound')
	compiledLink = compFuncApp(target, endLabel, 'compiled') 

	primitiveLink = endWithLink(linkage, applyPrimitiveSeq)

	compiledLabeled = appendInstrSeqs(compiledBranchInfo, compiledLink)
	compoundLabeled = appendInstrSeqs(compoundBranchInfo, compoundLink)
	primitiveLabeled = appendInstrSeqs(primitiveBranchInfo, primitiveLink)

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
		funcReturn = makeLabel('FUNC_RETURN')

		assignCont = "cont = LABELOBJ(_%(funcReturn)s);" % locals()

		funcList = compiledList if isCompiled else compoundList

		funcReturnInfo = labelInfo(funcReturn)
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

def compileLinkage(linkage):
	if linkage == ret:
		return makeInstrSeq([cont], [], ['goto CONTINUE;'])
	elif linkage == nex:
		return emptyInstrSeq
	else:
		return makeInstrSeq([], [], ['goto %(linkage)s;' % locals()])


def endWithLink(linkage, instrSeq):
	return preserving([cont], instrSeq, compileLinkage(linkage))

#--------------------------#

def make_keyword_groups():
	return {
		('define', 'def') : compDef, 
		('set!', 'ass!') : compAss, 
		('lambda', 'λ', 'fun') : compLambda, 
		('if',) : compIf, 
		('begin', 'progn'): compBegin, 
		('quote',) : compQuote
	}

def make_keywords():
	keyword_groups = make_keyword_groups()
	keyword_comps = {}

	for group in keyword_groups:
		for key in group:
			keyword_comps[key] = keyword_groups[group]

	return (keyword_comps.keys(), keyword_comps)

(keywords, keyword_comps) = make_keywords()

