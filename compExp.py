'''
TODO:
	* documentation
'''

from parse import parse

from registers import *
from keywords import *

from linkage import *

from macros import transformMacros

#----------------------------------#

def compExp(expr, target=val, linkage=nex):
	expr = transformMacros(expr)

	compFunc = getCompFunc(expr)

	return compFunc(expr, target, linkage)

#----------------------------------#

from compFuncs import *

def getCompFunc(expr):
	if isVar(expr):
		return compVar

	if isNum(expr):
		return compNum

	# else
	tag, *_ = expr

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

def isNum(exp):
	try:
		return type(int(exp)) == int
	except:
		return False

def isVar(exp):
	return type(exp) == str
