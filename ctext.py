# include this?
from parse import schemify

# make these more general
# (or not; it's easy to get these mixed up)

# assignments

def assText(text):
	return lambda expr, target: text.format(target, expr)

numText = assText('{} = NUMOBJ({});')
lookupText = assText('{} = lookup(NAMEOBJ("{}"), env);')
parseText = assText('{} = parse("{}\\n");')


# stack operations

def stackText(cmd):
	return lambda reg: '{}({});'.format(cmd, reg)

saveText = stackText('save')
restoreText = stackText('restore')

# labels, branches, gotos

ifBranches = ['TRUE_BRANCH', 'FALSE_BRANCH', 'AFTER_IF']

def gotoText(label):
	return 'goto {};'.format(label)

def ifTestText(label):
	return 'if (isTrue(val)) ' + gotoText(label)

def labelDestText(label):
	return '{}: '.format(label)

infoText = lambda label: 'print_info("{}");'.format(label)

labelText = lambda label: labelDestText(label) + ' ' + infoText(label)

# lambda

makeLambdaText = assText('{} = COMPOBJ(_{}, env);')
assFuncEnvText = 'env = COMPENVOBJ(func);'

# arglist

nullArglText = 'arglist = NULLOBJ;'
consValNullText = 'arglist = CONS(val, NULLOBJ);'
consValArglText = 'arglist = CONS(val, arglist);'