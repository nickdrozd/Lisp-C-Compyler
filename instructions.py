from ctext import *

# instructions

def makeInstrSeq(needs, modifies, stmnts):
	return [set(needs), set(modifies), stmnts]

emptyInstrSeq = makeInstrSeq([],[],[])

def registersNeeded(seq):
	if type(seq) == str:
		return set()
	else:
		return seq[0]

def registersModified(seq):
	if type(seq) == str:
		return set()
	else:
		return seq[1]

def statements(seq):
	if type(seq) == str:
		return [seq]
	else:
		return seq[2]

def needsRegister(seq, reg):
	return reg in registersNeeded(seq)

def modifiesRegister(seq, reg):
	return reg in registersModified(seq)


def appendInstrSeqs(*seqs):
	def append2Seqs(seq1, seq2):
		needed1 = registersNeeded(seq1)
		needed2 = registersNeeded(seq2)
		modified1 = registersModified(seq1)
		modified2 = registersModified(seq2)

		needed = listUnion(needed1, listDiff(needed2, modified1))
		modified = listUnion(modified1, modified2)

		statements1 = statements(seq1)
		statements2 = statements(seq2)
		statementSeq = statements1 + statements2

		return makeInstrSeq(needed, modified, statementSeq)

	returnSeq = emptyInstrSeq

	for seq in seqs:
		returnSeq = append2Seqs(returnSeq, seq)

	return returnSeq


def tackOnInstrSeq(seq, bodySeq):
	needed = registersNeeded(seq)
	modified = registersModified(seq)
	statementSeq = statements(seq) + statements(bodySeq)
	return makeInstrSeq(needed, modified, statementSeq)


def parallelInstrSeqs(seq1, seq2):
	needed1 = registersNeeded(seq1)
	needed2 = registersNeeded(seq2)
	needed = listUnion(needed1, needed2)

	modified1 = registersModified(seq1)
	modified2 = registersModified(seq2)
	modified = listUnion(modified1, modified2)


	statements1 = statements(seq1)
	statements2 = statements(seq2)
	statementSeq = statements1 + statements2

	return makeInstrSeq(needed, modified, statementSeq)


def preserving(regs, seq1, seq2):
	needed = registersNeeded(seq1)
	modified = registersModified(seq2)
	stmnts = statements(seq1)
	for reg in regs:
		if needsRegister(seq2, reg) and modifiesRegister(seq1, reg):
			stmnts = [saveText(reg)] + stmnts + restoreText(reg)
			needed.add(reg)
			modified.remove(reg)	
	return makeInstrSeq(needed, modified, stmnts + statements(seq2))


def listUnion(s1, s2):
	result = []
	for i in s1:
		result += [i]
	for i in s2:
		if i not in result:
			result += [i]
	return result

def listDiff(s1, s2):
	result = []
	for i in s1:
		if i not in s2:
			result += [i]
	return result









