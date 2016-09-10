from parse import parse
from compileDisp import compileDisp
from instructions import statements
from keywords import *
from labels import labels


def compyle(exprSeq):
	print('\n')

	for expr in exprSeq:
		parsed = parse(expr)
		compiled = compileDisp(parsed)
		code = statements(compiled)

		for line in code:
			print(line)

	print('\n\ntypedef enum {')
	for label in labels:
		print('\t_' + label + ',')
	print('}')

	print("\n\nCOMP_LABEL:\n")
	for label in labels:
		print('\tif (GETLABEL(val) == _' + label + ')')
		print('\t\tgoto ' + label + ';')

	print("\n\nCOMP_LABEL:\n")
	for label in labels:
		print('\tif (GETLABEL(cont) == _' + label + ')')
		print('\t\tgoto ' + label + ';')

	print('\n\nprint_label\n')
	for label in labels:
		print('case _' + label + ':')
		print('\tprintf(\"' + label + ' \");')
		print('\tbreak;')

	print('\n')



# exprSeq = [
# 	'(define x (quote + y z))', 
# 	'(define a 1)',
# 	'(define b 0)',
# 	'(define c (if (if p q r) a b))',
# 	'(define f (lambda (x) 5))'
#	'(define factorial (lambda (n) (if (= n 1) 1 (* (factorial (- n 1) n)))))'
#	'(define fib (lambda (n) (if (< n 2) n (+ (fib (- n 1)) (fib (- n 2))))))'
# ]

exprSeq = [
'(define add1 (lambda (n) (+ n 1)))',
'(add1 5)'
]

compyle(exprSeq)