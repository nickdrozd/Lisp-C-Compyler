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

triangular = (
	'(define recursive_triangular_compiled '
		'(lambda (n) '
			'(if (zero? n) '
				'0 '
				'(+ n (recursive_triangular_compiled (sub1 n))))))'
)

tetrahedral = (
	'(define recursive_tetrahedral_compiled '
		'(lambda (n) '
			'(if (zero? n) '
				'0 '
				'(+ (recursive_triangular_compiled n) '
					'(recursive_tetrahedral_compiled (sub1 n))))))'
)

supertetrahedral = (
	'(define recursive_supertetrahedral_compiled '
		'(lambda (n) '
			'(if (zero? n) '
				'0 '
				'(+ (recursive_tetrahedral_compiled n) '
					'(recursive_supertetrahedral_compiled (sub1 n))))))'
)

recursive_factorial = (
	'(define recursive_factorial_compiled '
		'(lambda (n) '
			'(if (zero? n) '
				'1 '
				'(* n (recursive_factorial_compiled (sub1 n))))))'
)

iterative_factorial = (
	'(define iterative_factorial_compiled '
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
	'(define recursive_fibonacci_compiled '
		'(lambda (n) '
			'(if (or (= n 0) '
					'(= n 1)) '
				'n '
				'(+ (recursive_fibonacci_compiled (- n 1)) '
					'(recursive_fibonacci_compiled (- n 2))))))'
)

iterative_fibonacci = (
	'(define iterative_fibonacci_compiled '
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

factorial = (
	'(define factorial iterative_factorial_compiled)'
)

fibonacci = (
	'(define fibonacci iterative_fibonacci_compiled)'
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
	triangular, tetrahedral, supertetrahedral, 
	recursive_factorial, iterative_factorial, 
	recursive_fibonacci, iterative_fibonacci,
	factorial, fibonacci
]

listLib = [cons, car, cdr, nil, length]

library = arithLib + listLib