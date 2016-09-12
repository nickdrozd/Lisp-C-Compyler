from keywords import *

# arithmetic operations

zero_ = (
	'(%(DEF_KEY)s zero? '
		'(%(LAMBDA_KEY)s (n) '
			'(= n 0)))'
) % locals()

add1 = (
	'(%(DEF_KEY)s add1 '
		'(%(LAMBDA_KEY)s (n) '
			'(+ n 1)))'
) % locals()

sub1 = (
	'(%(DEF_KEY)s sub1 '
		'(%(LAMBDA_KEY)s (n) '
			'(- n 1)))'
) % locals()

three_var_test = (
	'(%(DEF_KEY)s three_var_test '
		'(%(LAMBDA_KEY)s (x y z)'
			'(* x (- y z))))'
) % locals()

triangular = (
	'(%(DEF_KEY)s triangular '
		'(%(LAMBDA_KEY)s (n) '
			'(%(IF_KEY)s (zero? n) '
				'0 '
				'(+ n (triangular (sub1 n))))))'
) % locals()

tetrahedral = (
	'(%(DEF_KEY)s tetrahedral '
		'(%(LAMBDA_KEY)s (n) '
			'(%(IF_KEY)s (zero? n) '
				'0 '
				'(+ (triangular n) '
					'(tetrahedral (sub1 n))))))'
) % locals()

supertetrahedral = (
	'(%(DEF_KEY)s supertetrahedral '
		'(%(LAMBDA_KEY)s (n) '
			'(%(IF_KEY)s (zero? n) '
				'0 '
				'(+ (tetrahedral n) '
					'(supertetrahedral (sub1 n))))))'
) % locals()

recursive_factorial = (
	'(%(DEF_KEY)s recursive_factorial '
		'(%(LAMBDA_KEY)s (n) '
			'(%(IF_KEY)s (zero? n) '
				'1 '
				'(* n (recursive_factorial (sub1 n))))))'
) % locals()

iterative_factorial = (
	'(%(DEF_KEY)s iterative_factorial '
		'(%(LAMBDA_KEY)s (n) '
			'(%(DEF_KEY)s loop '
				'(%(LAMBDA_KEY)s (count total) '
					'(%(IF_KEY)s (zero? count) '
						'total '
						'(loop (sub1 count) '
							'(* total count)))))' 
			'(loop n 1)))'
) % locals()

recursive_fibonacci = (
	'(%(DEF_KEY)s recursive_fibonacci '
		'(%(LAMBDA_KEY)s (n) '
			'(%(IF_KEY)s (%(OR_KEY)s '
							'(= n 0) '
							'(= n 1)) '
				'n '
				'(+ (recursive_fibonacci (- n 1)) '
					'(recursive_fibonacci (- n 2))))))'
) % locals()

iterative_fibonacci = (
	'(%(DEF_KEY)s iterative_fibonacci '
		'(%(LAMBDA_KEY)s (n) '
			'(%(DEF_KEY)s loop '
				'(%(LAMBDA_KEY)s (count a b) '
					'(%(IF_KEY)s (zero? count) '
						'a '
						'(loop (sub1 count) '
							'b '
							'(+ a b))))) '
			'(loop n 0 1)))'
) % locals()

# list operations

cons = (
	'(%(DEF_KEY)s cons '
		'(%(LAMBDA_KEY)s (x y)'
			'(%(LAMBDA_KEY)s (s)'
				'(s x y))))'
) % locals()

car = (
	'(%(DEF_KEY)s car '
		'(%(LAMBDA_KEY)s (p) '
			'(p (%(LAMBDA_KEY)s (x y) '
					'x))))'
) % locals()

cdr = (
	'(%(DEF_KEY)s cdr '
		'(%(LAMBDA_KEY)s (p) '
			'(p (%(LAMBDA_KEY)s (x y) '
					'y))))'
) % locals()

nil = (
	'(%(DEF_KEY)s nil (%(QUOTE_KEY)s ()))'
) % locals()

length = (
	'(%(DEF_KEY)s length '
		'(%(LAMBDA_KEY)s (s) '
			'(%(IF_KEY)s (null? s) '
				'0 '
				'(add1 (length (cdr s))))))'
) % locals()

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