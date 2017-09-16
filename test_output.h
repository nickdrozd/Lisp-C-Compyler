/*
	This code is compiler-generated!
	It may be ugly, but it sure is fast!
	Can you figure out how it works?

	https://github.com/nickdrozd/Lisp-C-Compyler
*/

#ifndef COMP_CODE_GUARD
#define COMP_CODE_GUARD

#define COMPILED_CODE_BODY \
val = parse("()\n"); \
defineVar(NAMEOBJ("nil"), val, env); \
val = COMPOBJ(_ENTRY_1, env); \
goto AFTER_LAMBDA_1; \
ENTRY_1: print_info("ENTRY_1"); \
env = COMPENVOBJ(func); \
unev = parse("s\n"); \
env = extendEnv(unev, arglist, env); \
val = lookup(NAMEOBJ("s"), env); \
goto CONTINUE; \
AFTER_LAMBDA_1: print_info("AFTER_LAMBDA_1"); \
defineVar(NAMEOBJ("list"), val, env); \
val = COMPOBJ(_ENTRY_2, env); \
goto AFTER_LAMBDA_2; \
ENTRY_2: print_info("ENTRY_2"); \
env = COMPENVOBJ(func); \
unev = parse("(s)\n"); \
env = extendEnv(unev, arglist, env); \
val = COMPOBJ(_ENTRY_3, env); \
goto AFTER_LAMBDA_3; \
ENTRY_3: print_info("ENTRY_3"); \
env = COMPENVOBJ(func); \
unev = parse("(total rest)\n"); \
env = extendEnv(unev, arglist, env); \
func = lookup(NAMEOBJ("null?"), env); \
val = lookup(NAMEOBJ("rest"), env); \
arglist = CONS(val, NULLOBJ); \
val = applyPrimitive(func, arglist); \
if (isTrue(val)) goto TRUE_BRANCH_1; \
FALSE_BRANCH_1: print_info("FALSE_BRANCH_1"); \
func = lookup(NAMEOBJ("loop"), env); \
save(func); \
func = lookup(NAMEOBJ("cdr"), env); \
val = lookup(NAMEOBJ("rest"), env); \
arglist = CONS(val, NULLOBJ); \
val = applyPrimitive(func, arglist); \
arglist = CONS(val, NULLOBJ); \
save(arglist); \
func = lookup(NAMEOBJ("add1"), env); \
val = lookup(NAMEOBJ("total"), env); \
arglist = CONS(val, NULLOBJ); \
val = applyPrimitive(func, arglist); \
restore(arglist); \
arglist = CONS(val, arglist); \
restore(func); \
if (isPrimitive(func)) goto PRIMITIVE_1; \
if (isCompound(func)) goto COMPOUND_1; \
COMPILED_1: print_info("COMPILED_1"); \
val = COMPLABOBJ(func); \
goto COMP_LABEL; \
COMPOUND_1: print_info("COMPOUND_1"); \
save(cont); \
goto APPLY_COMPOUND; \
PRIMITIVE_1: print_info("PRIMITIVE_1"); \
val = applyPrimitive(func, arglist); \
goto CONTINUE; \
AFTER_CALL_1: print_info("AFTER_CALL_1"); \
TRUE_BRANCH_1: print_info("TRUE_BRANCH_1"); \
val = lookup(NAMEOBJ("total"), env); \
goto CONTINUE; \
AFTER_IF_1: print_info("AFTER_IF_1"); \
AFTER_LAMBDA_3: print_info("AFTER_LAMBDA_3"); \
defineVar(NAMEOBJ("loop"), val, env); \
func = lookup(NAMEOBJ("loop"), env); \
val = lookup(NAMEOBJ("s"), env); \
arglist = CONS(val, NULLOBJ); \
val = NUMOBJ(0); \
arglist = CONS(val, arglist); \
if (isPrimitive(func)) goto PRIMITIVE_2; \
if (isCompound(func)) goto COMPOUND_2; \
COMPILED_2: print_info("COMPILED_2"); \
val = COMPLABOBJ(func); \
goto COMP_LABEL; \
COMPOUND_2: print_info("COMPOUND_2"); \
save(cont); \
goto APPLY_COMPOUND; \
PRIMITIVE_2: print_info("PRIMITIVE_2"); \
val = applyPrimitive(func, arglist); \
goto CONTINUE; \
AFTER_CALL_2: print_info("AFTER_CALL_2"); \
AFTER_LAMBDA_2: print_info("AFTER_LAMBDA_2"); \
defineVar(NAMEOBJ("length"), val, env); \
val = COMPOBJ(_ENTRY_4, env); \
goto AFTER_LAMBDA_4; \
ENTRY_4: print_info("ENTRY_4"); \
env = COMPENVOBJ(func); \
unev = parse("(items n)\n"); \
env = extendEnv(unev, arglist, env); \
func = lookup(NAMEOBJ("zero?"), env); \
val = lookup(NAMEOBJ("n"), env); \
arglist = CONS(val, NULLOBJ); \
val = applyPrimitive(func, arglist); \
if (isTrue(val)) goto TRUE_BRANCH_2; \
FALSE_BRANCH_2: print_info("FALSE_BRANCH_2"); \
func = lookup(NAMEOBJ("list-ref"), env); \
save(func); \
func = lookup(NAMEOBJ("sub1"), env); \
val = lookup(NAMEOBJ("n"), env); \
arglist = CONS(val, NULLOBJ); \
val = applyPrimitive(func, arglist); \
arglist = CONS(val, NULLOBJ); \
save(arglist); \
func = lookup(NAMEOBJ("cdr"), env); \
val = lookup(NAMEOBJ("items"), env); \
arglist = CONS(val, NULLOBJ); \
val = applyPrimitive(func, arglist); \
restore(arglist); \
arglist = CONS(val, arglist); \
restore(func); \
if (isPrimitive(func)) goto PRIMITIVE_3; \
if (isCompound(func)) goto COMPOUND_3; \
COMPILED_3: print_info("COMPILED_3"); \
val = COMPLABOBJ(func); \
goto COMP_LABEL; \
COMPOUND_3: print_info("COMPOUND_3"); \
save(cont); \
goto APPLY_COMPOUND; \
PRIMITIVE_3: print_info("PRIMITIVE_3"); \
val = applyPrimitive(func, arglist); \
goto CONTINUE; \
AFTER_CALL_3: print_info("AFTER_CALL_3"); \
TRUE_BRANCH_2: print_info("TRUE_BRANCH_2"); \
func = lookup(NAMEOBJ("car"), env); \
val = lookup(NAMEOBJ("items"), env); \
arglist = CONS(val, NULLOBJ); \
val = applyPrimitive(func, arglist); \
goto CONTINUE; \
AFTER_IF_2: print_info("AFTER_IF_2"); \
AFTER_LAMBDA_4: print_info("AFTER_LAMBDA_4"); \
defineVar(NAMEOBJ("list-ref"), val, env); \
val = COMPOBJ(_ENTRY_5, env); \
goto AFTER_LAMBDA_5; \
ENTRY_5: print_info("ENTRY_5"); \
env = COMPENVOBJ(func); \
unev = parse("(list1 list2)\n"); \
env = extendEnv(unev, arglist, env); \
func = lookup(NAMEOBJ("null?"), env); \
val = lookup(NAMEOBJ("list1"), env); \
arglist = CONS(val, NULLOBJ); \
val = applyPrimitive(func, arglist); \
if (isTrue(val)) goto TRUE_BRANCH_3; \
FALSE_BRANCH_3: print_info("FALSE_BRANCH_3"); \
func = lookup(NAMEOBJ("cons"), env); \
save(cont); \
save(func); \
save(env); \
func = lookup(NAMEOBJ("append"), env); \
save(func); \
val = lookup(NAMEOBJ("list2"), env); \
arglist = CONS(val, NULLOBJ); \
save(arglist); \
func = lookup(NAMEOBJ("cdr"), env); \
val = lookup(NAMEOBJ("list1"), env); \
arglist = CONS(val, NULLOBJ); \
val = applyPrimitive(func, arglist); \
restore(arglist); \
arglist = CONS(val, arglist); \
restore(func); \
if (isPrimitive(func)) goto PRIMITIVE_4; \
if (isCompound(func)) goto COMPOUND_4; \
COMPILED_4: print_info("COMPILED_4"); \
cont = LABELOBJ(_AFTER_CALL_4); \
val = COMPLABOBJ(func); \
goto COMP_LABEL; \
COMPOUND_4: print_info("COMPOUND_4"); \
cont = LABELOBJ(_AFTER_CALL_4); \
save(cont); \
goto APPLY_COMPOUND; \
PRIMITIVE_4: print_info("PRIMITIVE_4"); \
val = applyPrimitive(func, arglist); \
AFTER_CALL_4: print_info("AFTER_CALL_4"); \
arglist = CONS(val, NULLOBJ); \
restore(env); \
save(arglist); \
func = lookup(NAMEOBJ("car"), env); \
val = lookup(NAMEOBJ("list1"), env); \
arglist = CONS(val, NULLOBJ); \
val = applyPrimitive(func, arglist); \
restore(arglist); \
arglist = CONS(val, arglist); \
restore(func); \
restore(cont); \
val = applyPrimitive(func, arglist); \
goto CONTINUE; \
TRUE_BRANCH_3: print_info("TRUE_BRANCH_3"); \
val = lookup(NAMEOBJ("list2"), env); \
goto CONTINUE; \
AFTER_IF_3: print_info("AFTER_IF_3"); \
AFTER_LAMBDA_5: print_info("AFTER_LAMBDA_5"); \
defineVar(NAMEOBJ("append"), val, env); \
val = COMPOBJ(_ENTRY_6, env); \
goto AFTER_LAMBDA_6; \
ENTRY_6: print_info("ENTRY_6"); \
env = COMPENVOBJ(func); \
unev = parse("(items)\n"); \
env = extendEnv(unev, arglist, env); \
val = COMPOBJ(_ENTRY_7, env); \
goto AFTER_LAMBDA_7; \
ENTRY_7: print_info("ENTRY_7"); \
env = COMPENVOBJ(func); \
unev = parse("(result rest)\n"); \
env = extendEnv(unev, arglist, env); \
func = lookup(NAMEOBJ("null?"), env); \
val = lookup(NAMEOBJ("rest"), env); \
arglist = CONS(val, NULLOBJ); \
val = applyPrimitive(func, arglist); \
if (isTrue(val)) goto TRUE_BRANCH_4; \
FALSE_BRANCH_4: print_info("FALSE_BRANCH_4"); \
func = lookup(NAMEOBJ("loop"), env); \
save(func); \
func = lookup(NAMEOBJ("cdr"), env); \
val = lookup(NAMEOBJ("rest"), env); \
arglist = CONS(val, NULLOBJ); \
val = applyPrimitive(func, arglist); \
arglist = CONS(val, NULLOBJ); \
save(arglist); \
func = lookup(NAMEOBJ("cons"), env); \
save(func); \
val = lookup(NAMEOBJ("result"), env); \
arglist = CONS(val, NULLOBJ); \
save(arglist); \
func = lookup(NAMEOBJ("car"), env); \
val = lookup(NAMEOBJ("rest"), env); \
arglist = CONS(val, NULLOBJ); \
val = applyPrimitive(func, arglist); \
restore(arglist); \
arglist = CONS(val, arglist); \
restore(func); \
val = applyPrimitive(func, arglist); \
restore(arglist); \
arglist = CONS(val, arglist); \
restore(func); \
if (isPrimitive(func)) goto PRIMITIVE_5; \
if (isCompound(func)) goto COMPOUND_5; \
COMPILED_5: print_info("COMPILED_5"); \
val = COMPLABOBJ(func); \
goto COMP_LABEL; \
COMPOUND_5: print_info("COMPOUND_5"); \
save(cont); \
goto APPLY_COMPOUND; \
PRIMITIVE_5: print_info("PRIMITIVE_5"); \
val = applyPrimitive(func, arglist); \
goto CONTINUE; \
AFTER_CALL_5: print_info("AFTER_CALL_5"); \
TRUE_BRANCH_4: print_info("TRUE_BRANCH_4"); \
val = lookup(NAMEOBJ("result"), env); \
goto CONTINUE; \
AFTER_IF_4: print_info("AFTER_IF_4"); \
AFTER_LAMBDA_7: print_info("AFTER_LAMBDA_7"); \
defineVar(NAMEOBJ("loop"), val, env); \
func = lookup(NAMEOBJ("loop"), env); \
val = lookup(NAMEOBJ("items"), env); \
arglist = CONS(val, NULLOBJ); \
val = lookup(NAMEOBJ("nil"), env); \
arglist = CONS(val, arglist); \
if (isPrimitive(func)) goto PRIMITIVE_6; \
if (isCompound(func)) goto COMPOUND_6; \
COMPILED_6: print_info("COMPILED_6"); \
val = COMPLABOBJ(func); \
goto COMP_LABEL; \
COMPOUND_6: print_info("COMPOUND_6"); \
save(cont); \
goto APPLY_COMPOUND; \
PRIMITIVE_6: print_info("PRIMITIVE_6"); \
val = applyPrimitive(func, arglist); \
goto CONTINUE; \
AFTER_CALL_6: print_info("AFTER_CALL_6"); \
AFTER_LAMBDA_6: print_info("AFTER_LAMBDA_6"); \
defineVar(NAMEOBJ("reverse"), val, env); \
val = COMPOBJ(_ENTRY_8, env); \
goto AFTER_LAMBDA_8; \
ENTRY_8: print_info("ENTRY_8"); \
env = COMPENVOBJ(func); \
unev = parse("(func items)\n"); \
env = extendEnv(unev, arglist, env); \
val = COMPOBJ(_ENTRY_9, env); \
goto AFTER_LAMBDA_9; \
ENTRY_9: print_info("ENTRY_9"); \
env = COMPENVOBJ(func); \
unev = parse("(result rest)\n"); \
env = extendEnv(unev, arglist, env); \
func = lookup(NAMEOBJ("null?"), env); \
val = lookup(NAMEOBJ("rest"), env); \
arglist = CONS(val, NULLOBJ); \
val = applyPrimitive(func, arglist); \
if (isTrue(val)) goto TRUE_BRANCH_5; \
FALSE_BRANCH_5: print_info("FALSE_BRANCH_5"); \
func = lookup(NAMEOBJ("loop"), env); \
save(cont); \
save(func); \
func = lookup(NAMEOBJ("cdr"), env); \
val = lookup(NAMEOBJ("rest"), env); \
arglist = CONS(val, NULLOBJ); \
val = applyPrimitive(func, arglist); \
arglist = CONS(val, NULLOBJ); \
save(arglist); \
func = lookup(NAMEOBJ("cons"), env); \
save(func); \
val = lookup(NAMEOBJ("result"), env); \
arglist = CONS(val, NULLOBJ); \
save(arglist); \
func = lookup(NAMEOBJ("func"), env); \
save(func); \
func = lookup(NAMEOBJ("car"), env); \
val = lookup(NAMEOBJ("rest"), env); \
arglist = CONS(val, NULLOBJ); \
val = applyPrimitive(func, arglist); \
arglist = CONS(val, NULLOBJ); \
restore(func); \
if (isPrimitive(func)) goto PRIMITIVE_8; \
if (isCompound(func)) goto COMPOUND_8; \
COMPILED_8: print_info("COMPILED_8"); \
cont = LABELOBJ(_AFTER_CALL_8); \
val = COMPLABOBJ(func); \
goto COMP_LABEL; \
COMPOUND_8: print_info("COMPOUND_8"); \
cont = LABELOBJ(_AFTER_CALL_8); \
save(cont); \
goto APPLY_COMPOUND; \
PRIMITIVE_8: print_info("PRIMITIVE_8"); \
val = applyPrimitive(func, arglist); \
AFTER_CALL_8: print_info("AFTER_CALL_8"); \
restore(arglist); \
arglist = CONS(val, arglist); \
restore(func); \
val = applyPrimitive(func, arglist); \
restore(arglist); \
arglist = CONS(val, arglist); \
restore(func); \
restore(cont); \
if (isPrimitive(func)) goto PRIMITIVE_9; \
if (isCompound(func)) goto COMPOUND_9; \
COMPILED_9: print_info("COMPILED_9"); \
val = COMPLABOBJ(func); \
goto COMP_LABEL; \
COMPOUND_9: print_info("COMPOUND_9"); \
save(cont); \
goto APPLY_COMPOUND; \
PRIMITIVE_9: print_info("PRIMITIVE_9"); \
val = applyPrimitive(func, arglist); \
goto CONTINUE; \
AFTER_CALL_9: print_info("AFTER_CALL_9"); \
TRUE_BRANCH_5: print_info("TRUE_BRANCH_5"); \
func = lookup(NAMEOBJ("reverse"), env); \
val = lookup(NAMEOBJ("result"), env); \
arglist = CONS(val, NULLOBJ); \
if (isPrimitive(func)) goto PRIMITIVE_7; \
if (isCompound(func)) goto COMPOUND_7; \
COMPILED_7: print_info("COMPILED_7"); \
val = COMPLABOBJ(func); \
goto COMP_LABEL; \
COMPOUND_7: print_info("COMPOUND_7"); \
save(cont); \
goto APPLY_COMPOUND; \
PRIMITIVE_7: print_info("PRIMITIVE_7"); \
val = applyPrimitive(func, arglist); \
goto CONTINUE; \
AFTER_CALL_7: print_info("AFTER_CALL_7"); \
AFTER_IF_5: print_info("AFTER_IF_5"); \
AFTER_LAMBDA_9: print_info("AFTER_LAMBDA_9"); \
defineVar(NAMEOBJ("loop"), val, env); \
func = lookup(NAMEOBJ("loop"), env); \
val = lookup(NAMEOBJ("items"), env); \
arglist = CONS(val, NULLOBJ); \
val = lookup(NAMEOBJ("nil"), env); \
arglist = CONS(val, arglist); \
if (isPrimitive(func)) goto PRIMITIVE_10; \
if (isCompound(func)) goto COMPOUND_10; \
COMPILED_10: print_info("COMPILED_10"); \
val = COMPLABOBJ(func); \
goto COMP_LABEL; \
COMPOUND_10: print_info("COMPOUND_10"); \
save(cont); \
goto APPLY_COMPOUND; \
PRIMITIVE_10: print_info("PRIMITIVE_10"); \
val = applyPrimitive(func, arglist); \
goto CONTINUE; \
AFTER_CALL_10: print_info("AFTER_CALL_10"); \
AFTER_LAMBDA_8: print_info("AFTER_LAMBDA_8"); \
defineVar(NAMEOBJ("map"), val, env); \
val = COMPOBJ(_ENTRY_10, env); \
goto AFTER_LAMBDA_10; \
ENTRY_10: print_info("ENTRY_10"); \
env = COMPENVOBJ(func); \
unev = parse("(comb null seq)\n"); \
env = extendEnv(unev, arglist, env); \
val = COMPOBJ(_ENTRY_11, env); \
goto AFTER_LAMBDA_11; \
ENTRY_11: print_info("ENTRY_11"); \
env = COMPENVOBJ(func); \
unev = parse("(result rest)\n"); \
env = extendEnv(unev, arglist, env); \
func = lookup(NAMEOBJ("null?"), env); \
val = lookup(NAMEOBJ("rest"), env); \
arglist = CONS(val, NULLOBJ); \
val = applyPrimitive(func, arglist); \
if (isTrue(val)) goto TRUE_BRANCH_6; \
FALSE_BRANCH_6: print_info("FALSE_BRANCH_6"); \
func = lookup(NAMEOBJ("loop"), env); \
save(cont); \
save(func); \
func = lookup(NAMEOBJ("cdr"), env); \
val = lookup(NAMEOBJ("rest"), env); \
arglist = CONS(val, NULLOBJ); \
val = applyPrimitive(func, arglist); \
arglist = CONS(val, NULLOBJ); \
save(arglist); \
func = lookup(NAMEOBJ("comb"), env); \
save(func); \
func = lookup(NAMEOBJ("car"), env); \
val = lookup(NAMEOBJ("rest"), env); \
arglist = CONS(val, NULLOBJ); \
val = applyPrimitive(func, arglist); \
arglist = CONS(val, NULLOBJ); \
val = lookup(NAMEOBJ("result"), env); \
arglist = CONS(val, arglist); \
restore(func); \
if (isPrimitive(func)) goto PRIMITIVE_11; \
if (isCompound(func)) goto COMPOUND_11; \
COMPILED_11: print_info("COMPILED_11"); \
cont = LABELOBJ(_AFTER_CALL_11); \
val = COMPLABOBJ(func); \
goto COMP_LABEL; \
COMPOUND_11: print_info("COMPOUND_11"); \
cont = LABELOBJ(_AFTER_CALL_11); \
save(cont); \
goto APPLY_COMPOUND; \
PRIMITIVE_11: print_info("PRIMITIVE_11"); \
val = applyPrimitive(func, arglist); \
AFTER_CALL_11: print_info("AFTER_CALL_11"); \
restore(arglist); \
arglist = CONS(val, arglist); \
restore(func); \
restore(cont); \
if (isPrimitive(func)) goto PRIMITIVE_12; \
if (isCompound(func)) goto COMPOUND_12; \
COMPILED_12: print_info("COMPILED_12"); \
val = COMPLABOBJ(func); \
goto COMP_LABEL; \
COMPOUND_12: print_info("COMPOUND_12"); \
save(cont); \
goto APPLY_COMPOUND; \
PRIMITIVE_12: print_info("PRIMITIVE_12"); \
val = applyPrimitive(func, arglist); \
goto CONTINUE; \
AFTER_CALL_12: print_info("AFTER_CALL_12"); \
TRUE_BRANCH_6: print_info("TRUE_BRANCH_6"); \
val = lookup(NAMEOBJ("result"), env); \
goto CONTINUE; \
AFTER_IF_6: print_info("AFTER_IF_6"); \
AFTER_LAMBDA_11: print_info("AFTER_LAMBDA_11"); \
defineVar(NAMEOBJ("loop"), val, env); \
func = lookup(NAMEOBJ("loop"), env); \
val = lookup(NAMEOBJ("seq"), env); \
arglist = CONS(val, NULLOBJ); \
val = lookup(NAMEOBJ("null"), env); \
arglist = CONS(val, arglist); \
if (isPrimitive(func)) goto PRIMITIVE_13; \
if (isCompound(func)) goto COMPOUND_13; \
COMPILED_13: print_info("COMPILED_13"); \
val = COMPLABOBJ(func); \
goto COMP_LABEL; \
COMPOUND_13: print_info("COMPOUND_13"); \
save(cont); \
goto APPLY_COMPOUND; \
PRIMITIVE_13: print_info("PRIMITIVE_13"); \
val = applyPrimitive(func, arglist); \
goto CONTINUE; \
AFTER_CALL_13: print_info("AFTER_CALL_13"); \
AFTER_LAMBDA_10: print_info("AFTER_LAMBDA_10"); \
defineVar(NAMEOBJ("fold-left"), val, env); \
val = COMPOBJ(_ENTRY_12, env); \
goto AFTER_LAMBDA_12; \
ENTRY_12: print_info("ENTRY_12"); \
env = COMPENVOBJ(func); \
unev = parse("nums\n"); \
env = extendEnv(unev, arglist, env); \
func = lookup(NAMEOBJ("fold-left"), env); \
val = lookup(NAMEOBJ("nums"), env); \
arglist = CONS(val, NULLOBJ); \
val = NUMOBJ(0); \
arglist = CONS(val, arglist); \
val = lookup(NAMEOBJ("_+_"), env); \
arglist = CONS(val, arglist); \
if (isPrimitive(func)) goto PRIMITIVE_14; \
if (isCompound(func)) goto COMPOUND_14; \
COMPILED_14: print_info("COMPILED_14"); \
val = COMPLABOBJ(func); \
goto COMP_LABEL; \
COMPOUND_14: print_info("COMPOUND_14"); \
save(cont); \
goto APPLY_COMPOUND; \
PRIMITIVE_14: print_info("PRIMITIVE_14"); \
val = applyPrimitive(func, arglist); \
goto CONTINUE; \
AFTER_CALL_14: print_info("AFTER_CALL_14"); \
AFTER_LAMBDA_12: print_info("AFTER_LAMBDA_12"); \
defineVar(NAMEOBJ("+"), val, env); \
val = COMPOBJ(_ENTRY_13, env); \
goto AFTER_LAMBDA_13; \
ENTRY_13: print_info("ENTRY_13"); \
env = COMPENVOBJ(func); \
unev = parse("nums\n"); \
env = extendEnv(unev, arglist, env); \
func = lookup(NAMEOBJ("fold-left"), env); \
val = lookup(NAMEOBJ("nums"), env); \
arglist = CONS(val, NULLOBJ); \
val = NUMOBJ(1); \
arglist = CONS(val, arglist); \
val = lookup(NAMEOBJ("_*_"), env); \
arglist = CONS(val, arglist); \
if (isPrimitive(func)) goto PRIMITIVE_15; \
if (isCompound(func)) goto COMPOUND_15; \
COMPILED_15: print_info("COMPILED_15"); \
val = COMPLABOBJ(func); \
goto COMP_LABEL; \
COMPOUND_15: print_info("COMPOUND_15"); \
save(cont); \
goto APPLY_COMPOUND; \
PRIMITIVE_15: print_info("PRIMITIVE_15"); \
val = applyPrimitive(func, arglist); \
goto CONTINUE; \
AFTER_CALL_15: print_info("AFTER_CALL_15"); \
AFTER_LAMBDA_13: print_info("AFTER_LAMBDA_13"); \
defineVar(NAMEOBJ("*"), val, env); \
val = COMPOBJ(_ENTRY_14, env); \
goto AFTER_LAMBDA_14; \
ENTRY_14: print_info("ENTRY_14"); \
env = COMPENVOBJ(func); \
unev = parse("(n)\n"); \
env = extendEnv(unev, arglist, env); \
func = lookup(NAMEOBJ("<"), env); \
val = NUMOBJ(2); \
arglist = CONS(val, NULLOBJ); \
val = lookup(NAMEOBJ("n"), env); \
arglist = CONS(val, arglist); \
val = applyPrimitive(func, arglist); \
if (isTrue(val)) goto TRUE_BRANCH_7; \
FALSE_BRANCH_7: print_info("FALSE_BRANCH_7"); \
func = lookup(NAMEOBJ("_*_"), env); \
save(cont); \
save(func); \
save(env); \
func = lookup(NAMEOBJ("recursive_factorial_compiled"), env); \
save(func); \
func = lookup(NAMEOBJ("sub1"), env); \
val = lookup(NAMEOBJ("n"), env); \
arglist = CONS(val, NULLOBJ); \
val = applyPrimitive(func, arglist); \
arglist = CONS(val, NULLOBJ); \
restore(func); \
if (isPrimitive(func)) goto PRIMITIVE_16; \
if (isCompound(func)) goto COMPOUND_16; \
COMPILED_16: print_info("COMPILED_16"); \
cont = LABELOBJ(_AFTER_CALL_16); \
val = COMPLABOBJ(func); \
goto COMP_LABEL; \
COMPOUND_16: print_info("COMPOUND_16"); \
cont = LABELOBJ(_AFTER_CALL_16); \
save(cont); \
goto APPLY_COMPOUND; \
PRIMITIVE_16: print_info("PRIMITIVE_16"); \
val = applyPrimitive(func, arglist); \
AFTER_CALL_16: print_info("AFTER_CALL_16"); \
arglist = CONS(val, NULLOBJ); \
restore(env); \
val = lookup(NAMEOBJ("n"), env); \
arglist = CONS(val, arglist); \
restore(func); \
restore(cont); \
val = applyPrimitive(func, arglist); \
goto CONTINUE; \
TRUE_BRANCH_7: print_info("TRUE_BRANCH_7"); \
val = NUMOBJ(1); \
goto CONTINUE; \
AFTER_IF_7: print_info("AFTER_IF_7"); \
AFTER_LAMBDA_14: print_info("AFTER_LAMBDA_14"); \
defineVar(NAMEOBJ("recursive_factorial_compiled"), val, env); \
val = COMPOBJ(_ENTRY_15, env); \
goto AFTER_LAMBDA_15; \
ENTRY_15: print_info("ENTRY_15"); \
env = COMPENVOBJ(func); \
unev = parse("(n)\n"); \
env = extendEnv(unev, arglist, env); \
val = COMPOBJ(_ENTRY_16, env); \
goto AFTER_LAMBDA_16; \
ENTRY_16: print_info("ENTRY_16"); \
env = COMPENVOBJ(func); \
unev = parse("(count total)\n"); \
env = extendEnv(unev, arglist, env); \
func = lookup(NAMEOBJ("<"), env); \
val = NUMOBJ(2); \
arglist = CONS(val, NULLOBJ); \
val = lookup(NAMEOBJ("count"), env); \
arglist = CONS(val, arglist); \
val = applyPrimitive(func, arglist); \
if (isTrue(val)) goto TRUE_BRANCH_8; \
FALSE_BRANCH_8: print_info("FALSE_BRANCH_8"); \
func = lookup(NAMEOBJ("loop"), env); \
save(func); \
func = lookup(NAMEOBJ("_*_"), env); \
val = lookup(NAMEOBJ("count"), env); \
arglist = CONS(val, NULLOBJ); \
val = lookup(NAMEOBJ("total"), env); \
arglist = CONS(val, arglist); \
val = applyPrimitive(func, arglist); \
arglist = CONS(val, NULLOBJ); \
save(arglist); \
func = lookup(NAMEOBJ("sub1"), env); \
val = lookup(NAMEOBJ("count"), env); \
arglist = CONS(val, NULLOBJ); \
val = applyPrimitive(func, arglist); \
restore(arglist); \
arglist = CONS(val, arglist); \
restore(func); \
if (isPrimitive(func)) goto PRIMITIVE_17; \
if (isCompound(func)) goto COMPOUND_17; \
COMPILED_17: print_info("COMPILED_17"); \
val = COMPLABOBJ(func); \
goto COMP_LABEL; \
COMPOUND_17: print_info("COMPOUND_17"); \
save(cont); \
goto APPLY_COMPOUND; \
PRIMITIVE_17: print_info("PRIMITIVE_17"); \
val = applyPrimitive(func, arglist); \
goto CONTINUE; \
AFTER_CALL_17: print_info("AFTER_CALL_17"); \
TRUE_BRANCH_8: print_info("TRUE_BRANCH_8"); \
val = lookup(NAMEOBJ("total"), env); \
goto CONTINUE; \
AFTER_IF_8: print_info("AFTER_IF_8"); \
AFTER_LAMBDA_16: print_info("AFTER_LAMBDA_16"); \
defineVar(NAMEOBJ("loop"), val, env); \
func = lookup(NAMEOBJ("loop"), env); \
val = NUMOBJ(1); \
arglist = CONS(val, NULLOBJ); \
val = lookup(NAMEOBJ("n"), env); \
arglist = CONS(val, arglist); \
if (isPrimitive(func)) goto PRIMITIVE_18; \
if (isCompound(func)) goto COMPOUND_18; \
COMPILED_18: print_info("COMPILED_18"); \
val = COMPLABOBJ(func); \
goto COMP_LABEL; \
COMPOUND_18: print_info("COMPOUND_18"); \
save(cont); \
goto APPLY_COMPOUND; \
PRIMITIVE_18: print_info("PRIMITIVE_18"); \
val = applyPrimitive(func, arglist); \
goto CONTINUE; \
AFTER_CALL_18: print_info("AFTER_CALL_18"); \
AFTER_LAMBDA_15: print_info("AFTER_LAMBDA_15"); \
defineVar(NAMEOBJ("iterative_factorial_compiled"), val, env); \
val = COMPOBJ(_ENTRY_17, env); \
goto AFTER_LAMBDA_17; \
ENTRY_17: print_info("ENTRY_17"); \
env = COMPENVOBJ(func); \
unev = parse("(n)\n"); \
env = extendEnv(unev, arglist, env); \
func = lookup(NAMEOBJ("<"), env); \
val = NUMOBJ(2); \
arglist = CONS(val, NULLOBJ); \
val = lookup(NAMEOBJ("n"), env); \
arglist = CONS(val, arglist); \
val = applyPrimitive(func, arglist); \
if (isTrue(val)) goto TRUE_BRANCH_9; \
FALSE_BRANCH_9: print_info("FALSE_BRANCH_9"); \
func = lookup(NAMEOBJ("_+_"), env); \
save(cont); \
save(func); \
save(env); \
func = lookup(NAMEOBJ("recursive_fibonacci_compiled"), env); \
save(func); \
func = lookup(NAMEOBJ("-"), env); \
val = NUMOBJ(2); \
arglist = CONS(val, NULLOBJ); \
val = lookup(NAMEOBJ("n"), env); \
arglist = CONS(val, arglist); \
val = applyPrimitive(func, arglist); \
arglist = CONS(val, NULLOBJ); \
restore(func); \
if (isPrimitive(func)) goto PRIMITIVE_20; \
if (isCompound(func)) goto COMPOUND_20; \
COMPILED_20: print_info("COMPILED_20"); \
cont = LABELOBJ(_AFTER_CALL_20); \
val = COMPLABOBJ(func); \
goto COMP_LABEL; \
COMPOUND_20: print_info("COMPOUND_20"); \
cont = LABELOBJ(_AFTER_CALL_20); \
save(cont); \
goto APPLY_COMPOUND; \
PRIMITIVE_20: print_info("PRIMITIVE_20"); \
val = applyPrimitive(func, arglist); \
AFTER_CALL_20: print_info("AFTER_CALL_20"); \
arglist = CONS(val, NULLOBJ); \
restore(env); \
save(arglist); \
func = lookup(NAMEOBJ("recursive_fibonacci_compiled"), env); \
save(func); \
func = lookup(NAMEOBJ("-"), env); \
val = NUMOBJ(1); \
arglist = CONS(val, NULLOBJ); \
val = lookup(NAMEOBJ("n"), env); \
arglist = CONS(val, arglist); \
val = applyPrimitive(func, arglist); \
arglist = CONS(val, NULLOBJ); \
restore(func); \
if (isPrimitive(func)) goto PRIMITIVE_19; \
if (isCompound(func)) goto COMPOUND_19; \
COMPILED_19: print_info("COMPILED_19"); \
cont = LABELOBJ(_AFTER_CALL_19); \
val = COMPLABOBJ(func); \
goto COMP_LABEL; \
COMPOUND_19: print_info("COMPOUND_19"); \
cont = LABELOBJ(_AFTER_CALL_19); \
save(cont); \
goto APPLY_COMPOUND; \
PRIMITIVE_19: print_info("PRIMITIVE_19"); \
val = applyPrimitive(func, arglist); \
AFTER_CALL_19: print_info("AFTER_CALL_19"); \
restore(arglist); \
arglist = CONS(val, arglist); \
restore(func); \
restore(cont); \
val = applyPrimitive(func, arglist); \
goto CONTINUE; \
TRUE_BRANCH_9: print_info("TRUE_BRANCH_9"); \
val = lookup(NAMEOBJ("n"), env); \
goto CONTINUE; \
AFTER_IF_9: print_info("AFTER_IF_9"); \
AFTER_LAMBDA_17: print_info("AFTER_LAMBDA_17"); \
defineVar(NAMEOBJ("recursive_fibonacci_compiled"), val, env); \
val = COMPOBJ(_ENTRY_18, env); \
goto AFTER_LAMBDA_18; \
ENTRY_18: print_info("ENTRY_18"); \
env = COMPENVOBJ(func); \
unev = parse("(n)\n"); \
env = extendEnv(unev, arglist, env); \
val = COMPOBJ(_ENTRY_19, env); \
goto AFTER_LAMBDA_19; \
ENTRY_19: print_info("ENTRY_19"); \
env = COMPENVOBJ(func); \
unev = parse("(count a b)\n"); \
env = extendEnv(unev, arglist, env); \
func = lookup(NAMEOBJ("one?"), env); \
val = lookup(NAMEOBJ("count"), env); \
arglist = CONS(val, NULLOBJ); \
val = applyPrimitive(func, arglist); \
if (isTrue(val)) goto TRUE_BRANCH_10; \
FALSE_BRANCH_10: print_info("FALSE_BRANCH_10"); \
func = lookup(NAMEOBJ("loop"), env); \
save(func); \
func = lookup(NAMEOBJ("_+_"), env); \
val = lookup(NAMEOBJ("b"), env); \
arglist = CONS(val, NULLOBJ); \
val = lookup(NAMEOBJ("a"), env); \
arglist = CONS(val, arglist); \
val = applyPrimitive(func, arglist); \
arglist = CONS(val, NULLOBJ); \
val = lookup(NAMEOBJ("b"), env); \
arglist = CONS(val, arglist); \
save(arglist); \
func = lookup(NAMEOBJ("sub1"), env); \
val = lookup(NAMEOBJ("count"), env); \
arglist = CONS(val, NULLOBJ); \
val = applyPrimitive(func, arglist); \
restore(arglist); \
arglist = CONS(val, arglist); \
restore(func); \
if (isPrimitive(func)) goto PRIMITIVE_21; \
if (isCompound(func)) goto COMPOUND_21; \
COMPILED_21: print_info("COMPILED_21"); \
val = COMPLABOBJ(func); \
goto COMP_LABEL; \
COMPOUND_21: print_info("COMPOUND_21"); \
save(cont); \
goto APPLY_COMPOUND; \
PRIMITIVE_21: print_info("PRIMITIVE_21"); \
val = applyPrimitive(func, arglist); \
goto CONTINUE; \
AFTER_CALL_21: print_info("AFTER_CALL_21"); \
TRUE_BRANCH_10: print_info("TRUE_BRANCH_10"); \
val = lookup(NAMEOBJ("b"), env); \
goto CONTINUE; \
AFTER_IF_10: print_info("AFTER_IF_10"); \
AFTER_LAMBDA_19: print_info("AFTER_LAMBDA_19"); \
defineVar(NAMEOBJ("loop"), val, env); \
func = lookup(NAMEOBJ("loop"), env); \
val = NUMOBJ(1); \
arglist = CONS(val, NULLOBJ); \
val = NUMOBJ(0); \
arglist = CONS(val, arglist); \
val = lookup(NAMEOBJ("n"), env); \
arglist = CONS(val, arglist); \
if (isPrimitive(func)) goto PRIMITIVE_22; \
if (isCompound(func)) goto COMPOUND_22; \
COMPILED_22: print_info("COMPILED_22"); \
val = COMPLABOBJ(func); \
goto COMP_LABEL; \
COMPOUND_22: print_info("COMPOUND_22"); \
save(cont); \
goto APPLY_COMPOUND; \
PRIMITIVE_22: print_info("PRIMITIVE_22"); \
val = applyPrimitive(func, arglist); \
goto CONTINUE; \
AFTER_CALL_22: print_info("AFTER_CALL_22"); \
AFTER_LAMBDA_18: print_info("AFTER_LAMBDA_18"); \
defineVar(NAMEOBJ("iterative_fibonacci_compiled"), val, env); \
val = lookup(NAMEOBJ("iterative_factorial_compiled"), env); \
defineVar(NAMEOBJ("factorial"), val, env); \
val = lookup(NAMEOBJ("iterative_fibonacci_compiled"), env); \
defineVar(NAMEOBJ("fibonacci"), val, env); \
goto DONE;

#define COMP_CONT(REG) \
if (GETLABEL(REG) == _ENTRY_1) goto ENTRY_1; \
if (GETLABEL(REG) == _AFTER_LAMBDA_1) goto AFTER_LAMBDA_1; \
if (GETLABEL(REG) == _ENTRY_2) goto ENTRY_2; \
if (GETLABEL(REG) == _AFTER_LAMBDA_2) goto AFTER_LAMBDA_2; \
if (GETLABEL(REG) == _ENTRY_3) goto ENTRY_3; \
if (GETLABEL(REG) == _AFTER_LAMBDA_3) goto AFTER_LAMBDA_3; \
if (GETLABEL(REG) == _TRUE_BRANCH_1) goto TRUE_BRANCH_1; \
if (GETLABEL(REG) == _FALSE_BRANCH_1) goto FALSE_BRANCH_1; \
if (GETLABEL(REG) == _AFTER_IF_1) goto AFTER_IF_1; \
if (GETLABEL(REG) == _PRIMITIVE_1) goto PRIMITIVE_1; \
if (GETLABEL(REG) == _COMPOUND_1) goto COMPOUND_1; \
if (GETLABEL(REG) == _COMPILED_1) goto COMPILED_1; \
if (GETLABEL(REG) == _AFTER_CALL_1) goto AFTER_CALL_1; \
if (GETLABEL(REG) == _PRIMITIVE_2) goto PRIMITIVE_2; \
if (GETLABEL(REG) == _COMPOUND_2) goto COMPOUND_2; \
if (GETLABEL(REG) == _COMPILED_2) goto COMPILED_2; \
if (GETLABEL(REG) == _AFTER_CALL_2) goto AFTER_CALL_2; \
if (GETLABEL(REG) == _ENTRY_4) goto ENTRY_4; \
if (GETLABEL(REG) == _AFTER_LAMBDA_4) goto AFTER_LAMBDA_4; \
if (GETLABEL(REG) == _TRUE_BRANCH_2) goto TRUE_BRANCH_2; \
if (GETLABEL(REG) == _FALSE_BRANCH_2) goto FALSE_BRANCH_2; \
if (GETLABEL(REG) == _AFTER_IF_2) goto AFTER_IF_2; \
if (GETLABEL(REG) == _PRIMITIVE_3) goto PRIMITIVE_3; \
if (GETLABEL(REG) == _COMPOUND_3) goto COMPOUND_3; \
if (GETLABEL(REG) == _COMPILED_3) goto COMPILED_3; \
if (GETLABEL(REG) == _AFTER_CALL_3) goto AFTER_CALL_3; \
if (GETLABEL(REG) == _ENTRY_5) goto ENTRY_5; \
if (GETLABEL(REG) == _AFTER_LAMBDA_5) goto AFTER_LAMBDA_5; \
if (GETLABEL(REG) == _TRUE_BRANCH_3) goto TRUE_BRANCH_3; \
if (GETLABEL(REG) == _FALSE_BRANCH_3) goto FALSE_BRANCH_3; \
if (GETLABEL(REG) == _AFTER_IF_3) goto AFTER_IF_3; \
if (GETLABEL(REG) == _PRIMITIVE_4) goto PRIMITIVE_4; \
if (GETLABEL(REG) == _COMPOUND_4) goto COMPOUND_4; \
if (GETLABEL(REG) == _COMPILED_4) goto COMPILED_4; \
if (GETLABEL(REG) == _AFTER_CALL_4) goto AFTER_CALL_4; \
if (GETLABEL(REG) == _ENTRY_6) goto ENTRY_6; \
if (GETLABEL(REG) == _AFTER_LAMBDA_6) goto AFTER_LAMBDA_6; \
if (GETLABEL(REG) == _ENTRY_7) goto ENTRY_7; \
if (GETLABEL(REG) == _AFTER_LAMBDA_7) goto AFTER_LAMBDA_7; \
if (GETLABEL(REG) == _TRUE_BRANCH_4) goto TRUE_BRANCH_4; \
if (GETLABEL(REG) == _FALSE_BRANCH_4) goto FALSE_BRANCH_4; \
if (GETLABEL(REG) == _AFTER_IF_4) goto AFTER_IF_4; \
if (GETLABEL(REG) == _PRIMITIVE_5) goto PRIMITIVE_5; \
if (GETLABEL(REG) == _COMPOUND_5) goto COMPOUND_5; \
if (GETLABEL(REG) == _COMPILED_5) goto COMPILED_5; \
if (GETLABEL(REG) == _AFTER_CALL_5) goto AFTER_CALL_5; \
if (GETLABEL(REG) == _PRIMITIVE_6) goto PRIMITIVE_6; \
if (GETLABEL(REG) == _COMPOUND_6) goto COMPOUND_6; \
if (GETLABEL(REG) == _COMPILED_6) goto COMPILED_6; \
if (GETLABEL(REG) == _AFTER_CALL_6) goto AFTER_CALL_6; \
if (GETLABEL(REG) == _ENTRY_8) goto ENTRY_8; \
if (GETLABEL(REG) == _AFTER_LAMBDA_8) goto AFTER_LAMBDA_8; \
if (GETLABEL(REG) == _ENTRY_9) goto ENTRY_9; \
if (GETLABEL(REG) == _AFTER_LAMBDA_9) goto AFTER_LAMBDA_9; \
if (GETLABEL(REG) == _TRUE_BRANCH_5) goto TRUE_BRANCH_5; \
if (GETLABEL(REG) == _FALSE_BRANCH_5) goto FALSE_BRANCH_5; \
if (GETLABEL(REG) == _AFTER_IF_5) goto AFTER_IF_5; \
if (GETLABEL(REG) == _PRIMITIVE_7) goto PRIMITIVE_7; \
if (GETLABEL(REG) == _COMPOUND_7) goto COMPOUND_7; \
if (GETLABEL(REG) == _COMPILED_7) goto COMPILED_7; \
if (GETLABEL(REG) == _AFTER_CALL_7) goto AFTER_CALL_7; \
if (GETLABEL(REG) == _PRIMITIVE_8) goto PRIMITIVE_8; \
if (GETLABEL(REG) == _COMPOUND_8) goto COMPOUND_8; \
if (GETLABEL(REG) == _COMPILED_8) goto COMPILED_8; \
if (GETLABEL(REG) == _AFTER_CALL_8) goto AFTER_CALL_8; \
if (GETLABEL(REG) == _PRIMITIVE_9) goto PRIMITIVE_9; \
if (GETLABEL(REG) == _COMPOUND_9) goto COMPOUND_9; \
if (GETLABEL(REG) == _COMPILED_9) goto COMPILED_9; \
if (GETLABEL(REG) == _AFTER_CALL_9) goto AFTER_CALL_9; \
if (GETLABEL(REG) == _PRIMITIVE_10) goto PRIMITIVE_10; \
if (GETLABEL(REG) == _COMPOUND_10) goto COMPOUND_10; \
if (GETLABEL(REG) == _COMPILED_10) goto COMPILED_10; \
if (GETLABEL(REG) == _AFTER_CALL_10) goto AFTER_CALL_10; \
if (GETLABEL(REG) == _ENTRY_10) goto ENTRY_10; \
if (GETLABEL(REG) == _AFTER_LAMBDA_10) goto AFTER_LAMBDA_10; \
if (GETLABEL(REG) == _ENTRY_11) goto ENTRY_11; \
if (GETLABEL(REG) == _AFTER_LAMBDA_11) goto AFTER_LAMBDA_11; \
if (GETLABEL(REG) == _TRUE_BRANCH_6) goto TRUE_BRANCH_6; \
if (GETLABEL(REG) == _FALSE_BRANCH_6) goto FALSE_BRANCH_6; \
if (GETLABEL(REG) == _AFTER_IF_6) goto AFTER_IF_6; \
if (GETLABEL(REG) == _PRIMITIVE_11) goto PRIMITIVE_11; \
if (GETLABEL(REG) == _COMPOUND_11) goto COMPOUND_11; \
if (GETLABEL(REG) == _COMPILED_11) goto COMPILED_11; \
if (GETLABEL(REG) == _AFTER_CALL_11) goto AFTER_CALL_11; \
if (GETLABEL(REG) == _PRIMITIVE_12) goto PRIMITIVE_12; \
if (GETLABEL(REG) == _COMPOUND_12) goto COMPOUND_12; \
if (GETLABEL(REG) == _COMPILED_12) goto COMPILED_12; \
if (GETLABEL(REG) == _AFTER_CALL_12) goto AFTER_CALL_12; \
if (GETLABEL(REG) == _PRIMITIVE_13) goto PRIMITIVE_13; \
if (GETLABEL(REG) == _COMPOUND_13) goto COMPOUND_13; \
if (GETLABEL(REG) == _COMPILED_13) goto COMPILED_13; \
if (GETLABEL(REG) == _AFTER_CALL_13) goto AFTER_CALL_13; \
if (GETLABEL(REG) == _ENTRY_12) goto ENTRY_12; \
if (GETLABEL(REG) == _AFTER_LAMBDA_12) goto AFTER_LAMBDA_12; \
if (GETLABEL(REG) == _PRIMITIVE_14) goto PRIMITIVE_14; \
if (GETLABEL(REG) == _COMPOUND_14) goto COMPOUND_14; \
if (GETLABEL(REG) == _COMPILED_14) goto COMPILED_14; \
if (GETLABEL(REG) == _AFTER_CALL_14) goto AFTER_CALL_14; \
if (GETLABEL(REG) == _ENTRY_13) goto ENTRY_13; \
if (GETLABEL(REG) == _AFTER_LAMBDA_13) goto AFTER_LAMBDA_13; \
if (GETLABEL(REG) == _PRIMITIVE_15) goto PRIMITIVE_15; \
if (GETLABEL(REG) == _COMPOUND_15) goto COMPOUND_15; \
if (GETLABEL(REG) == _COMPILED_15) goto COMPILED_15; \
if (GETLABEL(REG) == _AFTER_CALL_15) goto AFTER_CALL_15; \
if (GETLABEL(REG) == _ENTRY_14) goto ENTRY_14; \
if (GETLABEL(REG) == _AFTER_LAMBDA_14) goto AFTER_LAMBDA_14; \
if (GETLABEL(REG) == _TRUE_BRANCH_7) goto TRUE_BRANCH_7; \
if (GETLABEL(REG) == _FALSE_BRANCH_7) goto FALSE_BRANCH_7; \
if (GETLABEL(REG) == _AFTER_IF_7) goto AFTER_IF_7; \
if (GETLABEL(REG) == _PRIMITIVE_16) goto PRIMITIVE_16; \
if (GETLABEL(REG) == _COMPOUND_16) goto COMPOUND_16; \
if (GETLABEL(REG) == _COMPILED_16) goto COMPILED_16; \
if (GETLABEL(REG) == _AFTER_CALL_16) goto AFTER_CALL_16; \
if (GETLABEL(REG) == _ENTRY_15) goto ENTRY_15; \
if (GETLABEL(REG) == _AFTER_LAMBDA_15) goto AFTER_LAMBDA_15; \
if (GETLABEL(REG) == _ENTRY_16) goto ENTRY_16; \
if (GETLABEL(REG) == _AFTER_LAMBDA_16) goto AFTER_LAMBDA_16; \
if (GETLABEL(REG) == _TRUE_BRANCH_8) goto TRUE_BRANCH_8; \
if (GETLABEL(REG) == _FALSE_BRANCH_8) goto FALSE_BRANCH_8; \
if (GETLABEL(REG) == _AFTER_IF_8) goto AFTER_IF_8; \
if (GETLABEL(REG) == _PRIMITIVE_17) goto PRIMITIVE_17; \
if (GETLABEL(REG) == _COMPOUND_17) goto COMPOUND_17; \
if (GETLABEL(REG) == _COMPILED_17) goto COMPILED_17; \
if (GETLABEL(REG) == _AFTER_CALL_17) goto AFTER_CALL_17; \
if (GETLABEL(REG) == _PRIMITIVE_18) goto PRIMITIVE_18; \
if (GETLABEL(REG) == _COMPOUND_18) goto COMPOUND_18; \
if (GETLABEL(REG) == _COMPILED_18) goto COMPILED_18; \
if (GETLABEL(REG) == _AFTER_CALL_18) goto AFTER_CALL_18; \
if (GETLABEL(REG) == _ENTRY_17) goto ENTRY_17; \
if (GETLABEL(REG) == _AFTER_LAMBDA_17) goto AFTER_LAMBDA_17; \
if (GETLABEL(REG) == _TRUE_BRANCH_9) goto TRUE_BRANCH_9; \
if (GETLABEL(REG) == _FALSE_BRANCH_9) goto FALSE_BRANCH_9; \
if (GETLABEL(REG) == _AFTER_IF_9) goto AFTER_IF_9; \
if (GETLABEL(REG) == _PRIMITIVE_19) goto PRIMITIVE_19; \
if (GETLABEL(REG) == _COMPOUND_19) goto COMPOUND_19; \
if (GETLABEL(REG) == _COMPILED_19) goto COMPILED_19; \
if (GETLABEL(REG) == _AFTER_CALL_19) goto AFTER_CALL_19; \
if (GETLABEL(REG) == _PRIMITIVE_20) goto PRIMITIVE_20; \
if (GETLABEL(REG) == _COMPOUND_20) goto COMPOUND_20; \
if (GETLABEL(REG) == _COMPILED_20) goto COMPILED_20; \
if (GETLABEL(REG) == _AFTER_CALL_20) goto AFTER_CALL_20; \
if (GETLABEL(REG) == _ENTRY_18) goto ENTRY_18; \
if (GETLABEL(REG) == _AFTER_LAMBDA_18) goto AFTER_LAMBDA_18; \
if (GETLABEL(REG) == _ENTRY_19) goto ENTRY_19; \
if (GETLABEL(REG) == _AFTER_LAMBDA_19) goto AFTER_LAMBDA_19; \
if (GETLABEL(REG) == _TRUE_BRANCH_10) goto TRUE_BRANCH_10; \
if (GETLABEL(REG) == _FALSE_BRANCH_10) goto FALSE_BRANCH_10; \
if (GETLABEL(REG) == _AFTER_IF_10) goto AFTER_IF_10; \
if (GETLABEL(REG) == _PRIMITIVE_21) goto PRIMITIVE_21; \
if (GETLABEL(REG) == _COMPOUND_21) goto COMPOUND_21; \
if (GETLABEL(REG) == _COMPILED_21) goto COMPILED_21; \
if (GETLABEL(REG) == _AFTER_CALL_21) goto AFTER_CALL_21; \
if (GETLABEL(REG) == _PRIMITIVE_22) goto PRIMITIVE_22; \
if (GETLABEL(REG) == _COMPOUND_22) goto COMPOUND_22; \
if (GETLABEL(REG) == _COMPILED_22) goto COMPILED_22; \
if (GETLABEL(REG) == _AFTER_CALL_22) goto AFTER_CALL_22;

#define ALL_COMPILED_LABELS \
_ENTRY_1, \
_AFTER_LAMBDA_1, \
_ENTRY_2, \
_AFTER_LAMBDA_2, \
_ENTRY_3, \
_AFTER_LAMBDA_3, \
_TRUE_BRANCH_1, \
_FALSE_BRANCH_1, \
_AFTER_IF_1, \
_PRIMITIVE_1, \
_COMPOUND_1, \
_COMPILED_1, \
_AFTER_CALL_1, \
_PRIMITIVE_2, \
_COMPOUND_2, \
_COMPILED_2, \
_AFTER_CALL_2, \
_ENTRY_4, \
_AFTER_LAMBDA_4, \
_TRUE_BRANCH_2, \
_FALSE_BRANCH_2, \
_AFTER_IF_2, \
_PRIMITIVE_3, \
_COMPOUND_3, \
_COMPILED_3, \
_AFTER_CALL_3, \
_ENTRY_5, \
_AFTER_LAMBDA_5, \
_TRUE_BRANCH_3, \
_FALSE_BRANCH_3, \
_AFTER_IF_3, \
_PRIMITIVE_4, \
_COMPOUND_4, \
_COMPILED_4, \
_AFTER_CALL_4, \
_ENTRY_6, \
_AFTER_LAMBDA_6, \
_ENTRY_7, \
_AFTER_LAMBDA_7, \
_TRUE_BRANCH_4, \
_FALSE_BRANCH_4, \
_AFTER_IF_4, \
_PRIMITIVE_5, \
_COMPOUND_5, \
_COMPILED_5, \
_AFTER_CALL_5, \
_PRIMITIVE_6, \
_COMPOUND_6, \
_COMPILED_6, \
_AFTER_CALL_6, \
_ENTRY_8, \
_AFTER_LAMBDA_8, \
_ENTRY_9, \
_AFTER_LAMBDA_9, \
_TRUE_BRANCH_5, \
_FALSE_BRANCH_5, \
_AFTER_IF_5, \
_PRIMITIVE_7, \
_COMPOUND_7, \
_COMPILED_7, \
_AFTER_CALL_7, \
_PRIMITIVE_8, \
_COMPOUND_8, \
_COMPILED_8, \
_AFTER_CALL_8, \
_PRIMITIVE_9, \
_COMPOUND_9, \
_COMPILED_9, \
_AFTER_CALL_9, \
_PRIMITIVE_10, \
_COMPOUND_10, \
_COMPILED_10, \
_AFTER_CALL_10, \
_ENTRY_10, \
_AFTER_LAMBDA_10, \
_ENTRY_11, \
_AFTER_LAMBDA_11, \
_TRUE_BRANCH_6, \
_FALSE_BRANCH_6, \
_AFTER_IF_6, \
_PRIMITIVE_11, \
_COMPOUND_11, \
_COMPILED_11, \
_AFTER_CALL_11, \
_PRIMITIVE_12, \
_COMPOUND_12, \
_COMPILED_12, \
_AFTER_CALL_12, \
_PRIMITIVE_13, \
_COMPOUND_13, \
_COMPILED_13, \
_AFTER_CALL_13, \
_ENTRY_12, \
_AFTER_LAMBDA_12, \
_PRIMITIVE_14, \
_COMPOUND_14, \
_COMPILED_14, \
_AFTER_CALL_14, \
_ENTRY_13, \
_AFTER_LAMBDA_13, \
_PRIMITIVE_15, \
_COMPOUND_15, \
_COMPILED_15, \
_AFTER_CALL_15, \
_ENTRY_14, \
_AFTER_LAMBDA_14, \
_TRUE_BRANCH_7, \
_FALSE_BRANCH_7, \
_AFTER_IF_7, \
_PRIMITIVE_16, \
_COMPOUND_16, \
_COMPILED_16, \
_AFTER_CALL_16, \
_ENTRY_15, \
_AFTER_LAMBDA_15, \
_ENTRY_16, \
_AFTER_LAMBDA_16, \
_TRUE_BRANCH_8, \
_FALSE_BRANCH_8, \
_AFTER_IF_8, \
_PRIMITIVE_17, \
_COMPOUND_17, \
_COMPILED_17, \
_AFTER_CALL_17, \
_PRIMITIVE_18, \
_COMPOUND_18, \
_COMPILED_18, \
_AFTER_CALL_18, \
_ENTRY_17, \
_AFTER_LAMBDA_17, \
_TRUE_BRANCH_9, \
_FALSE_BRANCH_9, \
_AFTER_IF_9, \
_PRIMITIVE_19, \
_COMPOUND_19, \
_COMPILED_19, \
_AFTER_CALL_19, \
_PRIMITIVE_20, \
_COMPOUND_20, \
_COMPILED_20, \
_AFTER_CALL_20, \
_ENTRY_18, \
_AFTER_LAMBDA_18, \
_ENTRY_19, \
_AFTER_LAMBDA_19, \
_TRUE_BRANCH_10, \
_FALSE_BRANCH_10, \
_AFTER_IF_10, \
_PRIMITIVE_21, \
_COMPOUND_21, \
_COMPILED_21, \
_AFTER_CALL_21, \
_PRIMITIVE_22, \
_COMPOUND_22, \
_COMPILED_22, \
_AFTER_CALL_22

#endif
