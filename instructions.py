from ctext import *

# instructions

class InstrSeq:
	def __init__(self, needed=[], 
					modified=[], 
					statements=[]):
		self.needed = set(needed)
		self.modified = set(modified)
		self.statements = statements

	def needs(self, reg):
		return reg in self.needed

	def modifies(self, reg):
		return reg in self.modifies

###

class SaveInstr(InstrSeq):
	def __init__(self, reg):
		super().__init__([reg], [], [saveText(reg)])

class RestoreInstr(InstrSeq):
	def __init__(self, reg):
		super().__init__([], [reg], [restoreText(reg)])

###

class NumInstr(InstrSeq):
	def __init__(self, expr, target):
		instr = numText(expr, target)
		super().__init__([], [target], [instr])

def compNum(expr, target, linkage):
	instr = "%(target)s = NUMOBJ(%(expr)s);" % locals()
	instrSeq = makeInstrSeq([], [target], [instr])
	return endWithLink(linkage, instrSeq)

###

class VarInstr(InstrSeq):
	def __init__(self, expr, target):
		instr = varText(expr, target)
		super().__init__([env], [target], [instr])

def compVar(expr, target, linkage):
	instr = "%(target)s = lookup(NAMEOBJ(\"%(expr)s\"), env);" % locals()
	instrSeq = makeInstrSeq([env], [target], [instr])
	return endWithLink(linkage, instrSeq)

###

class QuoteInstr(InstrSeq):
	def __init__(self, expr, target):
		instr = quoteText(expr, target)
		super().__init__([], [target], [instr])

def compQuote(expr, target, linkage):
	_, text = expr
	lispText = schemify(text)

	instr = 
	instrSeq = makeInstrSeq([], [target], [instr])
	return endWithLink(linkage, instrSeq)
