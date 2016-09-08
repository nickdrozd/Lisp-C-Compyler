# TODO: default args to comp funcs (target=val and linkage=nex) ???

# TODO: figure out which funcs are needed
from keywords import *
from instructions import *
from labels import makeLabel
from llh import *
from parse import schemify


def compileDisp(expr, target=val, linkage=nex):
	if isNum(expr):
		return compNum(expr, target, linkage)
	elif isVar(expr):
		return compVar(expr, target, linkage)
	elif isQuote(expr):
		return compQuote(expr, target, linkage)
	elif isAss(expr):
		return compAss(expr, target, linkage)
	elif isDef(expr):
		return compDef(expr, target, linkage)
	elif isIf(expr):
		return compIf(expr, target, linkage)
	elif isLambda(expr):
		return compLambda(expr, target, linkage)
	elif isBegin(expr):
		return compBegin(expr, target, linkage)
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


# expr reg isn't used. figure out how to get 
# these expressions to Obj form

def compNum(expr, target, linkage):
	instr = "%(target)s = NUMOBJ(%(expr)s);" % locals()
	instrSeq = makeInstrSeq([], [target], [instr])
	return endWithLink(linkage, instrSeq)

# TODO
def compQuote(expr, target, linkage):
	text = quotedText(expr)
	lispText = schemify(text)

	parseText = 'unev = parse("%(lispText)s\\n");' % locals()
	assignText = "%(target)s = unev;" % locals()

	instr = parseText + '\n' + assignText
	instrSeq = makeInstrSeq([], [target], [instr])
	return endWithLink(linkage, instrSeq)

def compVar(expr, target, linkage):
	instr = "%(target)s = lookup(%(expr)s, env);" % locals()
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
		instr = CFunc + "(%(var)s, val, env);" % locals()
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
	afterIf = makeLabel('AFTER_IF') + ':'
	thenLink = afterIf if linkage == nex else linkage

	testCode = compileDisp(ifTest(expr), val, nex)
	thenCode = compileDisp(ifThen(expr), target, thenLink)
	# fallthrough after false branch?
	elseCode = compileDisp(ifElse(expr), target, linkage)

	isTrueInstr = "if (isTrue(val)) " + '\n'
	gotoTrueInstr = "\tgoto %(trueBranch)s;" % locals() + '\n'
	gotoFalseInstr = "goto %(falseBranch)s;" % locals()
	testGotoInstr = isTrueInstr + gotoTrueInstr + gotoFalseInstr
	testGotoSeq = makeInstrSeq([val], [], [testGotoInstr])

	thenCodeLabeled = appendInstrSeqs(trueBranch + ':', thenCode)
	elseCodeLabeled = appendInstrSeqs(falseBranch + ':', elseCode)

	thenElseSeq = parallelInstrSeqs(thenCodeLabeled, elseCodeLabeled)
	testGotosThenElseSeq = appendInstrSeqs(testGotoSeq, thenElseSeq, afterIf)

	preserved = [env, cont]
	return preserving(preserved, testCode, testGotosThenElseSeq)


def compSeq(seq, target, linkage):
	first = firstExp(seq)
	if isLastExp(seq):
		return compileDisp(first, target, linkage)
	else:
		compFirst = compileDisp(first, target, nex)
		rest = restExps(seq)
		compRest = compileDisp(rest, target, linkage)
		preserved = [env, cont]
		return preserving(preserved, compFirst, compRest)


def compLambda(expr, target=val, linkage=nex):
	funcEntry = makeLabel('ENTRY')
	afterLambda = makeLabel('AFTER_LAMBDA')

	lambdaLink = afterLambda if linkage == nex else linkage
	lambdaBody = compLambdaBody(expr, funcEntry)
	
	instr = "%(target)s = makeCompFunc(%(funcEntry)s, env)" % locals()
	instrSeq = makeInstrSeq([env], [target], [instr])

	instrLinked = endWithLink(lambdaLink, instrSeq)
	tackedOn = tackOnInstrSeq(instrLinked, lambdaBody)
	appended = appendInstrSeqs(tackedOn, afterLambda + ':')

	return appended

def compLambdaBody(expr, funcEntry):
	params = lambdaParams(expr)
	lispParams = schemify(params)

	label = "%(funcEntry)s:" % locals() # might turn out redundant
	assignFuncEnv = "env = compiledFuncEnv(func);"
	parseParams = 'unev = parse("%(lispParams)s\\n");' % locals()
	extendFuncEnv = "env = extendEnv(unev, arglist, env);" # %(params)s ?

	def labelInstrs(label, *instrs):
		totalInstr = label
		for instr in instrs:
			totalInstr += '\n\t' + instr
		return totalInstr

	# instr = label + '\n\t' + assignFuncEnv + '\n\t' + parseParams + '\n\t' + extendFuncEnv

	instr = labelInstrs(label, assignFuncEnv, 
						parseParams, extendFuncEnv)

	instrSeq = [[env, func, arglist], [env], [instr]]
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
	return emptyInstrSeq





def codeToGetRestArgs(argCodes):
	return emptyInstrSeq







def compFuncCall(target, linkage):
	return emptyInstrSeq






def compFuncApp(target, linkage):
	valTarg = target == val
	retLink = linkage == ret

	if valTarg and not retLink:
		pass


	elif not valTarg and not retLink:
		pass


	elif valTarg and retLink:
		pass




	else:
		pass














