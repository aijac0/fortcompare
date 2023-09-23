from frtt.utilities.types.generic import Program, ProgramUnit

def resolve_modules(program : Program):
    """
    Resolve the module references
        
    Args:
        program (Program): Object representation of a program
        
    Assumptions:
        1. Modules can only be declared at the global scope
    """

    # Iterate over each programunit
    for programunit in program.declared_programunits:
            
        # Iterate over each module reference
        for module_reference in programunit.referenced_module_names:
            
            # Search the global scope for module declaration
            module_declaration = __search_global(program, module_reference)
            if module_declaration is not None:
                programunit.referenced_modules.append(module_declaration)
                continue

            # Module declaration was not found
            #print("Module not found: {}".format(module_reference))
            #error_msg = "No declaration found for the module {} that is referenced in the {} {}"
            #raise Exception(error_msg.format(module_reference, programunit.type, programunit.name))

                
def __search_global(program : Program, module_reference : str) -> ProgramUnit:
    """
    Search the global scope for a module declaration

    Args:
        program (Program): Object representation of a program
        module_reference (str): Module reference

    Returns:
        ProgramUnit: Module declaration, or None if not found
    """
    
    # Get the module declaration from the global scope
    return program.declared_modules_map.get(module_reference)
            