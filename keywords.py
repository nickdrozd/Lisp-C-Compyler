DEFINE_KEYS = 'define', 'def'

ASS_KEYS = 'set!', 'ass!'

LAMBDA_KEYS = 'lambda', 'λ', 'fun'

IF_KEYS = ('if',)

BEGIN_KEYS = 'begin', 'progn'

QUOTE_KEYS = ('quote',)

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

def is_primitive(function_name):
    return function_name in PRIMITIVES
