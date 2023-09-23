from frtt.utilities.types.generic import Program
from frtt.static_analysis.parsing import parsing
from frtt.static_analysis.resolution import resolution
from frtt.static_analysis.isomorphism import isomorphism

def static_analysis(filepaths1 : list[str], filepaths2 : list[str]) -> tuple[Program, Program, dict]:

    # Run the parsing phase
    program1 = parsing(filepaths1)
    program2 = parsing(filepaths2)
    
    # Run the resolution phase
    resolution(program1)
    resolution(program2)
    
    # Run the isomorphism phase
    mapping = isomorphism(program1, program2)
    
    return program1, program2, mapping