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
'_+_', '_*_', '-', '/', 
'add1', 'sub1',
'=', '<', '>', 
'zero?', 'one?', 'eq?', 
'cons', 'car', 'cdr', 
'cadr', 'cddr', 'cdadr', 
'caddr', 'cdddr', 'cadddr',  
'read', 'display', 'error',
]