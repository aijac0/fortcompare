# Fortran Regression Testing Tool (FRTT)
A tool to mitigate the amount of behavior changed between two implementations of the same Fortran codebase.
Still a work in progress.

## Usage
1. Create a .yaml file similar to the one given in examples/arpack
2. Call "python3 src/fortcompare.py [yaml-file]"

## Overview
FRTT has three main phases: static analysis, dynamic analysis, and code generation.

### Static Analysis
The static analyzer is responsible for finding the similar subprograms[^1] between each implementation, as well as the external variables and subprograms that are referenced by each.
Input:
- Source files
Output:
- Serialized information

### Dynamic Analysis
The dynamic analyzer is responsible for getting empirical examples of the state of all variables referenced in each subprogram prior to its execution.
Input:
- Source files
- Implementation inputs
- Serialized information
Output:
- Serialized input states

### Code Generation
The code generator is responsible for creating a minimal complete implementation[^4] for each similar subprogram[^1], and unit tests that iteratively compare the output states[^3] when executed on the same input state[^1].
Input:
- Source files
- Serialized information
- Serialized input states
Output:
- Minimal complete implementations
- Unit tests

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

[^4]: A *minimal complete subimplementation* of a subprogram is the smallest static library that, when dynamically linked to an implementation of the subprogram, allow its execution.