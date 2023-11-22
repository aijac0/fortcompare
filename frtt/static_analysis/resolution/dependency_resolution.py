from utilities.types.generic import Program, ProgramUnit


def resolve_dependencies(program : Program):
    """
    Resolve the depenendencies between each ProgramUnit in a Program.
    Sets the attribute of program that represents the dependency graph of its program units.
    Each program unit gets mapped to the program units that it depends on for linking and execution.
        
    Args:
        program (Program): Object representation of a program
    """
    
    
    # Iterate over each programunit
    
    
    # Depth first search dependencies
    stack = []
    stack.extend(program.declared_programunits)
    while stack:
        curr = stack.pop()
        
        # Iterate over each referenced module
        for module in curr.referenced_modules:
            pass
        
        # Iterate over each referenced procedure
        for procedure in curr.referenced_procedures:
            pass
    
    # Iterate over each programunit
    for programunit in program.declared_programunits:
        pass
    