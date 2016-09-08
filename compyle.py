from parse import parse
from compileDisp import compileDisp
from instructions import statements
from keywords import *


def compyle(exprSeq):
	print('\n')

	for expr in exprSeq:
		parsed = parse(expr)
		compiled = compileDisp(parsed)
		code = statements(compiled)

		for line in code:
			print(line)
			print('\n')

	print('\n')



# exprSeq = [
# 	'(define x (quote + y z))', 
# 	'(define a 1)',
# 	'(define b 0)',
# 	'(define c (if (if p q r) a b))',
# 	'(define f (lambda (x) 5))'
# ]


exprSeq = ['(f 5 6)']

compyle(exprSeq)