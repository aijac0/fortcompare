from frtt.utilities.types.generic import ProgramUnit
from frtt.utilities.types.tree_node import TreeNode
from frtt.static_analysis.parsing.variable_parsing import parse_variables

def parse_program(tree : TreeNode) -> list[ProgramUnit]:
    """
    Parse a tree that represents a source file.
    Store information gathered in a list of ProgramUnit objects.
    :tree: Head of tree with value "Program"
    :rvalue: List of parsed programunit objects
    """
    
    # Make sure that tree has value "Program"
    if tree.value != "Program":
        raise Exception("Expected a \"Program\" TreeNode but received a \"{}\" TreeNode.".format(tree.value))

    # Get a list of the subtrees representing a program unit
    subtrees = tree.walk("ProgramUnit")
    
    # Get the ProgramUnit representation of each subtree
    return [parse_programunit(subtree) for subtree in subtrees]


def parse_programunit(tree):
    """
    Parse a tree that represents a program unit (module, function, subroutine).
    Store information gathered in a ProgramUnit object.
    :tree: Head of tree with value "ProgramUnit", "InternalSubprogram", or "ModuleSubprogram".
    :rvalue: ProgramUnit object.
    """
    
    # Make sure that tree has value "ProgramUnit", "InternalSubprogram", or "ModuleSubprogram"
    if tree.value != "ProgramUnit" and tree.value != "InternalSubprogram" and tree.value != "ModuleSubprogram":
        raise Exception("Expected a \"ProgramUnit\", \"InternalSubprogram\", or \"ModuleSubprogram\" TreeNode but received a \"{}\" TreeNode.".format(tree.value))

    # Initialize ProgramUnit object to return
    rvalue = ProgramUnit()
    
    # Get the type of the program unit
    programunitstmt = tree.step(["Module", "FunctionStmt", "SubroutineStmt"], exception_handling=True)
    if programunitstmt.value == "Module":
        rvalue.type = "module"
    elif programunitstmt.value == "FunctionStmt":
        rvalue.type = "function"
    elif programunitstmt.value == "SubroutineStmt":
        rvalue.type = "subroutine"
        
    # Get the name of the program unit
    namestmt = programunitstmt.step("Name", exception_handling=True)
    rvalue.name = namestmt.leaf().value[1:-1]
    
    # Parse the specification part of tree
    parse_specificationpart(tree.step("SpecificationPart", exception_handling=True), rvalue)
    
    # Parse the internal subprogram part of tree
    internalsubprogram_part = tree.step(["InternalSubprogramPart", "ModuleSubprogramPart"])
    if internalsubprogram_part:
        parse_internalsubprogrampart(internalsubprogram_part, rvalue)
    
    # Parse the execution part of tree
    execution_part = tree.step("ExecutionPart")
    if execution_part:
        parse_executionpart(execution_part, rvalue)
    
    return rvalue


def parse_specificationpart(tree, obj):
    """
    Parse a tree that represents the specification part of a program unit.
    Store information gathered in a ProgramUnit object.
    :tree: Head of tree with value "SpecificationPart".
    :obj: Object representation of the programunit being parsed.
    """

    # Make sure that tree has value "SpecificationPart"
    if tree.value != "SpecificationPart":
        raise Exception("Expected a \"SpecificationPart\" TreeNode but received a \"{}\" TreeNode.".format(tree.value))
    
    # Get nodes that represent use statements
    usestmts = tree.walk("UseStmt")
    
    # Add the name of each data reference as a variable reference
    for usestmt in usestmts:
        namestmt = usestmt.step("Name", exception_handling=True)
        name = namestmt.leaf().value[1:-1]
        obj.referenced_module_names.add(name)
            
    # Get nodes that represent data references
    datarefs = tree.walk("DataRef")
    
    # Add the name of each data reference as a name reference
    for dataref in datarefs:
        namestmt = dataref.step("Name", exception_handling=True)
        name = namestmt.leaf().value[1:-1]
        obj.referenced_names.add(name)
        
    # Get nodes that represent external programunit references
    externalstmts = tree.walk("ExternalStmt")
    
    # Add the name of each data reference as a programunit name reference
    for externalstmt in externalstmts:
        namestmt = externalstmt.step("Name", exception_handling=True)
        name = namestmt.leaf().value[1:-1]
        obj.referenced_procedure_names.add(name)
        
    # Parse variables declarations
    implicit_part = tree.step(["ImplicitPart"])
    if implicit_part:
        parse_variables(implicit_part, obj)


def parse_internalsubprogrampart(tree, obj):
    """
    Parse a tree that represents the internal subprogram part of a program unit.
    Store information gathered in a ProgramUnit object.
    :tree: Head of tree with value "InternalSubprogramPart".
    :obj: Object representation of the programunit being parsed.
    """
    
    # Make sure that tree has value "InternalSubprogramPart" or "ModuleSubprogramPart"
    if tree.value != "InternalSubprogramPart" and tree.value != "ModuleSubprogramPart":
        raise Exception("Expected a \"InternalSubprogramPart\" or \"ModuleSubprogramPart\" TreeNode but received a \"{}\" TreeNode.".format(tree.value))
    
    # Get nodes that represent internal subprogram declarations
    internal_subprograms = tree.walk(["InternalSubprogram", "ModuleSubprogram"])
    for internal_subprogram in internal_subprograms:
        rvalue = parse_programunit(internal_subprogram)
        rvalue.parent = obj
        obj.declared_procedures.append(rvalue)
        obj.declared_procedures_map[rvalue.name] = rvalue
        
        
def parse_executionpart(tree, obj):
    """
    Parse a tree that represents the execution part of a program unit.
    Store information gathered in a ProgramUnit object.
    :tree: Head of tree with value "ExecutionPart".
    :obj: Object representation of the programunit being parsed.
    """
    
    # Make sure that tree has value "ExecutionPart"
    if tree.value != "ExecutionPart":
        raise Exception("Expected a \"ExecutionPart\" TreeNode but received a \"{}\" TreeNode.".format(tree.value))
    
    # Get nodes that represent data references
    datarefs = tree.walk("DataRef")
    
    # Add the name of each data reference as a variable reference
    for dataref in datarefs:
        namestmt = dataref.step("Name", exception_handling=True)
        name = namestmt.leaf().value[1:-1]
        obj.referenced_names.add(name)
        
    # Get nodes that represent function calls (may be array accesses)
    functionreferences = tree.walk("FunctionReferences")
    for functionreference in functionreferences:
        proceduredesignator = functionreference.step("ProcedureDesignator", exception_handling=True)
        namestmt = proceduredesignator.step("Name", exception_handling=True)
        name = namestmt.leaf().value[1:-1]
        if name not in obj.declared_procedures_map:
            obj.referenced_names.add(name)
        
    # Get nodes that represent subroutine calls
    callstmts = tree.walk("CallStmt")
    for callstmt in callstmts:
        proceduredesignator = callstmt.step("ProcedureDesignator", exception_handling=True)
        namestmt = proceduredesignator.step("Name", exception_handling=True)
        name = namestmt.leaf().value[1:-1]
        obj.referenced_procedure_names.add(name)