# instructions


class InstrSeq:
    def __init__(self, needed, modified, stmts):
        self.needed = needed
        self.modified = modified
        self.stmts = stmts

    def needs(self, reg):
        return reg in self.needed

    def modifies(self, reg):
        return reg in self.modified


def appendInstrSeqs(*seqs):
    needed, modified, stmts = [], [], []

    for seq in seqs:
        if isinstance(seq, str):
            seq = InstrSeq([], [], [seq])

        needed = listUnion(
            needed,
            listDiff(
                seq.needed,
                modified))

        modified = listUnion(
            modified,
            seq.modified)

        stmts += seq.stmts

    return InstrSeq(needed, modified, stmts)


def tackOnInstrSeq(seq, bodySeq):
    return InstrSeq(
        seq.needed,
        seq.modified,
        seq.stmts + bodySeq.stmts)


def parallelInstrSeqs(seq1, seq2):
    return InstrSeq(
        listUnion(seq1.needed, seq2.needed),
        listUnion(seq1.modified, seq2.modified),
        seq1.stmts + seq2.stmts)


def preserving(regs, seq1, seq2):
    needed, modified, stmts = seq1.needed, seq1.modified, seq1.stmts

    for reg in regs:
        if seq2.needs(reg) and seq1.modifies(reg):
            needed = listUnion([reg], needed)
            modified = listDiff(modified, [reg])
            stmts = [f"save({reg});"] + stmts + [f"restore({reg});"]

    return appendInstrSeqs(
        InstrSeq(needed, modified, stmts),
        seq2)


def listUnion(s1, s2):
    return s1 + [
        s
        for s in s2
        if s not in s1
    ]


def listDiff(s1, s2):
    return [
        s
        for s in s1
        if s not in s2
    ]
