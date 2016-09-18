# list operations

nil = '''
(define nil (quote ()))
'''

list_ = '''
(define list 
	(lambda s s))
'''

length ='''
(define length 
	(lambda (s) 
		(if (null? s) 
			0 
			(add1 (length (cdr s))))))
'''

listRef = '''
(define list-ref
	(lambda (items n)
		(if (zero? n)
			(car items)
			(list-ref (cdr items) (sub1 n)))))
'''

append = '''
(define append
	(lambda (list1 list2)
		(if (null? list1)
			list2
			(cons (car list1)
				(append (cdr list1) list2)))))
'''

map_ = '''
(define map
	(lambda (func items)
		(if (null? items)
			nil
			(cons (func (car items))
				(map func (cdr items))))))
'''

foldRight = '''
(define fold-right
	(lambda (comb null seq)
		(if (null? seq)
			null
			(comb (car seq)
				(fold-right comb null (cdr seq))))))
'''


listLib = [
nil, list_, length,
listRef, append, 
map_, foldRight, 
]

# arithmetic operations

add = '''
(define + 
	(lambda nums
		(fold-right __+__ 0 nums)))
'''

mul = '''
(define * 
	(lambda nums
		(fold-right __*__ 1 nums)))
'''

triangular = '''
(define recursive_triangular_compiled 
	(lambda (n) 
		(if (zero? n) 
			0 
			(__+__ n (recursive_triangular_compiled (sub1 n))))))
'''

tetrahedral = '''
(define recursive_tetrahedral_compiled 
	(lambda (n) 
		(if (zero? n) 
			0 
			(__+__ (recursive_triangular_compiled n) 
				(recursive_tetrahedral_compiled (sub1 n))))))
'''

supertetrahedral = '''
(define recursive_supertetrahedral_compiled 
	(lambda (n) 
		(if (zero? n) 
			0 
			(__+__ (recursive_tetrahedral_compiled n) 
				(recursive_supertetrahedral_compiled (sub1 n))))))
'''

recursive_factorial = '''
(define recursive_factorial_compiled 
	(lambda (n) 
		(if (zero? n) 
			1 
			(* n (recursive_factorial_compiled (sub1 n))))))
'''

iterative_factorial = '''
(define iterative_factorial_compiled 
	(lambda (n) 
		(define loop 
			(lambda (count total) 
				(if (zero? count) 
					total 
					(loop (sub1 count) 
						(* total count))))) 
		(loop n 1)))
'''

recursive_fibonacci = '''
(define recursive_fibonacci_compiled 
	(lambda (n) 
		(if (< n 2)
			n 
			(__+__ (recursive_fibonacci_compiled (- n 1)) 
				(recursive_fibonacci_compiled (- n 2))))))
'''

iterative_fibonacci = '''
(define iterative_fibonacci_compiled 
	(lambda (n) 
		(define loop 
			(lambda (count a b) 
				(if (zero? count) 
					a 
					(loop (sub1 count) 
						b 
						(__+__ a b))))) 
		(loop n 0 1)))
'''

factorial = '''
(define factorial iterative_factorial_compiled)
'''

fibonacci = '''
(define fibonacci iterative_fibonacci_compiled)
'''


arithLib = [
	add, mul, 
	triangular, tetrahedral, supertetrahedral, 
	recursive_factorial, iterative_factorial, 
	recursive_fibonacci, iterative_fibonacci,
	factorial, fibonacci
]




library = listLib + arithLib