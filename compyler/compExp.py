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
    InstrSeq,
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
    return endWithLink(
        linkage,
        InstrSeq(
            [],
            [target],
            [f"{target} = NUMOBJ({expr});"]))


def compVar(expr, target, linkage):
    return endWithLink(
        linkage,
        InstrSeq(
            [ENV],
            [target],
            [f'{target} = lookup(NAMEOBJ("{expr}"), env);']))


def compQuote(expr, target, linkage):
    _, text = expr

    return endWithLink(
        linkage,
        InstrSeq(
            [],
            [target],
            [f'{target} = parse("{schemify(text)}\\n");']))


def compAssDef(CFunc):
    "CFunc is string"

    def isSugarDef(exp):
        # list? tuple? something more general?
        return isinstance(exp[1], list)

    def transformSugarDef(exp):
        if not isSugarDef(exp):
            return exp

        _, (func, *args), *body = exp

        return ['define', func, ['lambda', args] + body]

    def comp(expr, target, linkage):
        _, variable, value = transformSugarDef(expr)

        return endWithLink(
            linkage,
            preserving(
                [ENV],
                compExp(value, VAL, NEX),
                InstrSeq(
                    [ENV, VAL],
                    [target],
                    [f'{CFunc}(NAMEOBJ("{variable}"), val, env);'])))

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
            InstrSeq(
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

    return preserving(
        [ENV, CONT],
        compExp(first, target, NEX),
        compSeq(rest, target, linkage))


def compLambda(expr, target=VAL, linkage=NEX):
    (funcEntry, afterLambda), (funcEntryInfo, afterLambdaInfo) = \
        branchesAndInfos(('ENTRY', 'AFTER_LAMBDA'))

    return appendInstrSeqs(
        tackOnInstrSeq(
            endWithLink(
                afterLambda if linkage == NEX else linkage,
                InstrSeq(
                    [ENV],
                    [target],
                    [f"{target} = COMPOBJ(_{funcEntry}, env);"])),
            compLambdaBody(expr, funcEntryInfo)),
        InstrSeq([], [], [afterLambdaInfo]))


def compLambdaBody(expr, funcEntryInfo):
    _, params, *body = expr

    return appendInstrSeqs(
        InstrSeq([ENV, FUNC, ARGLIST], [ENV], [
            funcEntryInfo,
            "env = COMPENVOBJ(func);",
            f'unev = parse("{schemify(params)}\\n");',
            "env = extendEnv(unev, arglist, env);",
        ]),
        compSeq(body, VAL, RET))


def compApp(expr, target=VAL, linkage=NEX):
    function, *arguments = expr

    return preserving(
        [ENV, CONT],
        compExp(
            function,
            target=FUNC),
        preserving(
            [FUNC, CONT],
            constructArglist([
                compExp(arg)
                for arg in arguments
            ]),
            compFuncCall(target, linkage)
            if function not in PRIMITIVES else
            endWithLink(
                linkage,
                InstrSeq(
                    [FUNC, ARGLIST],
                    [target],
                    [f"{target} = applyPrimitive(func, arglist);"]))))


def constructArglist(argCodes):
    if not argCodes:
        return InstrSeq([], [ARGLIST], ["arglist = NULLOBJ;"])

    lastArg, *restArgs = reversed(argCodes)

    codeToGetLastArg = appendInstrSeqs(
        lastArg,
        InstrSeq(
            [VAL],
            [ARGLIST],
            ["arglist = CONS(val, NULLOBJ);"]))

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

    codeForNextArg = preserving(
        [ARGLIST],
        nextArg,
        InstrSeq(
            [VAL, ARGLIST],
            [ARGLIST],
            ["arglist = CONS(val, arglist);"]))

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

    applyPrimitiveSeq = InstrSeq(
        [FUNC, ARGLIST],
        [target],
        [f"{target} = applyPrimitive(func, arglist);"])

    def makeTestGotoSeq(testString, label):
        return InstrSeq(
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
        return InstrSeq(
            [FUNC],
            ALLREGS,
            [f"cont = LABELOBJ(_{linkage});"] + funcList)

    # target is func, eg in ((f 4) 5)
    if not valTarg and not retLink:
        (funcReturn,), (funcReturnInfo,) = branchesAndInfos(('FUNC_RETURN',))

        return InstrSeq(
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
        return InstrSeq([FUNC, CONT], ALLREGS, funcList)

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
