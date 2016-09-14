'''
compyle takes one argument, a list of Lisp strings.
Each string will get compiled to assembly-like C 
and then printed to a file called comp_code.h. THIS 
FILE WILL BE OVERWRITTEN IF IT ALREADY EXISTS.

The file is set to print the strings in library.py, 
but simpler sequences can be used. For instance, try
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
	comp_code = open('comp_code.h', 'w')

	heading = (
'''/* 
	This code is compiler-generated! 
	It may be ugly, but it sure is fast!
	Can you figure out how it works?
	
	https://github.com/nickdrozd/Lisp-C-Compyler
*/

#ifndef COMP_CODE_GUARD
#define COMP_CODE_GUARD

#define COMPILED_CODE_BODY \\
''')

	comp_code.write(heading)
	for expr in exprSeq:
		parsed = parse(expr)
		compiled = compileDisp(parsed)
		code = statements(compiled)

		for line in code:
			lineSlash = line.replace(';','; \\').replace(':',': \\') + '\n'
			comp_code.write(lineSlash)
	comp_code.write('goto DONE;')
	
	comp_code.write('\n\n')

	def isLastLabel(label):
		labelsLen = len(labels)
		labelIndex = labels.index(label)
		return labelIndex == labelsLen - 1

	comp_code.write('#define COMP_CONT(REG) \\' + '\n')
	for label in labels:
		lastLabel = isLastLabel(label)
		labelCheck = (
			'if (GETLABEL(REG) == _' + label + 
			') ' + 'goto ' + label + ';' +
			('' if lastLabel else ' \\' + '\n')
		)
		comp_code.write(labelCheck)

	comp_code.write('\n\n')

	comp_code.write('#define ALL_COMPILED_LABELS \\' + '\n')
	for label in labels:
		lastLabel = isLastLabel(label)
		listedLabel = (
			'_' + label + 
			('' if lastLabel else ', \\' + '\n')
		)
		comp_code.write(listedLabel)

	comp_code.write('\n\n' + '#endif' + '\n')



compyle(library)
# compyle(['((addn 4) 5)'])
# compyle(['(f 1 2 3 4 5 6 7 8)'])



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



