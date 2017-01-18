'''
TODO:
	* documentation
	* generic instruction generator?
	* instrSeq class
	* rename 'infos'
	* move out keyword_groups (how?)
'''

from parse import parse

from registers import *
from keywords import *

from linkage import *

from macros import transformMacros

#----------------------------------#

def compExp(expr, target=val, linkage=nex):
	expr = transformMacros(expr)

	if isSelfEvaluating(expr):
		compType = compVar if isVar(expr) else compNum
	else:
		tag, *_ = expr
		compType = getCompFunc(tag)

	return compType(expr, target, linkage)

#----------------------------------#

from compFuncs import *

def getCompFunc(tag):
	keyword_groups = {
		define_keys : compDef, 
		ass_keys : compAss, 
		lambda_keys : compLambda, 
		if_keys : compIf, 
		begin_keys : compBegin, 
		quote_keys : compQuote
	}

	for group in keyword_groups:
		if tag in group:
			return keyword_groups[group]

	# default
	return compApp

#----------------------------------#

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
