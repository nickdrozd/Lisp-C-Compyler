# make these more general

def CText(instr):
	return lambda expr, reg: instr.format(expr, reg)


numText = CText('{} = NUMOBJ({});')

varText = CText('{} = lookup(NAMEOBJ("{}"), env);')

quoteText = CText('{} = parse("{}\\n");')


def svRstText(cmd):
	instr = '{}({});'
	return lambda reg: CText(instr, reg)

saveText = svRstText('save')
restoreText = svRstText('restore')
