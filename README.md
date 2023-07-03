# FortCompare
A tool to mitigate the amount of behavior changed between two implementations of the same Fortran codebase.
Still a work in progress.

## Usage
1. Create a .yaml file similar to the one given in examples/arpack
2. Call "python3 src/fortcompare.py [yaml-file]"

## Behavior
Automagically generate a test for each similar subprogram[^1]. Each test will retrieve a known input state[^2], execute both subprogram implementations,
and compare the output states[^3] of each.

[^1]: Two subprograms are *similar* if the following is true:
    1. The subprogram type (function or subroutine) is the same.
    2. The return variable is the same.
    3. The argument variables are the same.
    4. The external variables referenced are the same and each come from the same module.
    5. The subprograms referenced are similar.

[^2]: An *input state* of a subprogram is an empirical example of the state of all external variables and common blocks referenced by the subprogram, taken prior to
    the execution of the subprogram.

[^3]: An *output state* of a subprogram is an empirical example of the state of all external variables and common blocks referenced by the subprogram, taken after
    the execution of the subprogram.