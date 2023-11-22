from utilities.types.generic import Program
from static_analysis.parsing.abstract_syntax_tree import get_abstract_syntax_tree
from static_analysis.parsing.tree_parsing import parse_program

def parsing(filepaths : list[str]) -> Program:
    """ 
    Parse the source files in a program for its abstract structure.

    Args:
        filepaths (list[str]): List of the paths to each source file in a program

    Returns:
        program (Program): Object representation of a program
    """
     
    # Initialize return values
    program = Program()

    # Iterate over each filepath
    for filepath in filepaths:
        
        # Generate the abstract syntax tree for the source file
        tree = get_abstract_syntax_tree(filepath)
        
        # Parse the programunits from the source file
        parsed_programunits = parse_program(tree)
        
        # Add parsed programunits to list
        while parsed_programunits:
            punit = parsed_programunits.pop()
            punit.filepath = filepath
            parsed_programunits.extend(punit.declared_procedures)
            program.declared_programunits.append(punit)

            # Add mapping to programunit
            if punit.parent is None:
                if punit.type == "module":
                    program.declared_modules_map[punit.name] = punit
                else:
                    program.declared_procedures_map[punit.name] = punit 
                
    return program