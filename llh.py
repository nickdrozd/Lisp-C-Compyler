''' LOW-LEVEL HELPERS '''

# numbers

def isNum(exp):
	try:
		return type(int(exp)) == int
	except:
		return False

# variables

def isVar(exp):
	return type(exp) == str

# classifier helper

def getTag(exp):
	return exp[0]

def hasForm(exp, form):
	return getTag(exp) == form

# quotation

def isQuote(exp):
	return hasForm(exp, 'quote')

def quotedText(exp):
	return exp[1]

# assignment

def isAss(exp):
	return hasForm(exp, 'set!')

def assVar(exp):
	return exp[1]

def assVal(exp):
	return exp[2]

# definition

def isDef(exp):
	return hasForm(exp, 'define')

def isSugarDef(exp):
	return type(exp[1]) == list

def transformSugarDef(exp):
	funcArgs = exp[1]
	func = funcArgs[0]
	args = funcArgs[1:]
	body = exp[2:]
	lambdaExp = ['lambda', args] + body
	return ['define', func, lambdaExp]

def defVar(exp):
	return exp[1]

def defVal(exp):
	return exp[2]

# booleans

def isIf(exp):
	return hasForm(exp, 'if')

def ifTest(exp):
	return exp[1]

def ifThen(exp):
	return exp[2]

def ifElse(exp):
	return exp[3]

def isOr(exp):
	return hasForm(exp, 'or')

def transformOr(expr):
	if len(expr[1:]) == 0:
		return 0
	else:
		first = expr[1]
		rest = transformOr(['or'] + expr[2:])
		return ['if', first, 1, rest]

# lambda abstraction

def isLambda(exp):
	return hasForm(exp, 'lambda')

def lambdaParams(exp):
	return exp[1]

def lambdaBody(exp):
	return exp[2:]

# sequence

def firstExp(seq):
	return seq[0]

def restExps(seq):
	return seq[1:]

def isLastExp(seq):
	return len(seq[1:]) == 0

def isBegin(exp):
	return hasForm(exp, 'begin')

def beginActions(exp):
	return exp[1:]

# function application

def operator(exp):
	return exp[0]

def operands(exp):
	return exp[1:]











