from utilities.types import ProgramUnit, Variable

def parse_programunit(tree):
    """
    Parse a tree that represents a program unit (module, function, subroutine).
    Store information gathered in a ProgramUnit object.
    :tree: Head of tree with value "ProgramUnit".
    :rvalue: ProgramUnit object.
    """
    
    # Make sure that tree has value "ProgramUnit"
    if tree.value != "ProgramUnit":
        raise Exception("Expected a \"ProgramUnit\" TreeNode but received a \"{}\" TreeNode.".format(tree.value))
    
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
    
    # Get nodes that represent entity declarations
    entitydecls = tree.walk("EntityDecl")
    
    # Add the name of each entity declaration as a variable declaration
    for entitydecl in entitydecls:
        namestmt = entitydecl.step("Name", exception_handling=True)
        name = namestmt.leaf().value[1:-1]
        if name not in obj.declared_names:
            var = Variable()
            var.name = name
            obj.declared_variables.append(var)
            obj.declared_names.add(name)    
            
    # Get nodes that represent data references
    datarefs = tree.walk("DataRef")
    
    # Add the name of each data reference as a variable reference
    for dataref in datarefs:
        namestmt = dataref.step("Name", exception_handling=True)
        name = namestmt.leaf().value[1:-1]
        obj.referenced_names.add(name)


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