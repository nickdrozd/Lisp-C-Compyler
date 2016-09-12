from keywords import *

# arithmetic operations

zero_ = (
	'(define zero? '
		'(lambda (n) '
			'(= n 0)))'
)

add1 = (
	'(define add1 '
		'(lambda (n) '
			'(+ n 1)))'
)

sub1 = (
	'(define sub1 '
		'(lambda (n) '
			'(- n 1)))'
)

three_var_test = (
	'(define three_var_test '
		'(lambda (x y z)'
			'(* x (- y z))))'
)

triangular = (
	'(define triangular '
		'(lambda (n) '
			'(if (zero? n) '
				'0 '
				'(+ n (triangular (sub1 n))))))'
)

tetrahedral = (
	'(define tetrahedral '
		'(lambda (n) '
			'(if (zero? n) '
				'0 '
				'(+ (triangular n) '
					'(tetrahedral (sub1 n))))))'
)

supertetrahedral = (
	'(define supertetrahedral '
		'(lambda (n) '
			'(if (zero? n) '
				'0 '
				'(+ (tetrahedral n) '
					'(supertetrahedral (sub1 n))))))'
)

recursive_factorial = (
	'(define recursive_factorial '
		'(lambda (n) '
			'(if (zero? n) '
				'1 '
				'(* n (recursive_factorial (sub1 n))))))'
)

iterative_factorial = (
	'(define iterative_factorial '
		'(lambda (n) '
			'(define loop '
				'(lambda (count total) '
					'(if (zero? count) '
						'total '
						'(loop (sub1 count) '
							'(* total count)))))' 
			'(loop n 1)))'
)

recursive_fibonacci = (
	'(define recursive_fibonacci '
		'(lambda (n) '
			'(if (or (= n 0) '
					'(= n 1)) '
				'n '
				'(+ (recursive_fibonacci (- n 1)) '
					'(recursive_fibonacci (- n 2))))))'
)

iterative_fibonacci = (
	'(define iterative_fibonacci '
		'(lambda (n) '
			'(define loop '
				'(lambda (count a b) '
					'(if (zero? count) '
						'a '
						'(loop (sub1 count) '
							'b '
							'(+ a b))))) '
			'(loop n 0 1)))'
)

# list operations

cons = (
	'(define cons '
		'(lambda (x y)'
			'(lambda (s)'
				'(s x y))))'
)

car = (
	'(define car '
		'(lambda (p) '
			'(p (lambda (x y) '
					'x))))'
)

cdr = (
	'(define cdr '
		'(lambda (p) '
			'(p (lambda (x y) '
					'y))))'
)

nil = (
	'(define nil (quote ()))'
)

length = (
	'(define length '
		'(lambda (s) '
			'(if (null? s) '
				'0 '
				'(add1 (length (cdr s))))))'
)

# libraries

arithLib = [
	zero_, add1, sub1,
	three_var_test,
	triangular, tetrahedral, supertetrahedral, 
	recursive_factorial, iterative_factorial, 
	recursive_fibonacci, iterative_fibonacci
]

listLib = [cons, car, cdr, nil, length]

library = arithLib + listLib