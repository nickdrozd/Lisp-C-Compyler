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
