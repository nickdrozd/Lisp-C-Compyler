'''
TODO:
	* documentation
	* generic instruction generator?
	* instrSeq class
	* remove llh?
	* rename 'infos'
	* move out keyword_groups (how?)
'''

from parse import parse # delete this

from registers import *
from keywords import *
from primitives import primitives

from instructions import *
from instrseqs import *
from linkage import *

from labels import *
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
	return NumSeq(expr, target, linkage)

def compVar(expr, target, linkage):
	return VarSeq(expr, target, linkage)

def compQuote(expr, target, linkage):
	_, text = expr
	lispText = schemify(text)
	return QuoteSeq(lispText, target, linkage)

def compAssDef(seqType):
	def isSugarDef(exp):
		# list? tuple? something more general?
		return type(exp[1]) == list

	def transformSugarDef(exp):
		if not isSugarDef(exp):
			return exp
		_, funcArgs, *body = exp
		func, *args = funcArgs
		lambdaExp = ['lambda', args] + body
		return ['define', func, lambdaExp]

	def comp(expr, target, linkage):
		expr = transformSugarDef(expr)

		_, variable, value = expr
		valueCode = compExp(value, val, nex)

		return seqType(variable, valCode, target, linkage)

	return comp

compAss = compAssDef(AssSeq)
compDef = compAssDef(DefSeq)

def compIf(expr, target=val, linkage=nex):
	# it would be nice to push these into IfInstr, 
	# but afterIf is needed for compiledCode (thenLink)
	labels = makeIfLabels()
	print(labels)
	trueBranch, falseBranch, afterIf = labels
	thenLink = afterIf if linkage == nex else linkage

	_, ifTest, ifThen, ifElse = expr

	compiledCode = [
		compExp(exp, targ, link) for 
			(exp, targ, link) in [
				(ifTest, val, nex), 
				(ifThen, target, linkage), 
				(ifElse, target, thenLink)
			]
	]

	return IfSeq(compiledCode, labels)

def compBegin(expr, target=val, linkage=nex):
	_, *seq = expr
	return compSeq(seq, target, linkage)

def compSeq(seq, target=val, linkage=nex):
	returnSeq = InstrSeq()
	regs = [env, cont]
	for exp in reversed(seq):
		comp = compExp(exp, target, linkage)
		returnSeq.preserving(regs, comp)
	return returnSeq

def compLambda(expr, target=val, linkage=nex):
	_, params, *body = expr
	lispParams = schemify(params)

	bodySeq = compSeq(body, val, ret)
	print('type:', type(bodySeq))

	return LambdaSeq(target, linkage, lispParams, bodySeq)





def compApp(expr, target=val, linkage=nex):
	function, *arguments = expr

	funcCode = compExp(function, target=func)
		
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

	if not argCodes:
		instr = "arglist = NULLOBJ;"
		return makeInstrSeq([], [arglist], [instr])

	# else:
	instr = "arglist = CONS(val, NULLOBJ);"
	instrSeq = makeInstrSeq([val], [arglist], [instr])

	lastArg, *restArgs = argCodes

	codeToGetLastArg = appendInstrSeqs(lastArg, instrSeq)

	if not restArgs:
		return codeToGetLastArg
	else:
		return preserving([env], codeToGetLastArg,
					codeToGetRestArgs(restArgs))


def codeToGetRestArgs(argCodes):
	nextArg, *restArgs = argCodes
	instr = "arglist = CONS(val, arglist);"
	instrSeq = makeInstrSeq([val, arglist], 
					[arglist], [instr])
	codeForNextArg = preserving([arglist], 
							nextArg, instrSeq)

	if not restArgs:
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


def compFuncApp(target, linkage, funcType):
	"funcType as string: 'compiled' or 'compound'"
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

