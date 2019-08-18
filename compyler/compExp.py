'''
TODO:
    * documentation
    * generic instruction generator?
    * instrSeq class
    * remove llh?
    * rename 'infos'
    * move out keyword_groups (how?)
'''

from registers import (
    cont,
    env,
    val,
    func,
    arglist,
    allRegs,
)
from keywords import (
    define_keys,
    ass_keys,
    lambda_keys,
    if_keys,
    begin_keys,
    quote_keys,
)
from primitives import primitives
from instructions import (
    appendInstrSeqs,
    makeInstrSeq,
    parallelInstrSeqs,
    preserving,
    tackOnInstrSeq,
)
from linkage import (
    nex,
    ret,
    endWithLink,
)
from labels import branchesAndInfos
from parse import schemify
from macros import transformMacros
from llh import (
    isVar,
    isSelfEvaluating,
)

#----------------------------------#

def compExp(expr, target=val, linkage=nex):
    expr = transformMacros(expr)
    if isSelfEvaluating(expr):
        compType = compVar if isVar(expr) else compNum
    else:
        try:
            tag, *_ = expr
            compType = KEYWORD_COMPS[tag]
        except (KeyError, TypeError):
            compType = compApp
    return compType(expr, target, linkage)

#----------------------------------#

def compNum(expr, target, linkage):
    instr = f"{target} = NUMOBJ({expr});"
    instrSeq = makeInstrSeq([], [target], [instr])
    return endWithLink(linkage, instrSeq)


def compVar(expr, target, linkage):
    instr = f'{target} = lookup(NAMEOBJ("{expr}"), env);'
    instrSeq = makeInstrSeq([env], [target], [instr])
    return endWithLink(linkage, instrSeq)


def compQuote(expr, target, linkage):
    _, text = expr
    lispText = schemify(text)

    instr = f'{target} = parse("{lispText}\\n");'
    instrSeq = makeInstrSeq([], [target], [instr])
    return endWithLink(linkage, instrSeq)


def compAssDef(CFunc):
    "CFunc is string"

    def isSugarDef(exp):
    # list? tuple? something more general?
        return isinstance(exp[1], list)

    def transformSugarDef(exp):
        if not isSugarDef(exp):
            return exp
        _, funcArgs, *body = exp
        f, *args = funcArgs
        lambdaExp = ['lambda', args] + body
        return ['define', f, lambdaExp]

    def comp(expr, target, linkage):
        expr = transformSugarDef(expr)

        _, variable, value = expr
        valueCode = compExp(value, val, nex)

        # leave ass/def val as return val
        instr = CFunc + f'(NAMEOBJ("{variable}"), val, env);'
        instrSeq = makeInstrSeq([env, val], [target], [instr])

        preserved = preserving([env], valueCode, instrSeq)
        return endWithLink(linkage, preserved)

    return comp


compAss = compAssDef('setVar')
compDef = compAssDef('defineVar')


def compIf(expr, target=val, linkage=nex):
    (trueBranch, _, afterIf), (trueBranchInfo, falseBranchInfo, afterIfInfo) = \
    branchesAndInfos(
        ['TRUE_BRANCH', 'FALSE_BRANCH', 'AFTER_IF'])

    (_, ifTest, ifThen, ifElse) = expr

    testCode = compExp(ifTest, val, nex)
    thenCode = compExp(ifThen, target, linkage)
    elseCode = compExp(ifElse, target, afterIf if linkage == nex else linkage)

    return preserving(
        [env, cont],
        testCode,
        appendInstrSeqs(
            makeInstrSeq(
                [val],
                [],
                [f"if (isTrue(val)) goto {trueBranch};"]),
            parallelInstrSeqs(
                appendInstrSeqs(falseBranchInfo, elseCode),
                appendInstrSeqs(trueBranchInfo, thenCode)),
            afterIfInfo))


def compBegin(expr, target=val, linkage=nex):
    _, *seq = expr
    return compSeq(seq, target, linkage)


def compSeq(seq, target=val, linkage=nex):
    first, *rest = seq
    if not rest:
        return compExp(first, target, linkage)

    compFirst = compExp(first, target, nex)
    compRest = compSeq(rest, target, linkage)
    preserved = [env, cont]
    return preserving(preserved, compFirst, compRest)


def compLambda(expr, target=val, linkage=nex):
    (funcEntry, afterLambda), (funcEntryInfo, afterLambdaInfo) = \
        branchesAndInfos(('ENTRY', 'AFTER_LAMBDA'))

    return appendInstrSeqs(
        tackOnInstrSeq(
            endWithLink(
                afterLambda if linkage == nex else linkage,
                makeInstrSeq(
                    [env],
                    [target],
                    [f"{target} = COMPOBJ(_{funcEntry}, env);"])),
            compLambdaBody(expr, funcEntryInfo)),
        afterLambdaInfo)


def compLambdaBody(expr, funcEntryInfo):
    _, params, *body = expr
    lispParams = schemify(params)

    assignFuncEnv = "env = COMPENVOBJ(func);"
    parseParams = f'unev = parse("{lispParams}\\n");'
    extendFuncEnv = "env = extendEnv(unev, arglist, env);" # %(params)s ?

    instrList = [
        funcEntryInfo,
        assignFuncEnv,
        parseParams,
        extendFuncEnv,
    ]

    instrSeq = makeInstrSeq([env, func, arglist], [env], instrList)
    bodySeq = compSeq(body, val, ret)
    appended = appendInstrSeqs(instrSeq, bodySeq)

    return appended


def compApp(expr, target=val, linkage=nex):
    function, *arguments = expr

    funcCode = compExp(function, target=func)

    argCodes = [compExp(arg) for arg in arguments]
    argListCode = constructArglist(argCodes)

    if function in primitives:
        primCall = f"{target} = applyPrimitive(func, arglist);"
        primCallSeq = makeInstrSeq([func, arglist], [target], [primCall])
        funcCallCode = endWithLink(linkage, primCallSeq)
    else:
        funcCallCode = compFuncCall(target, linkage)

    arglPresFunc = preserving([func, cont], argListCode, funcCallCode)

    return preserving([env, cont], funcCode, arglPresFunc)


def constructArglist(argCodes):
    argCodes = argCodes[::-1]

    if not argCodes:
        instr = "arglist = NULLOBJ;"
        return makeInstrSeq([], [arglist], [instr])

    # else:
    instr = "arglist = CONS(val, NULLOBJ);"
    instrSeq = makeInstrSeq([val], [arglist], [instr])

    lastArg, *restArgs = argCodes

    codeToGetLastArg = appendInstrSeqs(lastArg, instrSeq)

    return (
        codeToGetLastArg
        if not restArgs else
        preserving(
            [env],
            codeToGetLastArg,
            codeToGetRestArgs(restArgs))
    )


def codeToGetRestArgs(argCodes):
    nextArg, *restArgs = argCodes
    instr = "arglist = CONS(val, arglist);"
    instrSeq = makeInstrSeq([val, arglist], [arglist], [instr])
    codeForNextArg = preserving([arglist], nextArg, instrSeq)

    return (
        codeForNextArg
        if not restArgs else
        preserving(
            [env],
            codeForNextArg,
            codeToGetRestArgs(restArgs))
    )


def compFuncCall(target, linkage):
    branches, infos = branchesAndInfos((
        'PRIMITIVE',
        'COMPOUND',
        'COMPILED',
        'AFTER_CALL',
    ))

    (primitiveBranch, compoundBranch, _, afterCall) = branches

    (primitiveBranchInfo,
     compoundBranchInfo,
     compiledBranchInfo,
     afterCallInfo) = infos

    endLabel = afterCall if linkage == nex else linkage

    applyPrimitiveSeq = makeInstrSeq(
        [func, arglist],
        [target],
        [f"{target} = applyPrimitive(func, arglist);"])

    def makeTestGotoSeq(testString, label):
        return makeInstrSeq(
            [func],
            [],
            [f"if ({testString}(func)) goto {label};"])

    # calling compFuncApp twice generates two different endLabels

    return appendInstrSeqs(
        makeTestGotoSeq(
            'isPrimitive',
            primitiveBranch),
        makeTestGotoSeq(
            'isCompound',
            compoundBranch),
        parallelInstrSeqs(
            appendInstrSeqs(
                compiledBranchInfo,
                compFuncApp(target, endLabel, 'compiled')),
            parallelInstrSeqs(
                appendInstrSeqs(
                    compoundBranchInfo,
                    compFuncApp(target, endLabel, 'compound')),
                appendInstrSeqs(
                    primitiveBranchInfo,
                    endWithLink(
                        linkage,
                        applyPrimitiveSeq)))),
        afterCallInfo)


# pylint: disable=inconsistent-return-statements
def compFuncApp(target, linkage, funcType):
    "funcType as string: 'compiled' or 'compound'"
    valTarg = target == val
    retLink = linkage == ret

    funcList = (
        ["val = COMPLABOBJ(func);", "goto COMP_LABEL;"]
        if funcType == 'compiled' else
        ["save(cont);", "goto APPLY_COMPOUND;"]
    )

    # typical function call, eg (f 5)
    if valTarg and not retLink:
        return makeInstrSeq(
            [func],
            allRegs,
            [f"cont = LABELOBJ(_{linkage});"] + funcList)

    # target is func, eg in ((f 4) 5)
    if not valTarg and not retLink:
        (funcReturn,), (funcReturnInfo,) = branchesAndInfos(('FUNC_RETURN',))

        return makeInstrSeq(
            [func],
            allRegs,
            ([f"cont = LABELOBJ(_{funcReturn});"]
             + funcList
             + [
                 funcReturnInfo,
                 f"{target} = val;",
                 f"goto {linkage};",
             ]))

    # this gets called, but I don't understand when
    if valTarg and retLink:
        return makeInstrSeq([func, cont], allRegs, funcList)

    Exception('bad function call', 'compFuncApp')

#----------------------------------#

def makeKeywords():
    keyword_groups = {
        define_keys: compDef,
        ass_keys: compAss,
        lambda_keys: compLambda,
        if_keys: compIf,
        begin_keys: compBegin,
        quote_keys: compQuote
    }

    keyword_comps = {}

    for group in keyword_groups:
        for key in group:
            keyword_comps[key] = keyword_groups[group]

    return keyword_comps.keys(), keyword_comps


KEYWORDS, KEYWORD_COMPS = makeKeywords()
