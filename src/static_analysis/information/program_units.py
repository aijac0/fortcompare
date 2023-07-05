class ProgramUnit:
    
    def __init__(self):
        self.name = None                                              
        self.type = None                                              # "module", "function", or "subroutine"
        self.referenced_modules = set()
        self.declared_variables = set()
        self.referenced_variables = set()
        
    def __str__(self):
        out_str = ""
        out_str += "ProgramUnit:\n"
        out_str += "\tName: " + self.name + "\n"
        out_str += "\tType: " + self.type + "\n"
        out_str += "\tReferenced Modules: " + ("\n" if self.referenced_modules else "None\n")
        for referenced_module in self.referenced_modules:
            out_str += "\t\t" + referenced_module + "\n"
        out_str += "\tDeclared Variables: " + ("\n" if self.declared_variables else "None\n")
        for declared_variable in self.declared_variables:
            out_str += "\t\t" + declared_variable + "\n"
        out_str += "\tReferenced Variables: " + ("\n" if self.referenced_variables else "None\n")
        for referenced_variable in self.referenced_variables:
            out_str += "\t\t" + referenced_variable + "\n"
        return out_str
        

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
        obj.referenced_modules.add(name)
    
    # Get nodes that represent entity declarations
    entitydecls = tree.walk("EntityDecl")
    
    # Add the name of each data reference as a variable reference
    for entitydecl in entitydecls:
        namestmt = entitydecl.step("Name", exception_handling=True)
        name = namestmt.leaf().value[1:-1]
        obj.declared_variables.add(name)
    
    # Get nodes that represent data references
    datarefs = tree.walk("DataRef")
    
    # Add the name of each data reference as a variable reference
    for dataref in datarefs:
        namestmt = dataref.step("Name", exception_handling=True)
        name = namestmt.leaf().value[1:-1]
        obj.referenced_variables.add(name)


def parse_executionpart(tree, obj):
    """
    Parse a tree that represents the execution part of a program unit.
    Store information gathered in a ProgramUnit object.
    :tree: Head of tree with value "ExecutionPart".
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
        obj.referenced_variables.add(name)