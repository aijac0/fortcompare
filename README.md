# Fortran Regression Testing Tool (FRTT)

## Description

### Project Overview

The goal of Fortran Regression Testing Tool (FRTT) is to find a pragmatic method of quantifying the difference in behavior between two implementations[^1] of the same Fortran program. The rough description of my current method is to create tests that compare the behavior of every pair of similar subimplementations[^4].
Each test will retrieve a known input state[^5], execute each subimplementation[^2], and compare the output states[^6] of each.

### Input

* Two sets of source files, each representing an implementation of the same program. As of right now, I am assuming that there is complete access to the source files that comprise each implementation. Such an implementation will be called a complete implementation[^3]. In theory, it should be possible to compile and link a complete implementation into a valid executable without the need of external libraries.
* A set of input examples that result in the successful execution of both implementations. Input examples should be chosen as real examples that would be used in the program, and such that they cause the entirety of the program to be executed.

### Output

The output to FRTT will be a float in the range [0, 1]. An output of 0 signifies that the two implementations are opposite, and should be impossible with an ideal method for quantifying the similarity. An output of 1 signifies that the two implementations are identical. The method for determining this value will be described later.

### Similarity between Subimplementations

Roughly speaking, two subimplementations are similar if they have the structure of their input and output states are the same. In the context of functions, this would be realized as having same signature, assuming no external state. As a more formal definition, two subimplementations are similar if there is some bijective map between their input states, as well as a bijective map between their output states. Two subimplementations being similar is the criteria for making a test that compares them.

### Determining Input States

Ideally, the entire lifecycle of FRTT should be possible without context about the two implementations, besides what is given as input examples to the program. Therefore, input states for each similar subimplementation are gathered by executing one or both implementations on the input examples with a debugger. Prior to each time the subimplementation gets executed, the state of all the data that comprise its input state will be retrieved and stored.

### Quantifying the Similarity

A test is generated that iteratively retrieves an input state, executes each subimplementation, and stores the output states. The current method for quantifying the similarity is to take the average of the ratios between each value in each output state, taking the ratio that is less than or equal to 1. If both values being compared are 0, it will contribute a 1 to the average. Note that this method would allow for a quantified similarity of 0 if exactly one value is 0. The quantified similarity of two implementations is just the average of the quantified similarities of its subimplementations.

## Implementation

### Implementation Overview

FRTT has three main phases: static analysis, dynamic analysis, and code generation.

### Assumptions & Constraints

1. The only subimplementations that will be compared are functions and subroutines
2. An additional requirement for subimplementations to be similar is that they have the same signature, and their external states are objects that have the same declaration
3. Both implementations are complete
4. Both implementations given as input are similar
5. Both implementations given as input are represented by a function call, whose input examples are used as direct arguments

### Static Analysis

This phase is responsible for parsing and interpreting information that can be gathered from the implementation source files. It is during this phase that all similar subimplementations are found. It begins by parsing each source file into an abstract syntax tree. Each subtree representing a programunit (function, subroutine, or module) is then parsed for its declarations and references to variables, common blocks, and other sub-programunits. These declarations and references represent the abstract structure of the programunit. The references in each programunit is then resolved to the declarations in another programunit, so they point to the same object. At this point, an incomplete implementation would fail because it would contain references to declarations that do not exist. The task of determining whether two programunits are similar is essentially a graph isomorphism problem with nodes as variables, common blocks, sub-programunits and edges as references to these objects. This may be a large hindrance to a pure implementation of FRTT, where the names associated with declarations are not considered.

* Input:
  * Two sets of source files representing complete implementations
* Output:
  * Abstract syntax tree for each programunit
  * Abstract structure of each programunit, with resolved references
  * Mapping between the programunits in one implementation and the programunits in the other, which may or may surjective

### Dynamic Analysis

This phase is responsible for getting the set of input states for each set of similar subimplementations. Each implementation is iteratively executed on each input example using a debugger that is capable of retrieving the state of variables and common blocks when a breakpoint is triggered. These breakpoints will be set at the beginning of each subimplementation. By assumption 2, the input state of one subimplementation for is the input state for its similar subimplementations, without the need of a non-trivial bijective map.

* Input:
  * Abstract structure of each programunit, with resolved references
  * Mapping between the programunits in one implementation and the programunits in the other, which may or may not be surjective
* Output:
  * Mapping between each pair of similar programunits and the set of input states for them

### Code Generation

This phase is responsible for creating testable representations for each pair of similar subimplementations, and creating a test that performs the comparison as outlined earlier. Simply linking both implementations together would result in namespace conflicts. The solution is to dynamically link and unlink each implementation such that only the implementation currently being executed is linked to the test executable. For the sake of efficiency, a minimal complete subimplementation[^7] is ideal. Such an implementation will contain the smallest set of definitions that allow the execution of the programunit in a subimplementation. This may include definitions of the modules and sub-programunits referenced by the programunit. To minimize overlap between tests, definitions to sub-programunits will be mocked so that they trivially set their output states to zero. Additionally, all module definitions should contain only the definitions for variables that are referenced by the subimplementation and are hence a part of its input or output. By assumption 2, such a set of definitions will be identical. Therefore, the only difference between the minimal complete subimplementations is the definition of the programunit to be tested. Such a case would allow each test to be statically linked to the pieces of the minimal complete subimplementation that exclude the definition for the programunit to be tested. Then only the programunits to be tested needs to be put in individual dynamic libraries and linked at runtime. The functionality of the test itself is as follows:

1. For each pair of similar subimplementations:
    1. For each input state:
        1. For each subimplementation:
            1. The subimplementation is dynamically linked to the executable
            2. The input state is retrieved by setting the external state and the variables to be used as direct arguments
            3. The subimplementation is executed
            4. The output state is stored by getting the external state and the return values
        2. The quantified similarity is calculated for this pair of output states
    2. The quantified similarity is calculated by taking the average of all of its pairs of output states
2. The quantified similarity is calculated by taking the average of all of its pairs of similar subimplementations

* Input:
  * Abstract syntax tree for each programunit
  * Abstract structure of each programunit, with resolved references
  * Mapping between the programunits in one implementation and the programunits in the other, which may or may not be surjective
  * Mapping between each pair of similar programunits and the set of input states for them
* Output:
  * Source files that comprise all of the minimal complete subimplementations
  * Source files that comprise the test program

---

[^1]: An *implementation* is a sequence of executable instructions and the data that it manipulates. This can be represented by any source code is compilable.

[^2]: A *subimplementation* is a subset of the instructions and the data in an implementation.

[^3]: A *complete subimplementation* is a subimplementation which for every executable instruction that references a piece of data, there is an executable instruction that declares the piece of data.

[^4]: Two subimplementations are *similar* if there is a bijective function mapping their set of all input states to eachother, and if there is a bijective function mapping their set of all output states to eachother.

[^5]: An *input state* is the data in a subimplementation which has an executable instruction referencing it before it is defined by one of its executable instructions.

[^6]: An *output state* is the data in a subimplementation which has an executable instruction manipulating it before it by one of its executable instructions. An additional requirement is that each piece of data has a ratio operation defined that gives a real in the range [0, 1] that meaningfully quantifies its similarity.

[^7]: A *minimal complete subimplementation* is a complete subimplementation which has no proper subimplementation of itself that is complete.
