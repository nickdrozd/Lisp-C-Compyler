# Lisp-C-Compyler
Lisp-to-C compiler written in Python. Based on the compiler presented in SICP chapter 5!

INSTRUCTIONS: Call with "python3 compyle.py" from the command line. Then watch the code fly by!

This "compyler" (yeah, I hate that kind of thing too) compiles Lisp (Scheme) expressions into assembly-like C. Like most compiled code, this C code is highly context-dependent. In this case, the compiled code is intended to run in concert with lispinc (https://github.com/nickdrozd/lispinc). lispinc is itself to demonstrate how Lisp can be implemented at a primitive machine level. The actual output of the compiler doesn't make much sense outside of this context, but it could probably be adapted to a different setting without too much difficulty.

compyle.py contains the main function. See there for use details.

TODO:
* Documentation!
* Figure out how to file I/O (especially O)
* Make style more "pythonic", especially converting recursion to iteration
* rework instruction sequences so that information about registers needed and modified can be extracted from the instruction strings themselves. that would make comipledDisp a lot cleaner (but would it adversely affect adaptability?). 
