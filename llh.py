'''
CLASSIFIERS
'''

from keywords import *

# numbers, etc

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

def isQuote(exp):
	tag = getTag(exp)
	return tag == QUOTE_KEY

def quotedText(exp):
	return exp[1]

# assignment

def isAss(exp):
	tag = getTag(exp)
	return tag == ASS_KEY

def assVar(exp):
	return exp[1]

def assVal(exp):
	return exp[2]

# definition

def isDef(exp):
	tag = getTag(exp)
	return tag == DEF_KEY

def defVar(exp):
	return exp[1]

def defVal(exp):
	return exp[2]

# conditional

def isIf(exp):
	tag = getTag(exp)
	return tag == IF_KEY

def ifTest(exp):
	return exp[1]

def ifThen(exp):
	return exp[2]

def ifElse(exp):
	return exp[3]

# lambda abstraction

def isLambda(exp):
	tag = getTag(exp)
	return tag == LAMBDA_KEY

def lambdaParams(exp):
	return exp[1]

def lambdaBody(exp):
	return exp[2:]

# commencement

def isBegin(exp):
	tag = getTag(exp)
	return tag == BEGIN_KEY

def firstExp(seq):
	return seq[0]

def restExps(seq):
	return seq[1:]

def isLastExp(seq):
	return len(seq[1:]) == 0

# function application

def operator(exp):
	return exp[0]

def operands(exp):
	return exp[1:]









