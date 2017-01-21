import unittest

from parse import parse

from compExp import compExp
from instructions import *
from instrseqs import *

from registers import *

class TestCompyler(unittest.TestCase):
	def test_unreachable_code(self):
		"Verifies that only labels come directly after gotos"
		expr = '''
				(define (iterative_fibonacci_compiled n)
					(define (loop count a b)
						(if (one? count)
							b
							(loop (sub1 count)
								b
								(_+_ a b))))
					(loop n 0 1))
				'''
		target = val
		linkage = nex
		
		parsed = parse(expr)
		compiled = compExp(parsed, target, linkage)

		needed = compiled.needed
		modified = compiled.modified
		statements = compiled.statements

		index = 0
		while index < len(statements) - 1:
			if statements[index][:4] == 'goto':
				self.assertIn('print_info', statements[index+1])
			index += 1

















if __name__ == '__main__':
	unittest.main()
