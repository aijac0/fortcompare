from frtt.utilities.types.generic import Program
from frtt.static_analysis.resolution.module_resolution import resolve_modules
from frtt.static_analysis.resolution.procedure_resolution import resolve_procedures
from frtt.static_analysis.resolution.variable_resolution import resolve_variables
from frtt.static_analysis.resolution.dependency_resolution import resolve_dependencies

def resolution(program : Program):
    """
    Resolve the name references to objects in a program

    Args:
        program (Program) : Object representation of a program
    """

    # Resolve the module references
    resolve_modules(program)
    
    # Resolve the procedure references
    resolve_procedures(program)
    
    # Resolve the variable references
    resolve_variables(program)
    
    # Resolve the dependencies between program units
    resolve_dependencies(program)