# instructions


def make_instr_seq(needs, modifies, statements):
    return [needs, modifies, statements]


empty_instr_seq = make_instr_seq([], [], [])


def registers_needed(seq):
    return [] if isinstance(seq, str) else seq[0]


def registers_modified(seq):
    return [] if isinstance(seq, str) else seq[1]


def statements(seq):
    return [seq] if isinstance(seq, str) else seq[2]


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

        needed = list_union(needed_1, list_diff(needed_2, modified_1))
        modified = list_union(modified_1, modified_2)

        statements_1 = statements(seq_1)
        statements_2 = statements(seq_2)
        statement_seq = statements_1 + statements_2

        return make_instr_seq(needed, modified, statement_seq)

    return_seq = empty_instr_seq

    for seq in seqs:
        return_seq = append_2_seqs(return_seq, seq)

    return return_seq


def tack_on_instr_seq(seq, body_seq):
    needed = registers_needed(seq)
    modified = registers_modified(seq)
    statement_seq = statements(seq) + statements(body_seq)
    return make_instr_seq(needed, modified, statement_seq)


def parallel_instr_seqs(seq_1, seq_2):
    needed_1 = registers_needed(seq_1)
    needed_2 = registers_needed(seq_2)
    needed = list_union(needed_1, needed_2)

    modified_1 = registers_modified(seq_1)
    modified_2 = registers_modified(seq_2)
    modified = list_union(modified_1, modified_2)

    statements_1 = statements(seq_1)
    statements_2 = statements(seq_2)
    statement_seq = statements_1 + statements_2

    return make_instr_seq(needed, modified, statement_seq)


def preserving(regs, seq_1, seq_2):
    if not regs:
        return append_instr_seqs(seq_1, seq_2)

    first_reg, *rest_regs = regs
    needs_first = needs_register(seq_2, first_reg)
    modifies_first = modifies_register(seq_1, first_reg)

    if not (needs_first and modifies_first):
        return preserving(rest_regs, seq_1, seq_2)

    save = 'save({});'.format(first_reg)
    seq_1_statements = statements(seq_1)
    restore = 'restore({});'.format(first_reg)
    seq_1_pres_instr = [save] + seq_1_statements + [restore]

    first_seq_1_needs = list_union([first_reg], registers_needed(seq_1))
    first_seq_1_mods = list_diff(registers_modified(seq_1), [first_reg])

    pres_instr_seq = make_instr_seq(
        first_seq_1_needs,
        first_seq_1_mods,
        seq_1_pres_instr
    )

    return preserving(rest_regs, pres_instr_seq, seq_2)


def list_union(s_1, s_2):
    result = []
    for i in s_1:
        result += [i]
    for i in s_2:
        if i not in result:
            result += [i]
    return result


def list_diff(s_1, s_2):
    result = []
    for i in s_1:
        if i not in s_2:
            result += [i]
    return result
