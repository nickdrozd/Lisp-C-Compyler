'''
TODO:
    * documentation
    * generic instruction generator?
    * instr_seq class
    * remove llh?
    * rename 'infos'
    * move out keyword_groups (how?)
'''

import keywords

from registers import CONT, ENV, VAL, FUNC, ARGLIST, ALL_REGS

from instructions import preserving, \
    InstrSeq, tack_on_instr_seq, \
    append_instr_seqs, parallel_instr_seqs

from linkage import RET, NEX, end_with_link

from labels import branches_and_infos
from parse import schemify
from macros import transform_macros
from llh import is_self_evaluating, is_var

#----------------------------------#

def comp_exp(expr, target=VAL, linkage=NEX):
    expr = transform_macros(expr)

    if is_self_evaluating(expr):
        comp_type = comp_var if is_var(expr) else comp_num

    else:
        try:
            tag, *_ = expr
            comp_type = KEYWORD_COMPS[tag]
        except KeyError:
            comp_type = comp_app

    return comp_type(expr, target, linkage)

#----------------------------------#

def comp_num(expr, target, linkage):
    instr = "{} = NUMOBJ({});".format(target, expr)

    return end_with_link(
        linkage,
        InstrSeq(
            [ENV],
            [target],
            [instr]))


def comp_var(expr, target, linkage):
    instr = "{} = lookup(NAMEOBJ(\"{}\"), env);".format(target, expr)

    return end_with_link(
        linkage,
        InstrSeq(
            [ENV],
            [target],
            [instr]))


def comp_quote(expr, target, linkage):
    _, text = expr
    lisp_text = schemify(text)

    instr = '{} = parse("{}\\n");'.format(target, lisp_text)

    return end_with_link(
        linkage,
        InstrSeq(
            [],
            [target],
            [instr]))


def comp_ass_def(c_func):
    "c_func is string"

    def is_sugar_def(exp):
        return isinstance(exp[1], (list, tuple))

    def transform_sugar_def(exp):
        if not is_sugar_def(exp):
            return exp

        _, func_args, *body = exp

        func, *args = func_args

        return ['define', func, ['lambda', args, *body]]

    def comp(expr, target, linkage):
        expr = transform_sugar_def(expr)

        _, variable, value = expr

        value_code = comp_exp(value, VAL, NEX)

        # leave ass/def val as return val
        instr = c_func + '(NAMEOBJ(\"{}\"), val, env);'.format(variable)

        return end_with_link(
            linkage,
            preserving(
                [ENV],
                value_code,
                InstrSeq(
                    [ENV, VAL],
                    [target],
                    [instr])))

    return comp


# pylint: disable=invalid-name
comp_ass = comp_ass_def('setVar')
comp_def = comp_ass_def('defineVar')


def comp_if(expr, target=VAL, linkage=NEX):
    branches, infos = branches_and_infos(
        ('TRUE_BRANCH', 'FALSE_BRANCH', 'AFTER_IF'))

    true_branch, _, after_if = branches
    true_branch_info, false_branch_info, after_if_info = infos

    then_link = after_if if linkage == NEX else linkage

    _, if_test, if_then, if_else = expr

    test_code = comp_exp(if_test, VAL, NEX)
    then_code = comp_exp(if_then, target, linkage)
    else_code = comp_exp(if_else, target, then_link)

    true_instr = 'if (isTrue(val)) goto {};'.format(true_branch)

    return preserving(
        [ENV, CONT],
        test_code,
        append_instr_seqs(
            InstrSeq(
                [VAL],
                [],
                [true_instr]),
            parallel_instr_seqs(
                append_instr_seqs(
                    false_branch_info,
                    else_code),
                append_instr_seqs(
                    true_branch_info,
                    then_code)),
            after_if_info))


def comp_begin(expr, target=VAL, linkage=NEX):
    _, *seq = expr

    return comp_seq(seq, target, linkage)


def comp_seq(seq, target=VAL, linkage=NEX):
    first, *rest = seq

    if not rest:
        return comp_exp(first, target, linkage)

    comp_first = comp_exp(first, target, NEX)
    comp_rest = comp_seq(rest, target, linkage)

    return preserving(
        [ENV, CONT],
        comp_first,
        comp_rest)


def comp_lambda(expr, target=VAL, linkage=NEX):
    branches, infos = branches_and_infos(('ENTRY', 'AFTER_LAMBDA'))
    func_entry, after_lambda = branches
    func_entry_info, after_lambda_info = infos

    lambda_link = after_lambda if linkage == NEX else linkage
    lambda_body = comp_lambda_body(expr, func_entry_info)

    instr = "{} = COMPOBJ(_{}, env);".format(target, func_entry)

    return append_instr_seqs(
        tack_on_instr_seq(
            end_with_link(
                lambda_link,
                InstrSeq(
                    [ENV],
                    [target],
                    [instr])),
            lambda_body),
        after_lambda_info)


def comp_lambda_body(expr, func_entry_info):
    _, params, *body = expr

    instr_list = [
        func_entry_info,
        'env = COMPENVOBJ(func);',
        'unev = parse("{}\\n");'.format(schemify(params)),
        'env = extendEnv(unev, arglist, env);',
    ]

    body_seq = comp_seq(body, VAL, RET)

    return append_instr_seqs(
        InstrSeq(
            [ENV, FUNC, ARGLIST],
            [ENV],
            instr_list),
        body_seq)


def comp_app(expr, target=VAL, linkage=NEX):
    function, *arguments = expr

    func_code = comp_exp(function, target=FUNC)

    arg_codes = [comp_exp(arg) for arg in arguments]

    prim_call = "{} = applyPrimitive(func, arglist);".format(target)

    func_call_code = (
        end_with_link(
            linkage,
            InstrSeq(
                [FUNC, ARGLIST],
                [target],
                [prim_call]))
        if keywords.is_primitive(function) else
        comp_func_call(target, linkage)
    )

    return preserving(
        [ENV, CONT],
        func_code,
        preserving(
            [FUNC, CONT],
            construct_arglist(arg_codes),
            func_call_code)
    )


def construct_arglist(arg_codes):
    arg_codes = arg_codes[::-1]

    if not arg_codes:
        instr = "arglist = NULLOBJ;"

        return InstrSeq(
            [],
            [ARGLIST],
            [instr])

    instr = "arglist = CONS(val, NULLOBJ);"

    instr_seq = InstrSeq(
        [VAL],
        [ARGLIST],
        [instr])

    last_arg, *rest_args = arg_codes

    code_to_get_last_arg = append_instr_seqs(last_arg, instr_seq)

    if not rest_args:
        return code_to_get_last_arg

    return preserving(
        [ENV],
        code_to_get_last_arg,
        code_to_get_rest_args(rest_args))


def code_to_get_rest_args(arg_codes):
    next_arg, *rest_args = arg_codes

    instr = "arglist = CONS(val, arglist);"

    code_for_next_arg = preserving(
        [ARGLIST],
        next_arg,
        InstrSeq(
            [VAL, ARGLIST],
            [ARGLIST],
            [instr]))

    if not rest_args:
        return code_for_next_arg

    return preserving(
        [ENV],
        code_for_next_arg,
        code_to_get_rest_args(rest_args))


def comp_func_call(target, linkage):
    branches, infos = branches_and_infos((
        'PRIMITIVE', 'COMPOUND',
        'COMPILED', 'AFTER_CALL'
    ))

    primitive_branch, compound_branch, _, after_call = branches

    (primitive_branch_info, compound_branch_info,
     compiled_branch_info, after_call_info) = infos

    end_label = after_call if linkage == NEX else linkage

    def make_test_goto_seq(test, label):
        instr = 'if ({}(func)) goto {};'.format(test, label)

        return InstrSeq(
            [FUNC],
            [],
            [instr])

    apply_primitive_seq = InstrSeq(
        [FUNC, ARGLIST],
        [target],
        ['{} = applyPrimitive(func, arglist);'.format(target)]
    )

    # calling comp_func_app twice generates two different end_labels

    return append_instr_seqs(
        append_instr_seqs(
            make_test_goto_seq(
                'isPrimitive',
                primitive_branch),
            make_test_goto_seq(
                'isCompound',
                compound_branch)),
        parallel_instr_seqs(
            append_instr_seqs(
                compiled_branch_info,
                comp_func_app(target, end_label, 'compiled')),
            parallel_instr_seqs(
                append_instr_seqs(
                    compound_branch_info,
                    comp_func_app(target, end_label, 'compound')),
                append_instr_seqs(
                    primitive_branch_info,
                    end_with_link(
                        linkage,
                        apply_primitive_seq)))),
        after_call_info)


def comp_func_app(target, linkage, func_type):
    "func_type as string: 'compiled' or 'compound'"
    val_targ = target == VAL
    ret_link = linkage == RET

    compiled_list = [
        'val = COMPLABOBJ(func);',
        'goto COMP_LABEL;',
    ]

    compound_list = [
        'save(cont);',
        'goto APPLY_COMPOUND;',
    ]

    func_list = compiled_list if func_type == 'compiled' else compound_list

    # typical function call, eg (f 5)
    if val_targ and not ret_link:
        # common instructions
        assign_cont = "cont = LABELOBJ(_{});".format(linkage)

        return InstrSeq(
            [FUNC],
            ALL_REGS,
            [assign_cont,
             *func_list])

    # target is func, eg in ((f 4) 5)
    elif not val_targ and not ret_link:
        (func_return,), (func_return_info,) = \
            branches_and_infos(('FUNC_RETURN',))

        instr_list = [
            'cont = LABELOBJ(_{});'.format(func_return),
            *func_list,
            func_return_info,
            '{} = val;'.format(target),
            'goto {};'.format(linkage),
        ]

        return InstrSeq(
            [FUNC],
            ALL_REGS,
            instr_list)

    # this gets called, but I don't understand when
    elif val_targ and ret_link:
        return InstrSeq(
            [FUNC, CONT],
            ALL_REGS,
            func_list)

    else:
        Exception('bad function call', 'comp_func_app')

#----------------------------------#

def make_keywords():
    keyword_groups = {
        keywords.DEFINE: comp_def,
        keywords.ASS: comp_ass,
        keywords.LAMBDA: comp_lambda,
        keywords.IF: comp_if,
        keywords.BEGIN: comp_begin,
        keywords.QUOTE: comp_quote
    }

    keyword_comps = {}

    for group in keyword_groups:
        for key in group:
            keyword_comps[key] = keyword_groups[group]

    return keyword_comps.keys(), keyword_comps


KEYWORDS, KEYWORD_COMPS = make_keywords()
