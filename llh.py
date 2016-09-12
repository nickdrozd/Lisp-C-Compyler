'''
CLASSIFIERS
'''

from keywords import *

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
	return hasForm(exp, QUOTE_KEY)

def quotedText(exp):
	return exp[1]

# assignment

def isAss(exp):
	return hasForm(exp, ASS_KEY)

def assVar(exp):
	return exp[1]

def assVal(exp):
	return exp[2]

# definition

def isDef(exp):
	return hasForm(exp, DEF_KEY)

def defVar(exp):
	return exp[1]

def defVal(exp):
	return exp[2]

# booleans

def isIf(exp):
	return hasForm(exp, IF_KEY)

def ifTest(exp):
	return exp[1]

def ifThen(exp):
	return exp[2]

def ifElse(exp):
	return exp[3]

def isOr(exp):
	return hasForm(exp, OR_KEY)

def transformOr(expr):
	if len(expr[1:]) == 0:
		return 0
	else:
		first = expr[1]
		rest = transformOr([OR_KEY] + expr[2:])
		return [IF_KEY, first, 1, rest]

# lambda abstraction

def isLambda(exp):
	return hasForm(exp, LAMBDA_KEY)

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
	return hasForm(exp, BEGIN_KEY)

# function application

def operator(exp):
	return exp[0]

def operands(exp):
	return exp[1:]











