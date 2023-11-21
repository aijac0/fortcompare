from collections import deque
from typing import Union
from frtt.utilities.types.tree_node import TreeNode
from frtt.initial.initialize import initialize
from frtt.static_analysis.parsing.abstract_syntax_tree import get_abstract_syntax_tree
from tree_tools import *
from tree_consolidation import consolidate



def find_rooted_subpaths(trees, start_node):
    """
    Find all distinct subpaths in all subtrees rooted at a specific node in a set of trees
    All paths be linear (each node has 0 .. 1 children)
    Some paths will be cyclic (A -> B -> C -> ... -> A)
    """
    
    # Get subtrees rooted at start_node
    tree = consolidate(trees, start_node=start_node)
    
    # Get all distinct subpaths of subtrees
    return find_subpaths(tree)


def find_subpaths(trees : Union[TreeNode, list[TreeNode]]):
    """
    Find all distinct subpaths in a set of trees
    All paths be linear (each node has 0 .. 1 children)
    Some paths will be cyclic (A -> B -> C -> ... -> A)
    Returns dictionary mapping node names to the subpaths rooted at that node
    """
    
    # Consolidate trees
    tree = consolidate(trees) if type(trees) == list else trees
    
    # List of acyclic subpaths in trees
    subpaths = list()
    
    # Set of nodes that have been found to be cyclic
    cyclic_nodes = set()

    # Iterate over each path from root to leaf in tree
    for path in iter(enumerate_tree_paths(tree)):
        
        # Get each subpath of path
        new_subpaths = find_subpaths_helper(path, cyclic_nodes)
        subpaths.extend(new_subpaths)
                
    # Shorten subpaths that contain a cyclic node (not including the root)
    for subpath in subpaths:
        for curr in iter(enumerate_path_nodes(subpath)):
            if curr != subpath and curr.name in cyclic_nodes:
                curr.children = []
                break
                
    # Group subpaths rooted at the same node together
    node_subpath_map = dict()
    for subpath in subpaths:
        if subpath.name not in node_subpath_map: node_subpath_map[subpath.name] = []
        node_subpath_map[subpath.name].append(subpath)
    
    # Remove duplicate subpaths
    subpaths = []
    for node_subpaths in node_subpath_map.values():
        for node_subpath in iter(enumerate_tree_paths(consolidate(node_subpaths))):
            subpaths.append(node_subpath)
    
    return subpaths


def find_subpaths_helper(path : TreeNode, cyclic_nodes : set[str]):
    """
    Find all distinct subpaths of a path (used as a subroutine of find_subpaths)
    All paths be linear (each node has 0 .. 1 children)
    Some paths will be cyclic (A -> B -> C -> ... -> A)
    """
    
    # List of acyclic subpaths of path
    subpaths = []
    
    # Stack containing subpaths to check
    stack = deque()
    stack.append(path)

    # Iterate over each subpath
    while stack:
        subpath = stack.pop()
        
        # Keep track of nodes seen along subpath
        visited = set()
        
        # Traverse path searching for cycles
        is_acyclic = True
        prev_node = None
        for node in iter(enumerate_path_nodes(subpath)):
            
            # Path contains a cycle on node
            if node.name in visited:
                
                # Recreate of the cycle path, inner path, and external path
                #   Let (A -> ... -> B -> C -> ... -> B -> ... -> D) is the full subpath
                #   Let (B -> ... -> B) be the cycle path
                #   Let (A -> ... -> B -> ... -> C) be external path
                #   Let (C -> ... -> B) be the internal path
                # Cycle will be added to subpaths, all others will be added to stack

                # Get leaf and root nodes of the cycle path
                cycle_start_parent = None
                cycle_start = None
                cycle_end_parent = prev_node
                cycle_end = node
                for cycle_start in iter(enumerate_path_nodes(subpath)):
                    if cycle_start.name == cycle_end.name: break
                    cycle_start_parent = cycle_start
                
                # Inner path exists if the cycle path is not unary
                # Root of inner path is the child of the root of the cycle path
                # Leaf of inner path is the leaf of the cycle path
                if cycle_end_parent != cycle_start:
                
                    # Get the inner path
                    inner_path = cycle_start.children[0]
                    stack.append(inner_path)

                # Root of the cycle path is the root of the full subpath
                # Root of the excluded path is the leaf of the cycle path
                if cycle_start_parent is None:
                    
                    # Get the cycle path
                    cycle_path = subpath
                    new = TreeNode(cycle_end.name)
                    cycle_end_parent.children = [new]
                    subpaths.append(cycle_path)
                                        
                    # Get the excluded path
                    excluded_path = cycle_end
                    stack.append(excluded_path)
                
                # Root of the excluded path is the root of the full subpath
                # Child of the parent of root of the cycle path becomes leaf of cycle path
                else:
                    
                    # Get the cycle path
                    cycle_path = cycle_start
                    new = TreeNode(cycle_end.name)
                    cycle_end_parent.children = [new]
                    subpaths.append(cycle_path)
                    
                    # Get the excluded path
                    excluded_path = subpath
                    cycle_start_parent.children = [cycle_end]
                    stack.append(excluded_path)
                        
                # Discontinue search of current path to prevent detecting cycles caused by a cycle on a different node
                # Example:
                #   Path P : A -> B -> C -> A -> B
                #   Cycle S: A -> B -> C -> A
                #   Cycle R: B -> C -> A -> B
                #   S causes R
                is_acyclic = False
                cyclic_nodes.add(node.name)
                break
                
            # Continue along path
            prev_node = node
            visited.add(node.name)
            
        # Path does not contain a cycle
        if is_acyclic:
            
            # Add each subpath of path to list (excluding the final node, which would be a path of length 1)
            for node in iter(enumerate_path_nodes(subpath)):
                if node != prev_node:
                    subpaths.append(node)
    
    return subpaths

if __name__ == "__main__":
    
    # Get source files
    rootdir = input("Source root directory: ")
    filepaths = initialize(rootdir)

    # Get list of abstract syntax trees parsed from each source file
    trees = [get_abstract_syntax_tree(filepath) for filepath in filepaths]
    
    # Find subpaths
    subpaths = find_subpaths(trees)
    
    # Initialize the following sets of nodes
    nodes = set()
    acyclic_nodes = set()
    cyclic_nodes = set()
    internal_nodes = set()
    leaf_nodes = set()
    
    # Create sets
    for subpath in subpaths:
        for node in iter(enumerate_path_nodes(subpath)):
            nodes.add(node.name)
            if node.children:
                internal_nodes.add(node.name)
            elif node.name == subpath.name:
                cyclic_nodes.add(node.name)
    acyclic_nodes = nodes.difference(cyclic_nodes)
    leaf_nodes = nodes.difference(internal_nodes)
    
    # Write nodes to all_nodes.txt
    with open("frtt/data/nodes/all.txt", 'w') as f:
        for n in nodes:
            f.write(n + "\n")
            
    # Write cyclic nodes to cyclic_nodes.txt
    with open("frtt/data/nodes/cyclic.txt", 'w') as f:
        for n in cyclic_nodes:
            f.write(n + "\n")
            
    # Write acyclic nodes to cyclic_nodes.txt
    with open("frtt/data/nodes/acyclic.txt", 'w') as f:
        for n in acyclic_nodes:
            f.write(n + "\n")
            
    # Write internal nodes to internal_nodes.txt
    with open("frtt/data/nodes/internal.txt", 'w') as f:
        for n in internal_nodes:
            f.write(n + "\n")
            
    # Write leaf nodes to internal_nodes.txt
    with open("frtt/data/nodes/leaf.txt", 'w') as f:
        for n in leaf_nodes:
            f.write(n + "\n")
            
    # Initialize the following lists of paths
    cyclic_subpaths = list()
    acyclic_subpaths = list()
    
    # Create the lists
    node_subpath_map = dict()
    for subpath in subpaths:
        if subpath.name not in node_subpath_map: node_subpath_map[subpath.name] = list()
        node_subpath_map[subpath.name].append(subpath)
        for curr in iter(enumerate_path_nodes(subpath)): pass
        if curr.name == subpath.name: cyclic_subpaths.append(subpath)
        else: acyclic_subpaths.append(subpath)
    
    # Write subpaths to all_subpaths.txt
    with open("frtt/data/paths/subpaths/all.txt", 'w') as f:
        for subpath in subpaths:
            subpath_str = " -> ".join([node.name for node in iter(enumerate_path_nodes(subpath))])
            f.write(subpath_str + "\n")
            
    # Write cyclic subpaths to cyclic_subpaths.txt
    with open("frtt/data/paths/subpaths/cyclic.txt", 'w') as f:
        for subpath in cyclic_subpaths:
            subpath_str = " -> ".join([node.name for node in iter(enumerate_path_nodes(subpath))])
            f.write(subpath_str + "\n")
            
    # Write acyclic subpaths to acyclic_subpaths.txt
    with open("frtt/data/paths/subpaths/acyclic.txt", 'w') as f:
        for subpath in acyclic_subpaths:
            subpath_str = " -> ".join([node.name for node in iter(enumerate_path_nodes(subpath))])
            f.write(subpath_str + "\n")
            
    # Create consolidated subtrees
    for node in internal_nodes:
        node_subpaths = node_subpath_map[node]
        consolidated_subtree = consolidate(node_subpaths)
        
        # Write consolidated subtree to file
        with open("frtt/data/trees/subtrees/{}.txt".format(node), 'w') as f:
            f.write(str(consolidated_subtree))
            
