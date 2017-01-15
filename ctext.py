# include this?
from parse import schemify
from registers import *

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
	return '{}:'.format(label)

infoText = lambda label: 'print_info("{}");'.format(label)

branchText = lambda label: labelDestText(label) + ' ' + infoText(label)

# lambda

makeLambdaText = assignText('{} = COMPOBJ(_{}, env);')

funcEnvText = 'env = COMPENVOBJ(func);'
parseParamsText = lambda params: 'unev = parse("{}\n");'.format(params)
extendEnvText = 'env = extendEnv(unev, arglist, env);'

# func call

def funcTestGotoText(test):
	return lambda label: 'if ({}(func)) '.format(test) + gotoText(label)

isPrimitiveTestText = funcTestGotoText('isPrimitive')
isCompoundTestText = funcTestGotoText('isCompound')

# arglist

nullArglText = 'arglist = NULLOBJ;'
consValNullText = 'arglist = CONS(val, NULLOBJ);'
consValArglText = 'arglist = CONS(val, arglist);'


def applyPrimText(target):
	return '{} = applyPrimitive(func, arglist);'.format(target)

# func app

def assContText(linkage):
	return 'cont = LABELOBJ(_{});'.format(linkage)

# compiled instrs
assValFuncLabelText = 'val = COMPLABOBJ(func);'
gotoValText = gotoText('COMP_LABEL')

# compound instrs
saveCont = saveText(cont)
gotoCompound = gotoText('APPLY_COMPOUND')

# not valTarg, not retLink
def valtoTargText(target):
	return '{} = val;'.format(target)
