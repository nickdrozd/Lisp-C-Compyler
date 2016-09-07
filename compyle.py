from parse import parse
from compileDisp import compileDisp
from instructions import statements
from keywords import *


def compyle(exprSeq):
	print('\n')

	for expr in exprSeq:
		parsed = parse(expr)
		compiled = compileDisp(parsed,val,nex)
		code = statements(compiled)

		for line in code:
			print(line)
			print('\n')

	print('\n')

exprSeq = ['(define x y)', 
			'(define a 1)',
			'(define b 0)',
			'(if x a b)',
			'(define delayed_5 (lambda () 5))']


# exprSeq = ['(define delayed_5 (lambda () 5))']

compyle(exprSeq)