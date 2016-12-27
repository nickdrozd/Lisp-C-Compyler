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
