# include this?
from parse import schemify

# make these more general
# (or not; it's easy to get these mixed up)

# assignments

def assignText(text):
	return lambda expr, target: text.format(target, expr)

numText = assignText('{} = NUMOBJ({});')
lookupText = assignText('{} = lookup(NAMEOBJ("{}"), env);')
parseText = assignText('{} = parse("{}\\n");')

# ass / def

def assDefText(cmd):
	text = cmd + '(NAMEOBJ(\"{}\"), val, env);'
	return lambda var: text.format(var)

assCmd = 'setVar'
defCmd = 'defineVar'

# stack operations

def stackText(cmd):
	return lambda reg: '{}({});'.format(cmd, reg)

saveText = stackText('save')
restoreText = stackText('restore')

# labels, branches, gotos

ifBranches = 'TRUE_BRANCH', 'FALSE_BRANCH', 'AFTER_IF'
lambdaBranches = 'ENTRY', 'AFTER_LAMBDA'


def gotoText(label):
	return 'goto {};'.format(label)

gotoContinueText = gotoText('CONTINUE')

def ifTestGotoText(label):
	return 'if (isTrue(val)) ' + gotoText(label)

def labelDestText(label):
	return '{}: '.format(label)

infoText = lambda label: 'print_info("{}");'.format(label)

branchText = lambda label: labelDestText(label) + ' ' + infoText(label)

# lambda

makeLambdaText = assignText('{} = COMPOBJ(_{}, env);')
assFuncEnvText = 'env = COMPENVOBJ(func);'

# arglist

nullArglText = 'arglist = NULLOBJ;'
consValNullText = 'arglist = CONS(val, NULLOBJ);'
consValArglText = 'arglist = CONS(val, arglist);'