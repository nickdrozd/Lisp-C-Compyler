# include this?
from parse import schemify

# make these more general

# or not; it's easy to get these backwards

assText = lambda instr: lambda expr, reg: instr.format(reg, expr)

numText = assText('{} = NUMOBJ({});')
varText = assText('{} = lookup(NAMEOBJ("{}"), env);')
quoteText = assText('{} = parse("{}\\n");')


svRstText = lambda cmd: lambda reg: '{}({});'.format(cmd, reg) 

saveText = svRstText('save')
restoreText = svRstText('restore')


gotoText = lambda label: 'goto %s;' % label

ifTestText = lambda label: 'if (isTrue(val)) ' + gotoText(label)