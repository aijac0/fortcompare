from frtt.utilities.types.tree_node import TreeNode
from frtt.initial.initialize import initialize
from frtt.static_analysis.parsing.abstract_syntax_tree import get_abstract_syntax_tree

def consolidate(trees : list[TreeNode], start_node = None, ignore_nodes = None):
    if start_node is None: start_node = "Program"
    if ignore_nodes is None: ignore_nodes = []
    
    # Get list of trees to consolidate
    source_trees = []
    for tree in trees:
        source_trees.extend(tree.walk(start_node))
        if tree.name() == start_node: source_trees.append(tree)
    
    # Consolidate trees
    return consolidate_helper(source_trees, start_node, ignore_nodes)
            
            
def consolidate_helper(nodes : list[TreeNode], node_name : str, ignore_nodes : list[str]):
    
    # Initialize consolidated node
    new = TreeNode(node_name)
    
    # Ignore children of current node if it is one of the ignore_nodes
    if node_name in ignore_nodes:
        return new
    
    # Group children of nodes together that have the same name
    name_map = dict()
    for node in nodes:
        for child in node.children:
            if child.name() not in name_map:
                name_map[child.name()] = [child]
            else:
                name_map[child.name()].append(child)
    
    # Call consolidate helper on each group and add result to children of consolidated node
    for child_name, children in name_map.items():
        new.children.append(consolidate_helper(children, child_name, ignore_nodes))
        
    return new

if __name__ == "__main__":

    # Get source files
    rootdir = input("Source root directory: ")
    filepaths = initialize(rootdir)

    # Get list of abstract syntax trees parsed from each source file
    trees = [get_abstract_syntax_tree(filepath) for filepath in filepaths]
                
    # Consolidate trees
    start_node = "ProgramUnit"
    ignore_nodes = ["Expr", "ExecutionPart"]
    tree = consolidate(trees, start_node=start_node, ignore_nodes=ignore_nodes)

    # Write consolidated tree to file
    with open("frtt/exploratory/consolidated.txt", 'w') as f:
        f.write(str(tree))