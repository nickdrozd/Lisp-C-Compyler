from ctext import saveText, restoreText

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

	def addNeeded(self, reg):
		self.needed.update(reg)

	def addModified(self, reg):
		self.modified.update(reg)

	def addStackInstrs(self, reg):
		self.statements = (
			saveText(reg) + 
			self.statements + 
			restoreText(reg)
		)

	def preserveReg(self, reg):
		self.addNeeded(reg)
		self.addModified(reg)
		self.addStackInstrs(reg)

	def tackOnInstr(self, seq):
		if type(seq) == str:
			statements = [seq]
		elif isinstance(seq, InstrSeq):
			statements = seq.statements
		else:
			statements = seq

		self.statements += statements


def appendInstrSeqs(*seqs):
	result = InstrSeq()
	for seq in seqs:
		result.needed.update(
			seq.needed.difference(
				result.modified))

		result.modified.update(seq.modified)

		result.statements += seq.statements
	return result

