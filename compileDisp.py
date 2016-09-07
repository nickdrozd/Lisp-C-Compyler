# TODO: newlines for code text

# TODO: figure out which funcs are needed
from keywords import *
from instructions import *
from labels import makeLabel
from llh import *


def compileDisp(expr, target, linkage):
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
	# instr = target + " = " + expr + ';'
	instr = "%(target)s = NUMOBJ(%(expr)s);" % locals()
	# instr = "%(target)s = expr;"
	instrSeq = makeInstrSeq([], [target], [instr])
	return endWithLink(linkage, instrSeq)

def compQuote(expr, target, linkage):
	# instr = target + ' = ' + quotedText(expr) + ';'
	# text = quotedText(expr)
	instr = "%(target)s = %(text)s;" % locals()
	# instr = "%(target)s = quotedText(expr);"
	instrSeq = makeInstrSeq([], [target], [instr])
	return endWithLink(linkage, instrSeq)

def compVar(expr, target, linkage):
	# instr = target + ' = ' + 'lookup(' + expr + ', env);'
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

'''
def compAss(expr, target, linkage):
	var = assVar(expr)
	valueCode = compileDisp(assVal(expr), val, nex)

	# leave assVal as return val
	instr = "setVar(%(var)s, val, env);" % locals()
	instrSeq = makeInstrSeq([env, val], [target], [instr])

	preserved = preserving([env], valueCode, instrSeq)
	return endWithLink(linkage, preserved)

def compDef(expr, target, linkage):
	var = defVar(expr)
	valueCode = compileDisp(assVal(expr), val, nex)

	# leave defVal as return val
	instr = "defineVar(%(var)s, val, env);" % locals()
	# remove target from modified? (compAss too)
	instrSeq = makeInstrSeq([env, val], [target], [instr]) 

	preserved = preserving([env], valueCode, instrSeq)
	return endWithLink(linkage, preserved)
'''

def compIf(expr, target, linkage):
	trueBranch = makeLabel('TRUE_BRANCH')
	falseBranch = makeLabel('FALSE_BRANCH')
	afterIf = makeLabel('AFTER_IF') + ':'
	thenLink = afterIf if linkage == nex else linkage

	testCode = compileDisp(ifTest(expr), val, nex)
	thenCode = compileDisp(ifThen(expr), target, thenLink)
	elseCode = compileDisp(ifElse(expr), target, linkage)

	isTrueInstr = "if (isTrue(val)) " + '\n'
	gotoTrueInstr = "\tgoto %(trueBranch)s;" % locals() + '\n'
	gotoFalseInstr = "goto %(falseBranch)s;" % locals()
	testGotoInstr = isTrueInstr + gotoTrueInstr + gotoFalseInstr
	testGotoSeq = makeInstrSeq([val], [], [testGotoInstr])

	thenCodeLabeled = appendInstrSeqs(trueBranch+':', thenCode)
	elseCodeLabeled = appendInstrSeqs(falseBranch+':', elseCode)

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


def compLambda(expr, target, linkage):
	funcEntry = makeLabel('ENTRY')
	afterLambda = makeLabel('AFTER_LAMBDA')

	lambdaLink = afterLambda if linkage == nex else linkage
	lambdaBody = compLambdaBody(expr, funcEntry)
	
	instr = "%(target)s = makeCompFunc(%(funcEntry)s, env)" % locals()
	instrSeq = makeInstrSeq([env], [target], [instr])

	endLink = endWithLink(lambdaLink, instrSeq)
	tackedOn = tackOnInstrSeq(endLink, lambdaBody)
	appended = appendInstrSeqs(tackedOn, afterLambda+':')

	return appended

def compLambdaBody(expr, funcEntry):
	# how to represent parameters?
	# params = ???
	# params = "lambdaParams(expr)"

	label = "%(funcEntry)s:" % locals() # might turn out redundant
	assignFuncEnv = "env = compiledFuncEnv(func);"
	extendFuncEnv = "env = extendEnv(params, arglist, env);" # %(params)s ?

	instr = label + '\n\t' + assignFuncEnv + '\n\t' + extendFuncEnv

	instrSeq = [[env, func, arglist], [env], [instr]]
	bodySeq = compSeq(lambdaBody(expr), val, ret)
	appended = appendInstrSeqs(instrSeq, bodySeq)

	return appended


def compApp(expr, target, linkage):
	function = operator(expr)
	arguments = operands(expr)
	funcCode = compileDisp(function, func, nex)
	argCodes = list(map(
					(lambda op: 
						compileDisp(op, val, nex)),
					operands))

	argListCode = constructArglist(argCodes)
	funcCallCode = compFuncCall(target, linkage)
	arglPresFunc = preserving([func, cont], 
						argListCode, funcCallCode)

	return preserving([env, cont], 
				funcCode, arglPresFunc)

def constructArglist(argCodes):
	pass





def codeToGetRestArgs(argCodes):
	pass







def compFuncCall(target, linkage):
	pass






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














