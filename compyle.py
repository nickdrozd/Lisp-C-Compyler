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
from labels import labels
from library import library
from compExp import compExp
from registers import *
from linkage import *


def compyle(exprSeq):

	print()

	target = val
	linkage = nex

	for expr in exprSeq:
		print(expr, target, linkage, '\n')
		parsed = parse(expr)
		compiled = compExp(parsed, target, linkage)
		code = compiled.statements

		for line in code:
			print(line)

		print()

	print()


exprSeq = [
	# '5'
	# '(define x 5)',
	# '(def x 5)',
	# '(def (f x) (+ x 5))',
	# '(set! (f x) (+ x 5))',
	# '(if a b c)',
	# '(and a b c)'
	# '(or a b c)',
	# '((addn 4) 5)',
	# '(lambda (x) x)', 
	# '(lambda (x) (f x))', 
	# '((lambda (s) s) (quote (3 4 5)))',
	# '((lambda s s) 3 4 5)',
	# '(if a (lambda (x) b) 5)',
	# '(f)', 
	# '(f 4)',
	'(f 1 2 3 4 5 6 7 8)',
	# '(f (g a) b)',
	# '((f))',
	# '((f 4))',
	# '(- a b)',
	# '(begin (define f -) (f a b))',
]

compyle(exprSeq)
# compyle(library)







