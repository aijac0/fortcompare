# Fortran Regression Testing Tool (FRTT)
* FRTT is a tool to mitigate the amount of behavior changed between two implementations of the same Fortran codebase.
* Still a work in progress.

## Usage
1. Build with boost library
2. ./frtt [source_directory_1] [source_directory_2] ... [source_directory_n]

## Overview
* FRTT automagically generates a test for each similar subprogram[^1]. Each test will retrieve a known input state[^2], execute both subprogram implementations, and compare the output states[^3] of each.
* FRTT has three main phases: static analysis, dynamic analysis, and code generation.

### Static Analysis
* This phase is responsible for getting an abstraction of the structure of each implementation, such that its substructures can be compared to another implementation.
* This phase has two subphases: initialization, parsing and resolution.
* Input: 
  - TODO
* Output: 
  - TODO

#### Initialization
* This phase is responsible for getting the paths to the source files in each implementation.
* Input:
  - Implementation source directory paths
* Output:
  - Implementation source file paths

#### Parsing
* This phase is responsible for finding the structure of each implementation that can be interpreted from its individual source files.
* Input:
  - TODO
* Output:
  - TODO

#### Resolution
* This phase is responsible for finding the structure of each implementation as a whole.
* Input:
  - TODO
* Output:
  - TODO

### Dynamic Analysis
* The dynamic analyzer is responsible for getting empirical examples of the state of all variables referenced in each subprogram prior to its execution.
* Input:
  - Source files
  - Implementation inputs
  - Serialized information
* Output:
  - Serialized input states

### Code Generation
* The code generator is responsible for creating a minimal complete implementation[^4] for each similar subprogram[^1], and unit tests that iteratively compare the output states[^3] when executed on the same input state[^1].
* Input:
  - Source files
  - Serialized information
  - Serialized input states
* Output:
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