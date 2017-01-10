#!/usr/bin/python3

'''
compyle takes one argument, a list of Lisp strings.
Each string will get compiled to assembly-like C 
and then printed. Watch the code fly by!

The file is set to print the strings in library.py, 
but simpler sequences can be used. For instance, try
compyle(['(define f (lambda () 5))', '(define x (f))']).
'''

from parse import parse
from instructions import statements
from labels import labels
from library import library
from compExp import compExp


def compyle(exprSeq):

	print('\n')

	for expr in exprSeq:
		parsed = parse(expr)
		compiled = compExp(parsed)
		code = statements(compiled)

		for line in code:
			print(line)

		print('\n')

	print('\n')


exprSeq = [
	# '5'
	# '(define x 5)',
	# '(def x 5)',
	# '(def (f x) (+ x 5))',
	# '(set! (f x) (+ x 5))',
	'(if a b c)',
	# '(and a b c)'
	# '(or a b c)',
	# '((addn 4) 5)',
	# '(f 1 2 3 4 5 6 7 8)',
	# '(lambda (x) (f x))', 
	# '((lambda (s) s) (quote (3 4 5)))',
	# '((lambda s s) 3 4 5)',
	# '(f)', 
	# '((f))',
	# '((f 4))',
]

compyle(exprSeq)
# compyle(library)







