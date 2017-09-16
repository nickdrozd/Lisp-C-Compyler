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
    (define (loop total rest)
        (if (null? rest)
            total
            (loop (add1 total)
                (cdr rest))))
    (loop 0 s))
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

reverse = '''
(define (reverse items)
    (define (loop result rest)
        (if (null? rest)
            result
            (loop (cons (car rest)
                    result)
                (cdr rest))))
    (loop nil items))
'''

map_ = '''
(define (map func items)
    (define (loop result rest)
        (if (null? rest)
            (reverse result)
            (loop (cons (func (car rest))
                    result)
                (cdr rest))))
    (loop nil items))
'''

foldLeft = '''
(define (fold-left comb null seq)
    (define (loop result rest)
        (if (null? rest)
            result
            (loop (comb result
                    (car rest))
                (cdr rest))))
    (loop null seq))
'''


listLib = [
nil, list_, length,
listRef, append, reverse,
map_, foldLeft,
]

# arithmetic operations

add = '''
(define +
    (lambda nums
        (fold-left _+_ 0 nums)))
'''

mul = '''
(define *
    (lambda nums
        (fold-left _*_ 1 nums)))
'''

recursive_factorial = '''
(define (recursive_factorial_compiled n)
    (if (< n 2)
        1
        (_*_ n (recursive_factorial_compiled (sub1 n)))))
'''

iterative_factorial = '''
(define (iterative_factorial_compiled n)
    (define (loop count total)
        (if (< count 2)
            total
            (loop (sub1 count)
                (_*_ total count))))
    (loop n 1))
'''

recursive_fibonacci = '''
(define (recursive_fibonacci_compiled n)
    (if (< n 2)
        n
        (_+_ (recursive_fibonacci_compiled (- n 1))
            (recursive_fibonacci_compiled (- n 2)))))
'''

iterative_fibonacci = '''
(define (iterative_fibonacci_compiled n)
    (define (loop count a b)
        (if (one? count)
            b
            (loop (sub1 count)
                b
                (_+_ a b))))
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
