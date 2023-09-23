from queue import Queue
from frtt.utilities.types.generic import Program, ProgramUnit, Variable

def resolve_variables(program : Program):
    """
    Resolve the variable references
        
    Args:
        program (Program): Object representation of a program
        
    Assumptions:
        1. Implicit variables are not used 
    """

    # Iterate over each programunit
    for programunit in program.declared_programunits:
            
        # Iterate over each variable reference
        for variable_reference in programunit.referenced_names:
            
            # Search the local scope hierarchy for variable declaration
            variable_declaration = __search_local(programunit, variable_reference)
            if variable_declaration is not None:
                programunit.referenced_variables.append(variable_declaration)
                continue
            
            # Search the global scope for variable declaration
            variable_declaration = __search_global(program, variable_reference)
            if variable_declaration is not None:
                programunit.referenced_variables.append(variable_declaration)
                continue
            
            # Variable declaration was not found
            #print("Variable not found: {}".format(variable_reference))
            #error_msg = "No declaration found for the variable {} that is referenced in the {} {}"
            #raise Exception(error_msg.format(variable_reference, programunit.type, programunit.name))
                
                
def __search_local(curr : ProgramUnit, variable_reference : str, visited : set[ProgramUnit] = None) -> Variable:
    """
    Search the local scope hierarchy for a variable declaration
    Backtracks the local scope hierarchy until end is reached or declaration is found
    BFS to search each local scope, and the scopes of any directly or indirectly referenced modules

    Args:
        curr (ProgramUnit): Current local scope
        variable_reference (str): Variable reference
        visited (set[ProgramUnit], optional): ProgramUnits that have already been searched. Defaults to None.

    Returns:
        Variable: Variable declaration, or None if not found
        
    Assumptions:
        1. Modules can only be declared at the global scope
    """
    
    # Entire local scope hierarchy was searched
    if curr is None: return None

    # Initialize set of visited programunits
    if visited is None: visited = set()
    
    # Breadth first search the current local scope and the local scope of each directly or indirectly referenced module
    queue = Queue()
    queue.put(curr)
    while not queue.empty():
        
        # Get the next scope
        scope = queue.get()
        if scope in visited: continue
        visited.add(scope)

        # Return variable declaration if it is declared in scope
        if variable_reference in scope.declared_variables_map:
            return scope.declared_variables_map[variable_reference]
        
        # Add the modules referenced by scope to queue
        for module in scope.referenced_modules:
            queue.put(module)
        
    # Search the next higher local scope
    return __search_local(curr.parent, variable_reference, visited)


def __search_global(program : Program, variable_reference : str) -> Variable:
    """
    Search the global scope for a variable declaration

    Args:
        program (Program): Object representation of a program
        variable_reference (str): Variable reference

    Returns:
        Variable: Variable declaration, or None if not found
    """
    
    # Get the variable declaration from the global scope
    return program.declared_procedures_map.get(variable_reference)