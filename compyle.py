'''
compyle takes one argument, a list of Lisp strings.
Each string will get compiled to assembly-like C 
and then printed to a file called comp_code.h. THIS 
FILE WILL BE OVERWRITTEN IF IT ALREADY EXISTS.

The file is set to print the strings in library.py, 
but simpler sequences can be used. For instance, try
compyle(['(define f (lambda () 5))', '(define x (f))']).
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

''''''

# for testing
def compylePrint(exprSeq):

	for expr in exprSeq:
		parsed = parse(expr)
		compiled = compileDisp(parsed)
		code = statements(compiled)

		for line in code:
			print(line)

exprSeq = [
	# '((addn 4) 5)',
	# '(f 1 2 3 4 5 6 7 8)',
	# '(lambda (s) s)'
	'(lambda s s)'
]

# compylePrint(exprSeq)






