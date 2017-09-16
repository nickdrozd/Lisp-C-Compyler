# primitive functions

PRIMITIVES = (
    # arithmetic operations
    '_+_', '_*_', '-', '/',
    'add1', 'sub1',
    # boolean operations
    'not', '=', '<', '>',
    'zero?', 'one?', 'eq?',
    # type-check operations
    'null?', 'number?', 'list?',
    'boolean?', 'symbol?',
    # list operations
    'cons', 'car', 'cdr',
    'set-car!', 'set-cdr!',
    'cadr', 'cddr', 'cdadr',
    'caddr', 'cdddr', 'cadddr',
    # I/O operations
    'read', 'display',
    'newline', 'error',
    # primitive application operations
    'applyNilFunc', 'applyOneFunc', 'applyTwoFunc',
)
