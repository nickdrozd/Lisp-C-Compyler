'''
TODO:
    * documentation
    * generic instruction generator?
    * instr_seq class
    * remove llh?
    * rename 'infos'
    * move out keyword_groups (how?)
'''

from registers import *
from keywords import *
from primitives import primitives

from instructions import *
from linkage import *

from labels import branches_and_infos
from parse import schemify
from macros import transform_macros
from llh import *

#----------------------------------#

def comp_exp(expr, target=val, linkage=nex):
    expr = transform_macros(expr)
    if is_self_evaluating(expr):
        comp_type = comp_var if is_var(expr) else comp_num
    else:
        try:
            tag, *_ = expr
            comp_type = keyword_comps[tag]
        except:
            comp_type = comp_app
    return comp_type(expr, target, linkage)

#----------------------------------#

def comp_num(expr, target, linkage):
    instr = "%(target)s = NUMOBJ(%(expr)s);" % locals()
    instr_seq = make_instr_seq([], [target], [instr])
    return end_with_link(linkage, instr_seq)


def comp_var(expr, target, linkage):
    instr = "%(target)s = lookup(NAMEOBJ(\"%(expr)s\"), env);" % locals()
    instr_seq = make_instr_seq([env], [target], [instr])
    return end_with_link(linkage, instr_seq)


def comp_quote(expr, target, linkage):
    _, text = expr
    lisp_text = schemify(text)

    instr = '%(target)s = parse("%(lisp_text)s\\n");' % locals()
    instr_seq = make_instr_seq([], [target], [instr])
    return end_with_link(linkage, instr_seq)


def comp_ass_def(CFunc):
    "CFunc is string"

    def is_sugar_def(exp):
    # list? tuple? something more general?
        return type(exp[1]) == list

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
        value_code = comp_exp(value, val, nex)

        # leave ass/def val as return val
        instr = CFunc + "(NAMEOBJ(\"%(variable)s\"), val, env);" % locals()
        instr_seq = make_instr_seq([env, val], [target], [instr])

        preserved = preserving([env], value_code, instr_seq)
        return end_with_link(linkage, preserved)

    return comp


comp_ass = comp_ass_def('setVar')
comp_def = comp_ass_def('defineVar')


def comp_if(expr, target=val, linkage=nex):
    labels = ['TRUE_BRANCH', 'FALSE_BRANCH', 'AFTER_IF']

    branches, infos = branches_and_infos(labels)

    [true_branch, false_branch, after_if] = branches
    [true_branch_info, false_branch_info, after_if_info] = infos

    then_link = after_if if linkage == nex else linkage

    (_, if_test, if_then, if_else) = expr

    test_code = comp_exp(if_test, val, nex)
    then_code = comp_exp(if_then, target, linkage)
    else_code = comp_exp(if_else, target, then_link)

    is_true_instr = "if (isTrue(val)) "
    goto_true_instr = "goto %(true_branch)s;" % locals()
    instr_list = [is_true_instr + goto_true_instr]
    test_goto_seq = make_instr_seq([val], [], instr_list)

    then_code_labeled = append_instr_seqs(true_branch_info, then_code)
    else_code_labeled = append_instr_seqs(false_branch_info, else_code)

    else_then_seq = parallel_instr_seqs(else_code_labeled, then_code_labeled)
    test_gotos_then_else_seq = append_instr_seqs(test_goto_seq, else_then_seq, after_if_info)

    preserved = [env, cont]
    return preserving(preserved, test_code, test_gotos_then_else_seq)


def comp_begin(expr, target=val, linkage=nex):
    _, *seq = expr
    return comp_seq(seq, target, linkage)


def comp_seq(seq, target=val, linkage=nex):
    first, *rest = seq
    if not rest:
        return comp_exp(first, target, linkage)
    else:
        comp_first = comp_exp(first, target, nex)
        comp_rest = comp_seq(rest, target, linkage)
        preserved = [env, cont]
        return preserving(preserved, comp_first, comp_rest)


def comp_lambda(expr, target=val, linkage=nex):
    labels = ('ENTRY', 'AFTER_LAMBDA')

    branches, infos = branches_and_infos(labels)
    func_entry, after_lambda = branches
    func_entry_info, after_lambda_info = infos

    lambda_link = after_lambda if linkage == nex else linkage
    lambda_body = comp_lambda_body(expr, func_entry_info)

    instr = "%(target)s = COMPOBJ(_%(func_entry)s, env);" % locals()
    instr_seq = make_instr_seq([env], [target], [instr])

    instr_linked = end_with_link(lambda_link, instr_seq)
    tacked_on = tack_on_instr_seq(instr_linked, lambda_body)
    appended = append_instr_seqs(tacked_on, after_lambda_info)

    return appended


def comp_lambda_body(expr, func_entry_info):
    _, params, *body = expr
    lisp_params = schemify(params)

    assign_func_env = "env = COMPENVOBJ(func);"
    parse_params = 'unev = parse("%(lisp_params)s\\n");' % locals()
    extend_func_env = "env = extendEnv(unev, arglist, env);" # %(params)s ?

    instr_list = [func_entry_info, assign_func_env,
                    parse_params, extend_func_env]

    instr_seq = make_instr_seq([env, func, arglist],
                [env], instr_list)
    body_seq = comp_seq(body, val, ret)
    appended = append_instr_seqs(instr_seq, body_seq)

    return appended


def comp_app(expr, target=val, linkage=nex):
    function, *arguments = expr

    func_code = comp_exp(function, target=func)

    arg_codes = [comp_exp(arg) for arg in arguments]
    arg_list_code = construct_arglist(arg_codes)

    if function in primitives:
        prim_call = "%(target)s = applyPrimitive(func, arglist);" % locals()
        prim_call_seq = make_instr_seq([func, arglist], [target], [prim_call])
        func_call_code = end_with_link(linkage, prim_call_seq)
    else:
        func_call_code = comp_func_call(target, linkage)

    argl_pres_func = preserving([func, cont],
                        arg_list_code, func_call_code)

    return preserving([env, cont],
                func_code, argl_pres_func)


def construct_arglist(arg_codes):
    arg_codes = arg_codes[::-1]

    if not arg_codes:
        instr = "arglist = NULLOBJ;"
        return make_instr_seq([], [arglist], [instr])

    # else:
    instr = "arglist = CONS(val, NULLOBJ);"
    instr_seq = make_instr_seq([val], [arglist], [instr])

    last_arg, *rest_args = arg_codes

    code_to_get_last_arg = append_instr_seqs(last_arg, instr_seq)

    if not rest_args:
        return code_to_get_last_arg
    else:
        return preserving([env], code_to_get_last_arg,
                    code_to_get_rest_args(rest_args))


def code_to_get_rest_args(arg_codes):
    next_arg, *rest_args = arg_codes
    instr = "arglist = CONS(val, arglist);"
    instr_seq = make_instr_seq([val, arglist],
                    [arglist], [instr])
    code_for_next_arg = preserving([arglist],
                            next_arg, instr_seq)

    if not rest_args:
        return code_for_next_arg
    else:
        return preserving([env], code_for_next_arg,
                    code_to_get_rest_args(rest_args))


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

    end_label = after_call if linkage == nex else linkage

    def make_test_goto_seq(test_string, label):
        test = "if (%(test_string)s(func)) " % locals()
        goto = "goto %(label)s;" % locals()
        instr_list = [test + goto]
        return make_instr_seq([func], [], instr_list)

    test_primitive_seq = make_test_goto_seq('isPrimitive', primitive_branch)
    test_compound_seq = make_test_goto_seq('isCompound', compound_branch)
    test_seqs = append_instr_seqs(test_primitive_seq, test_compound_seq)

    apply_primitive = "%(target)s = applyPrimitive(func, arglist);" % locals()
    apply_primitive_seq = make_instr_seq([func, arglist],
                    [target], [apply_primitive])

    # calling comp_func_app twice generates two different end_labels
    func_types = ('compound', 'compiled')
    comp_func_apps = [
        comp_func_app(target, end_label, func_type)
            for func_type in func_types]
    (compound_link, compiled_link) = comp_func_apps

    primitive_link = end_with_link(linkage, apply_primitive_seq)

    branch_links = (
        (compiled_branch_info, compiled_link),
        (compound_branch_info, compound_link),
        (primitive_branch_info, primitive_link)
    )

    labeled = [append_instr_seqs(branch, link)
                for (branch, link) in branch_links]

    (compiled_labeled, compound_labeled,
        primitive_labeled) = labeled

    compound_prim_para = parallel_instr_seqs(compound_labeled, primitive_labeled)
    compiled_para = parallel_instr_seqs(compiled_labeled, compound_prim_para)

    return append_instr_seqs(test_seqs, compiled_para, after_call_info)


def comp_func_app(target, linkage, func_type):
    "func_type as string: 'compiled' or 'compound'"
    val_targ = target == val
    ret_link = linkage == ret

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
        assign_cont = "cont = LABELOBJ(_%(linkage)s);" % locals()

        func_list = compiled_list if is_compiled else compound_list
        instr_list = [assign_cont] + func_list

        return make_instr_seq([func], all_regs, instr_list)


    # target is func, eg in ((f 4) 5)
    elif not val_targ and not ret_link:
        labels = ('FUNC_RETURN',)
        branches, infos = branches_and_infos(labels)
        (func_return,) = branches
        (func_return_info,) = infos

        assign_cont = "cont = LABELOBJ(_%(func_return)s);" % locals()

        func_list = compiled_list if is_compiled else compound_list

        assign_target = "%(target)s = val;" % locals()
        goto_linkage = "goto %(linkage)s;" % locals()

        return_list = [func_return_info, assign_target, goto_linkage]

        instr_list = [assign_cont] + func_list + return_list

        return make_instr_seq([func], all_regs, instr_list)


    # this gets called, but I don't understand when
    elif val_targ and ret_link:
        instr_list = compiled_list if is_compiled else compound_list

        return make_instr_seq([func, cont], all_regs, instr_list)

    else:
        Exception('bad function call', 'comp_func_app')

#----------------------------------#

def make_keywords():
    keyword_groups = {
        define_keys : comp_def,
        ass_keys : comp_ass,
        lambda_keys : comp_lambda,
        if_keys : comp_if,
        begin_keys : comp_begin,
        quote_keys : comp_quote
    }

    keyword_comps = {}

    for group in keyword_groups:
        for key in group:
            keyword_comps[key] = keyword_groups[group]

    return keyword_comps.keys(), keyword_comps

keywords, keyword_comps = make_keywords()
