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
    make_instr_seq, tack_on_instr_seq, \
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
    instr_seq = make_instr_seq([], [target], [instr])
    return end_with_link(linkage, instr_seq)


def comp_var(expr, target, linkage):
    instr = "{} = lookup(NAMEOBJ(\"{}\"), env);".format(target, expr)
    instr_seq = make_instr_seq([ENV], [target], [instr])
    return end_with_link(linkage, instr_seq)


def comp_quote(expr, target, linkage):
    _, text = expr
    lisp_text = schemify(text)

    instr = '{} = parse("{}\\n");'.format(target, lisp_text)
    instr_seq = make_instr_seq([], [target], [instr])
    return end_with_link(linkage, instr_seq)


def comp_ass_def(CFunc):
    "CFunc is string"

    def is_sugar_def(exp):
        return isinstance(exp[1], (list, tuple))

    def transform_sugar_def(exp):
        if not is_sugar_def(exp):
            return exp
        _, func_args, *body = exp
        func, *args = func_args
        lambda_exp = ['lambda', args] + body
        return ['define', func, lambda_exp]

    def comp(expr, target, linkage):
        expr = transform_sugar_def(expr)

        _, variable, value = expr
        value_code = comp_exp(value, VAL, NEX)

        # leave ass/def val as return val
        instr = CFunc + "(NAMEOBJ(\"{}\"), val, env);".format(variable)
        instr_seq = make_instr_seq([ENV, VAL], [target], [instr])

        preserved = preserving([ENV], value_code, instr_seq)
        return end_with_link(linkage, preserved)

    return comp


comp_ass = comp_ass_def('setVar')
comp_def = comp_ass_def('defineVar')


def comp_if(expr, target=VAL, linkage=NEX):
    labels = ['TRUE_BRANCH', 'FALSE_BRANCH', 'AFTER_IF']

    branches, infos = branches_and_infos(labels)

    [true_branch, false_branch, after_if] = branches
    [true_branch_info, false_branch_info, after_if_info] = infos

    then_link = after_if if linkage == NEX else linkage

    (_, if_test, if_then, if_else) = expr

    test_code = comp_exp(if_test, VAL, NEX)
    then_code = comp_exp(if_then, target, linkage)
    else_code = comp_exp(if_else, target, then_link)

    is_true_instr = "if (isTrue(val)) "
    goto_true_instr = "goto {};".format(true_branch)
    instr_list = [is_true_instr + goto_true_instr]
    test_goto_seq = make_instr_seq([VAL], [], instr_list)

    then_code_labeled = append_instr_seqs(
        true_branch_info,
        then_code)

    else_code_labeled = append_instr_seqs(
        false_branch_info,
        else_code)

    else_then_seq = parallel_instr_seqs(
        else_code_labeled,
        then_code_labeled)

    test_gotos_then_else_seq = append_instr_seqs(
        test_goto_seq,
        else_then_seq,
        after_if_info)

    preserved = [ENV, CONT]
    return preserving(preserved, test_code, test_gotos_then_else_seq)


def comp_begin(expr, target=VAL, linkage=NEX):
    _, *seq = expr
    return comp_seq(seq, target, linkage)


def comp_seq(seq, target=VAL, linkage=NEX):
    first, *rest = seq

    if not rest:
        return comp_exp(first, target, linkage)

    comp_first = comp_exp(first, target, NEX)
    comp_rest = comp_seq(rest, target, linkage)
    preserved = [ENV, CONT]
    return preserving(preserved, comp_first, comp_rest)


def comp_lambda(expr, target=VAL, linkage=NEX):
    labels = ('ENTRY', 'AFTER_LAMBDA')

    branches, infos = branches_and_infos(labels)
    func_entry, after_lambda = branches
    func_entry_info, after_lambda_info = infos

    lambda_link = after_lambda if linkage == NEX else linkage
    lambda_body = comp_lambda_body(expr, func_entry_info)

    instr = "{} = COMPOBJ(_{}, env);".format(target, func_entry)
    instr_seq = make_instr_seq([ENV], [target], [instr])

    instr_linked = end_with_link(lambda_link, instr_seq)
    tacked_on = tack_on_instr_seq(instr_linked, lambda_body)
    appended = append_instr_seqs(tacked_on, after_lambda_info)

    return appended


def comp_lambda_body(expr, func_entry_info):
    _, params, *body = expr
    lisp_params = schemify(params)

    assign_func_env = "env = COMPENVOBJ(func);"
    parse_params = 'unev = parse("{}\\n");'.format(lisp_params)
    extend_func_env = "env = extendEnv(unev, arglist, env);" # %(params)s ?

    instr_list = [
        func_entry_info,
        assign_func_env,
        parse_params,
        extend_func_env
    ]

    instr_seq = make_instr_seq(
        [ENV, FUNC, ARGLIST],
        [ENV],
        instr_list
    )

    body_seq = comp_seq(body, VAL, RET)
    appended = append_instr_seqs(instr_seq, body_seq)

    return appended


def comp_app(expr, target=VAL, linkage=NEX):
    function, *arguments = expr

    func_code = comp_exp(function, target=FUNC)

    arg_codes = [comp_exp(arg) for arg in arguments]
    arg_list_code = construct_arglist(arg_codes)

    if keywords.is_primitive(function):
        prim_call = "{} = applyPrimitive(func, arglist);".format(target)
        prim_call_seq = make_instr_seq([FUNC, ARGLIST], [target], [prim_call])
        func_call_code = end_with_link(linkage, prim_call_seq)
    else:
        func_call_code = comp_func_call(target, linkage)

    argl_pres_func = preserving(
        [FUNC, CONT],
        arg_list_code,
        func_call_code
    )

    return preserving(
        [ENV, CONT],
        func_code,
        argl_pres_func
    )


def construct_arglist(arg_codes):
    arg_codes = arg_codes[::-1]

    if not arg_codes:
        instr = "arglist = NULLOBJ;"
        return make_instr_seq([], [ARGLIST], [instr])

    # else:
    instr = "arglist = CONS(val, NULLOBJ);"
    instr_seq = make_instr_seq([VAL], [ARGLIST], [instr])

    last_arg, *rest_args = arg_codes

    code_to_get_last_arg = append_instr_seqs(last_arg, instr_seq)

    if not rest_args:
        return code_to_get_last_arg

    return preserving(
        [ENV],
        code_to_get_last_arg,
        code_to_get_rest_args(rest_args)
    )


def code_to_get_rest_args(arg_codes):
    next_arg, *rest_args = arg_codes
    instr = "arglist = CONS(val, arglist);"
    instr_seq = make_instr_seq(
        [VAL, ARGLIST],
        [ARGLIST],
        [instr]
    )

    code_for_next_arg = preserving(
        [ARGLIST],
        next_arg,
        instr_seq
    )

    if not rest_args:
        return code_for_next_arg

    return preserving(
        [ENV],
        code_for_next_arg,
        code_to_get_rest_args(rest_args)
    )


def comp_func_call(target, linkage):
    labels = (
        'PRIMITIVE', 'COMPOUND',
        'COMPILED', 'AFTER_CALL'
    )

    branches, infos = branches_and_infos(labels)

    (primitive_branch, compound_branch,
     compiled_branch, after_call) = branches

    (primitive_branch_info, compound_branch_info,
     compiled_branch_info, after_call_info) = infos

    end_label = after_call if linkage == NEX else linkage

    def make_test_goto_seq(test_string, label):
        test = "if ({}(func)) ".format(test_string)
        goto = "goto {};".format(label)
        instr_list = [test + goto]
        return make_instr_seq([FUNC], [], instr_list)

    test_primitive_seq = make_test_goto_seq('isPrimitive', primitive_branch)
    test_compound_seq = make_test_goto_seq('isCompound', compound_branch)
    test_seqs = append_instr_seqs(test_primitive_seq, test_compound_seq)

    apply_primitive = "{} = applyPrimitive(func, arglist);".format(target)
    apply_primitive_seq = make_instr_seq(
        [FUNC, ARGLIST],
        [target],
        [apply_primitive]
    )

    # calling comp_func_app twice generates two different end_labels
    func_types = ('compound', 'compiled')

    comp_func_apps = [
        comp_func_app(target, end_label, func_type)
        for func_type in func_types
    ]

    (compound_link, compiled_link) = comp_func_apps

    primitive_link = end_with_link(linkage, apply_primitive_seq)

    branch_links = (
        (compiled_branch_info, compiled_link),
        (compound_branch_info, compound_link),
        (primitive_branch_info, primitive_link)
    )

    labeled = [
        append_instr_seqs(branch, link)
        for (branch, link) in branch_links
    ]

    (compiled_labeled, compound_labeled,
     primitive_labeled) = labeled

    compound_prim_para = parallel_instr_seqs(
        compound_labeled,
        primitive_labeled)

    compiled_para = parallel_instr_seqs(
        compiled_labeled,
        compound_prim_para)

    return append_instr_seqs(
        test_seqs,
        compiled_para,
        after_call_info)


def comp_func_app(target, linkage, func_type):
    "func_type as string: 'compiled' or 'compound'"
    val_targ = target == VAL
    ret_link = linkage == RET

    assign_val = "val = COMPLABOBJ(func);"
    goto_val = "goto COMP_LABEL;"
    compiled_list = [assign_val, goto_val]

    save_cont = "save(cont);"
    goto_compound = "goto APPLY_COMPOUND;"
    compound_list = [save_cont, goto_compound]

    is_compiled = func_type == 'compiled'

    # typical function call, eg (f 5)
    if val_targ and not ret_link:
        # common instructions
        assign_cont = "cont = LABELOBJ(_{});".format(linkage)

        func_list = compiled_list if is_compiled else compound_list
        instr_list = [assign_cont] + func_list

        return make_instr_seq([FUNC], ALL_REGS, instr_list)


    # target is func, eg in ((f 4) 5)
    elif not val_targ and not ret_link:
        labels = ('FUNC_RETURN',)
        branches, infos = branches_and_infos(labels)
        (func_return,) = branches
        (func_return_info,) = infos

        assign_cont = "cont = LABELOBJ(_{});".format(func_return)

        func_list = compiled_list if is_compiled else compound_list

        assign_target = "{} = val;".format(target)
        goto_linkage = "goto {};".format(linkage)

        return_list = [func_return_info, assign_target, goto_linkage]

        instr_list = [assign_cont] + func_list + return_list

        return make_instr_seq([FUNC], ALL_REGS, instr_list)


    # this gets called, but I don't understand when
    elif val_targ and ret_link:
        instr_list = compiled_list if is_compiled else compound_list

        return make_instr_seq([FUNC, CONT], ALL_REGS, instr_list)

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
