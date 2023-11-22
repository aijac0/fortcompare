from utilities.types.generic import ProgramUnit, Variable
from utilities.types.tree_node import TreeNode



def parse_variables(tree : TreeNode, obj : ProgramUnit):
    """
    Parse variable declarations from a tree.
    Store information gathered in Variable objects within ProgramUnit object.
    :tree: Head of tree with value "ImplicitPart".
    :obj: Object representation of the programunit being parsed.
    """

    # Make sure that tree has value "ImplicitPart"
    if tree.value != "ImplicitPart":
        raise Exception("Expected a \"ImplicitPart\" TreeNode but received a \"{}\" TreeNode.".format(tree.value))
    
    # Get nodes that represent entity declarations
    entitydecls = tree.walk("EntityDecl")

    # Create a Variable object for each distinct entity declaration
    for entitydecl in entitydecls:
        namestmt = entitydecl.step("Name", exception_handling=True)
        name = namestmt.leaf().value[1:-1]
        if name not in obj.declared_variables_map:
            var = Variable()
            var.name = name
            obj.declared_variables.append(var)
            obj.declared_variables_map[name] = var
    
    # Iterate over each distinct variable
    for var in obj.declared_variables:
        vname = var.name
        
        # Get subtree representing variable declaration statements
        # Subtree consists of all branches under "ImplicitPart" that have either no entitydecl or the entitydecl associated with target variable (and possible others)
        subtree = tree.deep_copy()
        queue = [(subtree, next) for next in subtree.children]
        while queue:
            prev, curr = queue.pop()
            leaves = set([leaf.value[1:-1] for leaf in curr.leaves()])
            skip = False
            if vname not in leaves:
                for other_var in obj.declared_variables:
                    other_vname = other_var.name
                    if other_vname in leaves:
                        skip = True
                        prev.children.remove(curr)
                        del curr
                        break
            if not skip:
                queue.extend([(curr, next) for next in curr.children])
                
        # Parse object representation of Variable from subtree representing a variable declaration
        parse_variable(subtree, var)
        
        
def parse_variable(tree : TreeNode, obj : Variable):
    """
    Parse variable declarations from a tree representing a declaration for a single variable.
    Store information gathered in Variable object.
    :tree: Head of tree with value "ImplicitPart" representing declaration for a single variable.
    :obj: Object representation of the variable being declared.
    """
    
    # Make sure that tree has value "ImplicitPart"
    if tree.value != "ImplicitPart":
        raise Exception("Expected a \"ImplicitPart\" TreeNode but received a \"{}\" TreeNode.".format(tree.value))
    
    # Parse type
    #parse_type(tree, obj)
    
    # Parse kind
    #parse_kind(tree, obj)
    
    
def parse_type(tree : TreeNode, obj : Variable):
    subtree = tree.step(["IntegerTypeSpec", "Real", "Character", "Logical", "Complex", "DoublePrecision", "DerivedTypeSpec"])
    if subtree:
        match subtree.value:
            case "IntegerTypeSpec":
                obj.type = "integer"
            case "Real":
                obj.type = "real"
            case "Character":
                obj.type = "character"
            case "Logical":
                obj.type = "logical"
            case "Complex":
                obj.type = "complex"
            case "DoublePrecision":
                obj.type = "double precision"
            case "DerivedTypeSpec":
                namestmt = subtree.step("Name", exception_handling=False)
                name = namestmt.leaf().value[1:-1]
                obj.type = name
            
            
def parse_kind(tree : TreeNode, obj : Variable):
    subtree = tree.step("KindSelector")
    if subtree:
        kindstr = subtree.leaf().value
        if kindstr.isnumeric():
            obj.kind = int(kindstr)
            
            
def parse_dimensions(tree : TreeNode, obj : Variable):
    pass
    
    