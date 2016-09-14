# TODO: 
# 	* BEGIN???
#	* default args to comp funcs (target=val and linkage=nex) ???
#	* add COMP_LABEL continue dispatch to ec_main.c
#	* list of parse calls to constants, e.g
#		* Obj obj4 = parse("n\n");
#		* use somethine like makeLabel

# TODO: figure out which funcs are needed
from keywords import *
from instructions import *
from labels import makeLabel
from labels import labelInfo
from llh import *
from parse import schemify


def compileDisp(expr, target=val, linkage=nex):
	if isNum(expr):
		return compNum(expr, target, linkage)
	elif isVar(expr):
		return compVar(expr, target, linkage)
	elif isLambda(expr):
		return compLambda(expr, target, linkage)
	elif isIf(expr):
		return compIf(expr, target, linkage)
	elif isDef(expr):
		return compDef(expr, target, linkage)
	elif isAss(expr):
		return compAss(expr, target, linkage)
	elif isQuote(expr):
		return compQuote(expr, target, linkage)
	elif isOr(expr):
		expr = transformOr(expr)
		return compIf(expr, target, linkage)
	elif isBegin(expr):
		expr = beginActions(expr)
		return compSeq(expr, target, linkage)
	else:
		return compApp(expr, target, linkage)







def compLink(linkage):
	if linkage == ret:
		return makeInstrSeq([cont], [], ['goto CONTINUE;'])
	elif linkage == nex:
		return emptyInstrSeq
	else:
		return makeInstrSeq([], [], ['goto %(linkage)s;' % locals()])


def endWithLink(linkage, instrSeq):
	return preserving([cont], instrSeq, compLink(linkage))



def compNum(expr, target, linkage):
	instr = "%(target)s = NUMOBJ(%(expr)s);" % locals()
	instrSeq = makeInstrSeq([], [target], [instr])
	return endWithLink(linkage, instrSeq)

def compQuote(expr, target, linkage):
	text = quotedText(expr)
	lispText = schemify(text)

	instr = '%(target)s = parse("%(lispText)s\\n");' % locals()
	instrSeq = makeInstrSeq([], [target], [instr])
	return endWithLink(linkage, instrSeq)

def compVar(expr, target, linkage):
	instr = "%(target)s = lookup(NAMEOBJ(\"%(expr)s\"), env);" % locals()
	instrSeq = makeInstrSeq([env], [target], [instr])
	return endWithLink(linkage, instrSeq)

def compAssDef(varSel, valSel, CFunc):
	'''
	CFunc is string
	'''
	def comp(expr, target, linkage):
		var = varSel(expr)
		valueCode = compileDisp(valSel(expr), val, nex)

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

	testCode = compileDisp(ifTest(expr), val, nex)
	thenCode = compileDisp(ifThen(expr), target, thenLink)
	# fallthrough after false branch?
	elseCode = compileDisp(ifElse(expr), target, linkage)

	isTrueInstr = "if (isTrue(val)) "
	gotoTrueInstr = "goto %(trueBranch)s;" % locals()
	gotoFalseInstr = "goto %(falseBranch)s;" % locals()
	testGotoInstr = isTrueInstr + gotoTrueInstr + '\n' + gotoFalseInstr
	testGotoSeq = makeInstrSeq([val], [], [testGotoInstr])

	thenCodeLabeled = appendInstrSeqs(trueBranchInfo, thenCode)
	elseCodeLabeled = appendInstrSeqs(falseBranchInfo, elseCode)

	thenElseSeq = parallelInstrSeqs(thenCodeLabeled, elseCodeLabeled)
	testGotosThenElseSeq = appendInstrSeqs(testGotoSeq, thenElseSeq, afterIfInfo)

	preserved = [env, cont]
	return preserving(preserved, testCode, testGotosThenElseSeq)


def compSeq(seq, target, linkage):
	first = firstExp(seq)
	if isLastExp(seq):
		return compileDisp(first, target, linkage)
	else:
		compFirst = compileDisp(first, target, nex)
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

	label = labelInfo(funcEntry) 
	assignFuncEnv = "env = COMPENVOBJ(func);"
	parseParams = 'unev = parse("%(lispParams)s\\n");' % locals()
	extendFuncEnv = "env = extendEnv(unev, arglist, env);" # %(params)s ?

	instr = joinInstrsNewlines(label, assignFuncEnv, 
					parseParams, extendFuncEnv)

	instrSeq = makeInstrSeq([env, func, arglist], 
								[env], [instr])
	bodySeq = compSeq(lambdaBody(expr), val, ret)
	appended = appendInstrSeqs(instrSeq, bodySeq)

	return appended


def compApp(expr, target=val, linkage=nex):
	function = operator(expr)
	arguments = operands(expr)
	funcCode = compileDisp(function, target=func)
	argCodes = list(map(
					(lambda arg: 
						compileDisp(arg)),
					arguments))

	argListCode = constructArglist(argCodes)
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
	instr = "arglist = LISTOBJ(makeList(val, NULL));"
	instrSeq = makeInstrSeq([val], [arglist], 
										[instr])
	lastArg = argCodes[0]
	codeToGetLastArg = appendInstrSeqs(lastArg, 
										instrSeq)

	restArgs = argCodes[1:]
	if len(restArgs) == 0:
		return codeToGetLastArg
	else:
		return preserving([env], codeToGetLastArg,
					codeToGetRestArgs(restArgs))


def codeToGetRestArgs(argCodes):
	nextArg = argCodes[0]
	instr = "arglist = LISTOBJ(makeList(val, GETLIST(arglist)));"
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
	primBranch = makeLabel("PRIMITIVE")
	compBranch = makeLabel("COMPILED")
	afterCall = makeLabel("AFTER_CALL")
	compLink = afterCall if linkage == nex else linkage

	primBranchInfo = labelInfo(primBranch)
	compBranchInfo = labelInfo(compBranch)
	afterCallInfo = labelInfo(afterCall)

	test = "if (isPrimitive(func)) "
	gotoPrim = "goto %(primBranch)s;" % locals()
	testGotoPrim = test + gotoPrim
	testPrimSeq = makeInstrSeq([func], [], 
							[testGotoPrim])

	applyPrim = "%(target)s = applyPrimitive(func, arglist);" % locals()
	applyPrimSeq = makeInstrSeq([func, arglist],
					[target], [applyPrim])
	
	compLink = compFuncApp(target, compLink)
	primLink = endWithLink(linkage, applyPrimSeq)

	compLabeled = appendInstrSeqs(compBranchInfo, compLink)
	primLabeled = appendInstrSeqs(primBranchInfo, primLink)
	compPrimSeqs = parallelInstrSeqs(compLabeled, primLabeled)

	return appendInstrSeqs(testPrimSeq, 
				compPrimSeqs, afterCallInfo)


def compFuncApp(target, linkage):
	valTarg = target == val
	retLink = linkage == ret

	if valTarg and not retLink:
		assignCont = "cont = LABELOBJ(_%(linkage)s);" % locals()
		assignVal = "val = COMPLABOBJ(func);"
		gotoVal = "goto COMP_LABEL;"
		instr = joinInstrsNewlines(assignCont,
					assignVal, gotoVal)
		return makeInstrSeq([func], allRegs, [instr])

	elif not valTarg and not retLink:
		funcReturn = makeLabel('FUNC_RETURN')

		assignCont = "cont = LABELOBJ(_%(funcReturn)s)" % locals()
		assignVal = "val = COMPLABOBJ(func);"
		gotoVal = "goto COMP_LABEL;"
		# FUNC_RETURN_#:
		assignTarget = "%(target)s = val;" % locals()
		gotoLinkage = "goto COMP_LABEL;" 

		instr = joinInstrsNewlines(assignCont, assignVal,
			gotoVal, funcReturn, assignTarget, gotoLinkage)

		return makeInstrSeq([func], allRegs, [instr])

	elif valTarg and retLink:
		assignVal = "val = COMPLABOBJ(func);"
		gotoVal = "goto COMP_LABEL;"

		instr = assignVal + '\n' + gotoVal
		return makeInstrSeq([func, cont], allRegs, [instr])

	else:
		Exception('bad function call', 'compFuncApp')










