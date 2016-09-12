from parse import parse
from compileDisp import compileDisp
from instructions import statements
from keywords import *
from labels import labels
from library import library


def compyle(exprSeq):
	print('\n')

	# print("COMPILED_CODE:")
	for expr in exprSeq:
		parsed = parse(expr)
		compiled = compileDisp(parsed)
		code = statements(compiled)

		for line in code:
			print('\t\t' + line)
	print('goto DONE;')

	# print('// compiler labels')
	# for label in labels:
	# 	print('\t_' + label + ',')

	# print("\n\nCOMP_LABEL:\n")
	# for label in labels:
	# 	print('\tif (GETLABEL(val) == _' + label + ')')
	# 	print('\t\tgoto ' + label + ';')

	# print("\n\nCONTINUE:\n")
	# print('// compiler labels')
	# for label in labels:
	# 	print('\tif (GETLABEL(cont) == _' + label + ')')
	# 	print('\t\tgoto ' + label + ';')

	# print('\n\nprint_label\n')
	# for label in labels:
	# 	print('case _' + label + ':')
	# 	print('\tprintf(\"' + label + ' \");')
	# 	print('\tbreak;')

	print('\n')


compyle(library)

exprSeq = [
# 	'(define x (quote + y z))', 
# 	'(define a 1)',
# 	'(define b 0)',
# 	'(define c (if (if p q r) a b))',
# 	'(define f (lambda (x) 5))'
	'(define factorial (lambda (n) (if (= n 1) 1 (* (factorial (- n 1) n)))))'
# 	'(define fib (lambda (n) (if (< n 2) n (+ (fib (- n 1)) (fib (- n 2))))))'
]

# exprSeq = [
# '(define add1 (lambda (n) (+ n 1)))',
# '(add1 (add1 5))'
# ]

# compyle(exprSeq)

# from compileDisp import compSeq
# from library import *

# x = [parse(iterative_fibonacci)]

# s = statements(compSeq(x, val, nex))

# for i in s:
# 	print(i)