'''
compyle takes one argument, a list of Lisp strings.
Each string will get compiled to assembly-like C 
and then printed.

The file is set to print the strings in library.py, 
but simply sequences can be used. For instance, try
compyle(['(define f (lambda () 5))', '(define x (f))']).

TODO: figure out how to get the output into a file!
'''

from parse import parse
from compileDisp import compileDisp
from instructions import statements
from keywords import *
from labels import labels
from library import library


def compyle(exprSeq):
	print('\n')

	for expr in exprSeq:
		parsed = parse(expr)
		compiled = compileDisp(parsed)
		code = statements(compiled)

		for line in code:
			print(line)

	print('\n')

compyle(library)



""" SAVE THIS """

# def compyle(exprSeq):
# 	print('\n')

# 	# print('#define COMPILED_CODE_BODY \\')
# 	for expr in exprSeq:
# 		parsed = parse(expr)
# 		compiled = compileDisp(parsed)
# 		code = statements(compiled)

# 		for line in code:
# 			print(line)

	# print('goto DONE;')

	# labelsLen = len(labels)
	# print('#define ALL_COMPILED_LABELS \\')
	# for label in labels:
	# 	if labels.index(label) == labelsLen - 1:
	# 		print('_' + label)
	# 	else:
	# 		print('_' + label + ',' + ' \\')

	# for label in labels:
	# 	print('\t_' + label + ', ')

	# for label in labels:
	# 	print('if (GETLABEL(REG) == _' + label + ')' + ' \\')
	# 	print('goto ' + label + ';' + ' \\')

	# print("\n\nCOMP_LABEL:\n")
	# for label in labels:
	# 	print('\t\tif (GETLABEL(val) == _' + label + ')')
	# 	print('\t\t\tgoto ' + label + ';')

	# print("\n\nCONTINUE:\n")
	# print('// compiler labels')
	# for label in labels:
	# 	print('\t\tif (GETLABEL(cont) == _' + label + ')')
	# 	print('\t\t\tgoto ' + label + ';')

	# print('\n\nprint_label\n')
	# for label in labels:
	# 	print('case _' + label + ':')
	# 	print('\tprintf(\"' + label + ' \");')
	# 	print('\tbreak;')

	# print('\n')



