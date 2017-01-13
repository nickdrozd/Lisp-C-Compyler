from ctext import *


class InstrSeq:
	def __repr__(self):
		return '\n'.join([str(type(self))] + self.statements)

	def __init__(self, needed=(), modified=(), statements=[]):
		self.needed = set(needed)
		self.modified = set(modified)
		self.statements = statements

	def needs(self, reg):
		return reg in self.needed

	def modifies(self, reg):
		return reg in self.modified

	def preserve(self, reg):
		self.needed.add(reg)
		self.modified.remove(reg)
		self.statements = (
			[saveText(reg)] + 
			self.statements + 
			restoreText(reg)
		)


def appendInstrSeqs(*seqs):
	needed, modified, statements = set(), set(), []
	for seq in seqs:
		needed.update(seq.needed.difference(modified))
		modified.update(seq.modified)
		statements += seq.statements
	return InstrSeq(needed, modified, statements)


def tackOnInstrSeq(seq, bodySeq):
	needed = seq.needed
	modified = seq.modified
	statements = seq.statements + bodySeq.statements
	return InstrSeq(needed, modified, statements)


def parallelInstrSeqs(*seqs):
	needed, modified, statements = set(), set(), []
	for seq in seqs:
		needed.update(seq.needed)
		modified.update(seq.modified)
		statements += seq.statements
	return InstrSeq(needed, modified, statements)


def preserving(regs, seq1, seq2):
	returnSeq = InstrSeq(
		seq1.needed, 
		seq2.modified, 
		seq1.statements)
	for reg in regs:
		if seq2.needs(reg) and seq1.modifies(reg):
			returnSeq.preserve(reg)
	returnSeq.statements += seq2.statements
	return returnSeq

