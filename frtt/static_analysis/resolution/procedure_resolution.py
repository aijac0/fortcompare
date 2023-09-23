from queue import Queue
from frtt.utilities.types.generic import Program, ProgramUnit

def resolve_procedures(program : Program):
    """
    Resolve the procedure references
        
    Args:
        program (Program): Object representation of a program
    """

    # Iterate over each programunit
    for programunit in program.declared_programunits:
            
        # Iterate over each procedure reference
        for procedure_reference in programunit.referenced_procedure_names:
            
            # Search the local scope hierarchy for procedure declaration
            procedure_declaration = __search_local(programunit, procedure_reference)
            if procedure_declaration is not None:
                programunit.referenced_procedures.append(procedure_declaration)
                continue
            
            # Search the global scope for procedure declaration
            procedure_declaration = __search_global(program, procedure_reference)
            if procedure_declaration is not None:
                programunit.referenced_procedures.append(procedure_declaration)
                continue
            
            # Procedure declaration was not found
            #print("Procedure not found: {}".format(procedure_reference))
            #error_msg = "No declaration found for the procedure {} that is referenced in the {} {}"
            #raise Exception(error_msg.format(procedure_reference, programunit.type, programunit.name))
                
                
def __search_local(curr : ProgramUnit, procedure_reference : str, visited : set[ProgramUnit] = None) -> ProgramUnit:
    """
    Search the local scope hierarchy for a procedure declaration
    Backtracks the local scope hierarchy until end is reached or declaration is found
    BFS to search each local scope, and the scopes of any directly or indirectly referenced modules

    Args:
        curr (ProgramUnit): Current local scope
        procedure_reference (str): Procedure reference
        visited (set[ProgramUnit], optional): ProgramUnits that have already been searched. Defaults to None.

    Returns:
        ProgramUnit: Procedure declaration, or None if not found
        
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

        # Return procedure declaration if it is declared in scope
        if procedure_reference in scope.declared_procedures_map:
            return scope.declared_procedures_map[procedure_reference]
        
        # Add the modules referenced by scope to queue
        for module in scope.referenced_modules:
            queue.put(module)
        
    # Search the next higher local scope
    return __search_local(curr.parent, procedure_reference, visited)


def __search_global(program : Program, procedure_reference : str) -> ProgramUnit:
    """
    Search the global scope for a procedure declaration

    Args:
        program (Program): Object representation of a program
        procedure_reference (str): Procedure reference

    Returns:
        ProgramUnit: Procedure declaration, or None if not found
    """
    
    # Get the procedure declaration from the global scope
    return program.declared_procedures_map.get(procedure_reference)