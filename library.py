# list operations

nil = '''
(define nil (quote ()))
'''

list_ = '''
(define list 
	(lambda s s))
'''

length = '''
(define (length s) 
		(if (null? s) 
			0 
			(add1 (length (cdr s)))))
'''

listRef = '''
(define (list-ref items n)
	(if (zero? n)
		(car items)
		(list-ref (cdr items) (sub1 n))))
'''

append = '''
(define (append list1 list2)
	(if (null? list1)
		list2
		(cons (car list1)
			(append (cdr list1) list2))))
'''

map_ = '''
(define (map func items)
	(if (null? items)
		nil
		(cons (func (car items))
			(map func (cdr items)))))
'''

foldRight = '''
(define (fold-right comb null seq)
	(if (null? seq)
		null
		(comb (car seq)
			(fold-right comb null (cdr seq)))))
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

recursive_factorial = '''
(define (recursive_factorial_compiled n) 
	(if (zero? n) 
		1 
		(__*__ n (recursive_factorial_compiled (sub1 n)))))
'''

iterative_factorial = '''
(define (iterative_factorial_compiled n)
	(define (loop count total)
		(if (zero? count)
			total
			(loop (sub1 count)
				(__*__ total count))))
	(loop n 1))
'''

recursive_fibonacci = '''
(define (recursive_fibonacci_compiled n) 
	(if (< n 2)
		n 
		(__+__ (recursive_fibonacci_compiled (- n 1)) 
			(recursive_fibonacci_compiled (- n 2)))))
'''

iterative_fibonacci = '''
(define (iterative_fibonacci_compiled n)
	(define (loop count a b)
		(if (zero? count)
			a
			(loop (sub1 count)
				b
				(__+__ a b))))
	(loop n 0 1))
'''

factorial = '''
(define factorial iterative_factorial_compiled)
'''

fibonacci = '''
(define fibonacci iterative_fibonacci_compiled)
'''


arithLib = [
	add, mul, 
	recursive_factorial, iterative_factorial, 
	recursive_fibonacci, iterative_fibonacci,
	factorial, fibonacci
]


library = listLib + arithLib