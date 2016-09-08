from parse import parse
from compileDisp import compileDisp
from instructions import statements
from keywords import *


def compyle(exprSeq,target=val,linkage=nex):
	print('\n')

	for expr in exprSeq:
		parsed = parse(expr)
		compiled = compileDisp(parsed,target,linkage)
		code = statements(compiled)

		for line in code:
			print(line)
			print('\n')

	print('\n')

# exprSeq = ['(define x y)', 
# 			'(define a 1)',
# 			'(define b 0)',
# 			'(if x a b)',]


exprSeq = ['(define f (lambda (x) 5))']

compyle(exprSeq)