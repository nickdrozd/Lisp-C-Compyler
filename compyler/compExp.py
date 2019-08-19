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
    CONT,
    ENV,
    VAL,
    FUNC,
    ARGLIST,
    ALLREGS,
)
from keywords import (
    define_keys,
    ass_keys,
    lambda_keys,
    if_keys,
    begin_keys,
    quote_keys,
)
from primitives import PRIMITIVES
from instructions import (
    appendInstrSeqs,
    makeInstrSeq,
    parallelInstrSeqs,
    preserving,
    tackOnInstrSeq,
)
from linkage import (
    NEX,
    RET,
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

def compExp(expr, target=VAL, linkage=NEX):
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
    instrSeq = makeInstrSeq([ENV], [target], [instr])
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
        valueCode = compExp(value, VAL, NEX)

        # leave ass/def val as return val
        instr = CFunc + f'(NAMEOBJ("{variable}"), val, env);'
        instrSeq = makeInstrSeq([ENV, VAL], [target], [instr])

        preserved = preserving([ENV], valueCode, instrSeq)
        return endWithLink(linkage, preserved)

    return comp


compAss = compAssDef('setVar')
compDef = compAssDef('defineVar')


def compIf(expr, target=VAL, linkage=NEX):
    (trueBranch, _, afterIf), (trueBranchInfo, falseBranchInfo, afterIfInfo) = \
    branchesAndInfos(
        ['TRUE_BRANCH', 'FALSE_BRANCH', 'AFTER_IF'])

    (_, ifTest, ifThen, ifElse) = expr

    testCode = compExp(ifTest, VAL, NEX)
    thenCode = compExp(ifThen, target, linkage)
    elseCode = compExp(ifElse, target, afterIf if linkage == NEX else linkage)

    return preserving(
        [ENV, CONT],
        testCode,
        appendInstrSeqs(
            makeInstrSeq(
                [VAL],
                [],
                [f"if (isTrue(val)) goto {trueBranch};"]),
            parallelInstrSeqs(
                appendInstrSeqs(falseBranchInfo, elseCode),
                appendInstrSeqs(trueBranchInfo, thenCode)),
            afterIfInfo))


def compBegin(expr, target=VAL, linkage=NEX):
    _, *seq = expr
    return compSeq(seq, target, linkage)


def compSeq(seq, target=VAL, linkage=NEX):
    first, *rest = seq
    if not rest:
        return compExp(first, target, linkage)

    compFirst = compExp(first, target, NEX)
    compRest = compSeq(rest, target, linkage)
    preserved = [ENV, CONT]
    return preserving(preserved, compFirst, compRest)


def compLambda(expr, target=VAL, linkage=NEX):
    (funcEntry, afterLambda), (funcEntryInfo, afterLambdaInfo) = \
        branchesAndInfos(('ENTRY', 'AFTER_LAMBDA'))

    return appendInstrSeqs(
        tackOnInstrSeq(
            endWithLink(
                afterLambda if linkage == NEX else linkage,
                makeInstrSeq(
                    [ENV],
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

    instrSeq = makeInstrSeq([ENV, FUNC, ARGLIST], [ENV], instrList)
    bodySeq = compSeq(body, VAL, RET)
    appended = appendInstrSeqs(instrSeq, bodySeq)

    return appended


def compApp(expr, target=VAL, linkage=NEX):
    function, *arguments = expr

    funcCode = compExp(function, target=FUNC)

    argCodes = [compExp(arg) for arg in arguments]
    argListCode = constructArglist(argCodes)

    if function in PRIMITIVES:
        primCall = f"{target} = applyPrimitive(func, arglist);"
        primCallSeq = makeInstrSeq([FUNC, ARGLIST], [target], [primCall])
        funcCallCode = endWithLink(linkage, primCallSeq)
    else:
        funcCallCode = compFuncCall(target, linkage)

    arglPresFunc = preserving([FUNC, CONT], argListCode, funcCallCode)

    return preserving([ENV, CONT], funcCode, arglPresFunc)


def constructArglist(argCodes):
    argCodes = argCodes[::-1]

    if not argCodes:
        instr = "arglist = NULLOBJ;"
        return makeInstrSeq([], [ARGLIST], [instr])

    # else:
    instr = "arglist = CONS(val, NULLOBJ);"
    instrSeq = makeInstrSeq([VAL], [ARGLIST], [instr])

    lastArg, *restArgs = argCodes

    codeToGetLastArg = appendInstrSeqs(lastArg, instrSeq)

    return (
        codeToGetLastArg
        if not restArgs else
        preserving(
            [ENV],
            codeToGetLastArg,
            codeToGetRestArgs(restArgs))
    )


def codeToGetRestArgs(argCodes):
    nextArg, *restArgs = argCodes
    instr = "arglist = CONS(val, arglist);"
    instrSeq = makeInstrSeq([VAL, ARGLIST], [ARGLIST], [instr])
    codeForNextArg = preserving([ARGLIST], nextArg, instrSeq)

    return (
        codeForNextArg
        if not restArgs else
        preserving(
            [ENV],
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

    endLabel = afterCall if linkage == NEX else linkage

    applyPrimitiveSeq = makeInstrSeq(
        [FUNC, ARGLIST],
        [target],
        [f"{target} = applyPrimitive(func, arglist);"])

    def makeTestGotoSeq(testString, label):
        return makeInstrSeq(
            [FUNC],
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
    valTarg = target == VAL
    retLink = linkage == RET

    funcList = (
        ["val = COMPLABOBJ(func);", "goto COMP_LABEL;"]
        if funcType == 'compiled' else
        ["save(cont);", "goto APPLY_COMPOUND;"]
    )

    # typical function call, eg (f 5)
    if valTarg and not retLink:
        return makeInstrSeq(
            [FUNC],
            ALLREGS,
            [f"cont = LABELOBJ(_{linkage});"] + funcList)

    # target is func, eg in ((f 4) 5)
    if not valTarg and not retLink:
        (funcReturn,), (funcReturnInfo,) = branchesAndInfos(('FUNC_RETURN',))

        return makeInstrSeq(
            [FUNC],
            ALLREGS,
            ([f"cont = LABELOBJ(_{funcReturn});"]
             + funcList
             + [
                 funcReturnInfo,
                 f"{target} = val;",
                 f"goto {linkage};",
             ]))

    # this gets called, but I don't understand when
    if valTarg and retLink:
        return makeInstrSeq([FUNC, CONT], ALLREGS, funcList)

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
