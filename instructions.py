from ctext import *
from registers import *


class InstrSeq:
	def __str__(self):
		return '\n'.join([str(type(self))] + self.statements)

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
		self.modified.discard(reg)
		self.statements = (
			[saveText(reg)] + 
			self.statements + 
			[restoreText(reg)]
		)

	def endWithLink(self, linkage):
		return preserving([cont], 
				self, 
				LinkageSeq(linkage))

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
		seq1.modified, 
		seq1.statements)

	for reg in regs:
		if seq2.needs(reg) and seq1.modifies(reg):
			returnSeq.preserve(reg)

	return appendInstrSeqs(
			returnSeq, 
			seq2)

###

def EmptySeq():
	return InstrSeq()

def GotoContSeq():
	return InstrSeq([cont], [], [gotoContinueText])

def GotoLinkageSeq(linkage):
	return InstrSeq([], [], [gotoText(linkage)])

def LinkageSeq(linkage):
	seqs = {
		ret : GotoContSeq, 
		nex : EmptySeq
	}

	try:
		return seqs[linkage]()
	except:
		return GotoLinkageSeq(linkage)




# from instrseqs import LinkageSeq


# def endWithLink(linkage, instrSeq):
# 	return preserving([cont], 
# 			instrSeq, 
# 			LinkageSeq(linkage))