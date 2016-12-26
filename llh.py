''' LOW-LEVEL HELPERS '''

def isSelfEvaluating(exp):
	return isNum(exp) or isVar(exp)

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

# quotation

def quotedText(exp):
	return exp[1]

# assignment

def assVar(exp):
	return exp[1]

def assVal(exp):
	return exp[2]

# definition

def isSugarDef(exp):
	return type(exp[1]) == list

def transformSugarDef(exp):
	if not isSugarDef(exp):
		return exp
	funcArgs, body = exp[1], exp[2:]
	func, args = funcArgs[0], funcArgs[1:]
	lambdaExp = ['lambda', args] + body
	return ['define', func, lambdaExp]

def defVar(exp):
	return exp[1]

def defVal(exp):
	return exp[2]

# booleans

def ifClauses(exp):
	return exp[1:]

# lambda abstraction

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

def beginActions(exp):
	return exp[1:]

# function application

def operator(exp):
	return exp[0]

def operands(exp):
	return exp[1:]
