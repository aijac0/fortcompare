from frtt.static_analysis.parsing import abstract_syntax_tree as ast, tree_parsing as tp
from frtt.utilities.types.tree_node import TreeNode
from frtt.initial.initialize import initialize

def reconstruct_path(predecessors, new):
    path = [new]
    curr = new
    while True:
        if predecessors[curr] is None:
            break
        curr = predecessors[curr]
        path.append(curr)
        
    head = None
    prev = None
    for curr in reversed(path):
        new = TreeNode(curr.value)
        if head is None:
            head = new
            prev = new
        else:
            prev.children.append(new)
            prev = new
    return head
                

def parse_ast_variables(tree : TreeNode):
    variables = dict()
    variable_names = []
    tree = tree.step("ImplicitPart", exception_handling=False)
    if not tree: return variables
    
    for variable_name in [decl.leaf().value[1:-1] for decl in tree.walk("EntityDecl")]:
        variable_names.append(variable_name)
        
    for variable_name in variable_names:
        tree_copy = tree.deep_copy()
        variables[variable_name] = tree_copy
        queue = [(tree_copy, next) for next in tree_copy.children]
        while queue:
            prev, curr = queue.pop()
            leaves = set([leaf.value[1:-1] for leaf in curr.leaves()])
            skip = False
            if variable_name not in leaves:
                for other_vname in variable_names:
                    if other_vname in leaves:
                        skip = True
                        prev.children.remove(curr)
                        del curr
                        break
            if not skip:
                queue.extend([(curr, next) for next in curr.children])
        
            
    return variables        


def parse_file_variables(filepath):
    tree = ast.get_abstract_syntax_tree(filepath)
    routine_variables = dict()
    for subtree in tree.kins("ProgramUnit"):
        programunit = tp.parse_programunit(subtree)
        routine_variables[programunit.name] = parse_ast_variables(subtree)
    return routine_variables


def find_trees(path, trees):
    if not len(path): return []
    matching_trees = []
    for tree in trees:
        subtrees = tree.walk(path[0])
        if pts.get_node_name(tree) == path[0]:
            subtrees.append(tree)
        for subtree in subtrees:
            contains_path = True
            curr = subtree
            for i in range(1, len(path)):
                curr = curr.step(path[i])
                if not curr:
                    contains_path = False
                    break
            if contains_path: 
                matching_trees.append(tree)
                break
    return matching_trees


def enumerate_paths(tree : TreeNode):
    """
    DFS to get each path from root to leaf in tree
    """
    
    # DFS storing path to current node
    stack = [(tree, ())]
    while stack:
        curr, prev_path = stack.pop()
        curr_name = curr.name()
        curr_path = prev_path + (curr_name,)
        
        # Create and output path if node is a leaf
        if not curr.children:
            head = TreeNode(curr_path[0])
            prev = head
            for curr_name in curr_path[1:]:
                curr = TreeNode(curr_name)
                prev.children.append(curr)
                prev = curr
            yield head
            
        # Traverse children
        else:
            stack.extend([(next, curr_path) for next in curr.children])
            
def get_node_names(path : TreeNode):
    """
    Print '->' separated names of nodes in path.
    Assumes path is linear (each node has either 0 or 1 children)
    """
    node_names = []
    curr = path
    while True:
        node_names.append(curr.name())
        if not curr.children:
            break
        curr = curr.children[0]
    return node_names

def get_path(tree : TreeNode, path : list[str]):
    stack = [(tree, 0)]
    while stack:
        curr, depth = stack.pop()
        if depth + 1 == len(path):
            head = TreeNode(path[0])
            prev = head
            for node_name in path[1:-1]:
                next = TreeNode(node_name)
                prev.children.append(next)
                prev = next
            prev.children.append(curr)
            return head
        stack.extend([(c, depth + 1) for c in curr.children if c.name() == path[depth + 1]])
    return None

def has_path(tree : TreeNode, path : list[str]):
    stack = [(tree, 0)]
    while stack:
        curr, depth = stack.pop()
        if depth + 1 == len(path): return True
        stack.extend([(c, depth + 1) for c in curr.children if c.name() == path[depth + 1]])
    return False