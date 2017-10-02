# instructions


class InstrSeq:
    def __init__(self, needed, modified, statements):
        self.needed = set(needed)
        self.modified = set(modified)
        self.statements = statements

    def needs_register(self, reg):
        return reg in self.needed

    def modifies_register(self, reg):
        return reg in self.modified


def registers_needed(seq):
    return set() if isinstance(seq, str) else seq.needed


def registers_modified(seq):
    return set() if isinstance(seq, str) else seq.modified


def statements(seq):
    return [seq] if isinstance(seq, str) else seq.statements


def needs_register(seq, reg):
    return reg in registers_needed(seq)


def modifies_register(seq, reg):
    return reg in registers_modified(seq)


def append_instr_seqs(*seqs):
    def append_2_seqs(seq_1, seq_2):
        needed_1 = registers_needed(seq_1)
        needed_2 = registers_needed(seq_2)
        modified_1 = registers_modified(seq_1)
        modified_2 = registers_modified(seq_2)

        needed = needed_1.union(
            needed_2.difference(
                modified_1))

        modified = modified_1.union(modified_2)

        return InstrSeq(
            needed,
            modified,
            statements(seq_1) + statements(seq_2))

    return_seq = InstrSeq([], [], [])

    for seq in seqs:
        return_seq = append_2_seqs(return_seq, seq)

    return return_seq


def tack_on_instr_seq(seq, body_seq):
    return InstrSeq(
        seq.needed,
        seq.modified,
        seq.statements + body_seq.statements)


def parallel_instr_seqs(seq_1, seq_2):
    return InstrSeq(
        seq_1.needed.union(seq_2.needed),
        seq_1.modified.union(seq_2.modified),
        seq_1.statements + seq_2.statements)


def preserving(regs, seq_1, seq_2):
    if not regs:
        return append_instr_seqs(seq_1, seq_2)

    first_reg, *rest_regs = regs

    if not (seq_2.needs_register(first_reg)
            and seq_1.modifies_register(first_reg)):
        return preserving(rest_regs, seq_1, seq_2)

    return preserving(
        rest_regs,
        InstrSeq(
            registers_needed(seq_1).union({first_reg}),
            registers_modified(seq_1).difference({first_reg}),
            [
                'save({});'.format(first_reg),
                *seq_1.statements,
                'restore({});'.format(first_reg),
            ]),
        seq_2)
