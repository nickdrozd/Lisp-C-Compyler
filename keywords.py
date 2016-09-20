# registers
cont = 'cont'
env = 'env'
val = 'val'
func = 'func'
arglist = 'arglist'

allRegs = [cont, env, val, func, arglist]

# linkages
ret = 'return'
nex = 'next'

# primitives

primitives = [
# arithmetic operations
'_+_', '_*_', '-', '/', 
'add1', 'sub1',
# boolean operations
'=', '<', '>', 
'zero?', 'one?', 'eq?',
# type-check operations 
'null?', 'number?', 'list?',
'boolean?', 'symbol?', 
# list operations
'cons', 'car', 'cdr', 
'cadr', 'cddr', 'cdadr', 
'caddr', 'cdddr', 'cadddr', 
# I/O operations 
'read', 'display', 
'newline', 'error',
]