# include this?
from parse import schemify

# make these more general
# (or not; it's easy to get these mixed up)

# assignments

assText = lambda instr: lambda expr, reg: instr.format(reg, expr)

numText = assText('{} = NUMOBJ({});')
varText = assText('{} = lookup(NAMEOBJ("{}"), env);')
quoteText = assText('{} = parse("{}\\n");')
lambdaText = assText('{} = COMPOBJ(_{}, env);'

# stack operations

stackText = lambda cmd: lambda reg: '{}({});'.format(cmd, reg) 

saveText = stackText('save')
restoreText = stackText('restore')

# labels, branches, gotos

gotoText = lambda label: 'goto {};'.format(label)

ifTestText = lambda label: 'if (isTrue(val)) ' + gotoText(label)

labelDestText = lambda label: '{}: '.format(label)
infoText = lambda label: 'print_info("{}");'.format(label)

labelText = lambda label: labelDestText(label) + ' ' + infoText(label)


