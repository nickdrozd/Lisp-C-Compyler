from llh import getTag # needed?

def transformOr(exp):
	if len(exp[1:]) == 0:
		return 0
	else:
		first = exp[1]
		rest = transformOr(['or'] + exp[2:])
		return ['if', first, 1, rest]

def transformCond(exp):
	condPairs = exp[1:]
	if len(condPairs) == 0:
		return '0'

	firstPair, restPairs = condPairs[0], condPairs[1:]

	condition = firstPair[0]
	consequence = ['begin'] + firstPair[1:]

	if condition == 'else':
		return consequence

	restTransformed = transformCond(['cond'] + restPairs)

	transformed = ['if', condition, consequence, restTransformed]

	return transformed

def transformLet(exp):
	bindings, body = exp[1], exp[2:]

	variables = [binding[0] for binding in bindings]
	values = [binding[1] for binding in bindings]

	lambdaExp = ['lambda', variables] + body

	return [lambdaExp] + values


macro_transformers = {
	'let' : transformLet,
	'cond' : transformCond,
	'or' : transformOr,
	# 'and' : transformAnd,
	# 'delay' : transformDelay,
}

macro_keys = macro_transformers.keys()

def isMacro(expr):
	try:
		return getTag(expr) in macro_keys
	except:
		return False

def transformMacro(expr):
	return macro_transformers[getTag(expr)](expr)

def transformMacros(expr):
	while isMacro(expr):
		expr = transformMacro(expr)

	return expr