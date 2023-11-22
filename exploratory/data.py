from collections import deque
from initial.initialize import initialize
from static_analysis.parsing.abstract_syntax_tree import get_abstract_syntax_tree
from utilities.types.tree_node import TreeNode
from subtrees import find_subtrees


def init_trees(src_rootdir : str):
    """
    Get list of abstract syntax trees from Fortran source files under a root directory
    Get list of subtrees from trees (see subtrees.py)
    Return trees, tree, subtrees
    """

    # Get source files
    filepaths = initialize(src_rootdir)
    
    # Get list of abstract syntax trees parsed from each source file
    trees = [get_abstract_syntax_tree(filepath) for filepath in filepaths]
    
    # Get list of consolidated subtrees
    subtrees = find_subtrees(trees)
    
    return trees, subtrees


def write_counts(trees : list[TreeNode], data_rootdir : str):
    """
    For each distinct ordered pair of nodes (n1, n2), write the following:
    1. Minimum number of times n2 appears as a child of n1 for any instance of n1
    2. Maximum number of times n2 appears as a child for n1 for an instance of n1
    """
    
    # Get list of nodes and dictionary containing min/max counts
    nodes, counts = __get_counts(trees)
    
    # Open file
    f = open(data_rootdir + '/' + "counts.txt", 'w')
    
    # Iterate over each distinct pair of nodes (distinct means (n1, n2) != (n3, n4) implies n1 != n3 or n2 != n4)
    for n1 in nodes:
        for n2 in nodes:
            
            # Get min, max counts
            if n2 in counts[n1]:
                mn, mx = counts[n1][n2]
            else:
                mn, mx = 0, 0
                
            # Write min, max counts
            entry = "{} {} {} {}\n".format(n1, n2, mn, mx)
            f.write(entry)
    
    # Close file
    f.close()


def __get_counts(trees : list[TreeNode]):
    """
    For each distinct ordered pair of nodes (n1, n2), get the following:
    1. Minimum number of times n2 appears as a child of n1 for any instance of n1
    2. Maximum number of times n2 appears as a child for n1 for an instance of n1
    Return list of distinct nodes and dictionary mapping n1 -> n2 -> (min, max)
    Mapping will have an entry (n1 -> ...) for all n1
    Mapping may not have an entry (n1 -> n2 -> ...) for all n1 for all n2
    """
    
    # Initialize list of nodes and dictionary containing min/max counts
    nodes = list()
    counts = dict()
    
    # Iterate over each tree
    for tree in trees:
        
        # Initialize stack
        stack = deque()
        stack.append(tree)
        
        # DFS
        while stack:
            
            # Get next node from stack
            curr = stack.pop()
            if curr.name not in counts: 
                counts[curr.name] = dict()
                nodes.append(curr.name)
            
            # Number of times each node is as a child of curr
            temp_nodes = list()
            temp_counts = dict()
            
            # Iterate over each child node
            for next in curr.children:
                
                # Add 1 to count
                if next.name not in temp_counts: 
                    temp_nodes.append(next.name)
                    temp_counts[next.name] = 0
                temp_counts[next.name] += 1
                
                # Add child to stack
                stack.append(next)
                
            # Update counts
            for node in temp_nodes:
                count = temp_counts[node]
                if node not in counts[curr.name]: counts[curr.name][node] = (count, count)
                else: 
                    mn, mx = counts[curr.name][node]
                    counts[curr.name][node] = (min(count, mn), max(count, mx))
                    
    return nodes, counts


def write_nodes(subtrees : list[TreeNode], data_rootdir : str):
    """
    Write all nodes to file
    Write each node to the file associated with each category that it belongs to
    1. Internal
    2. Leaf
    3. Acyclic
    4. Cyclic
    * An 'internal node' is a node that appears at least once as a non-leaf node in some tree
    * A 'leaf node' is a node that only appears as a leaf node in all trees
    * An 'acyclic node' is a node that never appears more than once in all subpaths
    * A 'cyclic node' is a node that appears more than one in some subpath
    """
    
    # Get dictionary mapping each node to disjoint categories
    node_map = __get_nodes(subtrees)
    
    # Open files
    all_file = open(data_rootdir + "/nodes/all.txt", 'w')
    internal_file = open(data_rootdir + "/nodes/internal.txt", 'w')
    leaf_file = open(data_rootdir + "/nodes/leaf.txt", 'w')
    acyclic_file = open(data_rootdir + "/nodes/acyclic.txt", 'w')
    cyclic_file = open(data_rootdir + "/nodes/cyclic.txt", 'w')
    
    # Write each node to file
    for node, category in node_map.items():
        
        # Write node to file containg all nodes
        nodeline = node + '\n'
        all_file.write(nodeline)
        
        # Write node to files corresponding to category
        match category:
            
            # Internal, acyclic
            case 1:             
                internal_file.write(nodeline)
                acyclic_file.write(nodeline)
                
            # Internal, cyclic
            case 2:
                internal_file.write(nodeline)
                cyclic_file.write(nodeline)
                
            # Leaf, acyclic
            case 3:
                leaf_file.write(nodeline)
                acyclic_file.write(nodeline)
                
    # Close files
    all_file.close()
    internal_file.close()
    leaf_file.close()
    acyclic_file.close()
    cyclic_file.close()
    

def __get_nodes(subtrees : list[TreeNode]):
    """
    Parse tree for distinct nodes
    Assign each node to one of the following groups:
    1. Internal, acyclic
    2. Internal, cyclic
    3. Leaf, acyclic
    * An 'internal node' is a node that appears at least once as a non-leaf node in some tree
    * A 'leaf node' is a node that only appears as a leaf node in all trees
    * An 'acyclic node' is a node that never appears more than once in all subpaths
    * A 'cyclic node' is a node that appears more than one in some subpath
    Return dictionary mapping each node to an integer 1-3 corresponding to its group
    """
    
    # Initialize list of all nodes and sets identifying nodes belonging to a category (not mutally exclusive)
    nodes = list()
    seen = set()
    internal = set()
    cyclic = set()
    
    # Iterate over each subtree
    for head in subtrees:
        
        # Initialize stack
        stack = deque()
        stack.append(head)
        
        # DFS
        while stack:
            
            # Get next node from stack
            curr = stack.pop()
            if curr.name not in seen:
                nodes.append(curr.name)
                seen.add(curr.name)
            
            # Node is internal (node has children)
            if curr.children:
                internal.add(curr.name)
            
            # Node is cyclic (node has no children and is equal to head)
            elif curr.name == head.name:
                cyclic.add(curr.name)
                
            # Add children to stack
            for child in curr.children:
                stack.append(child)
                
    # Assign each node to a category
    categories = dict()
    for node in nodes:
        
        # Node is internal
        if node in internal:
            
            # Node is internal, cyclic
            if node in cyclic:
                category = 1
                
            # Node is internal, acyclic
            else:
                category = 2
            
        # Node is leaf, acyclic    
        else:
            category = 3

        # Assign node to category
        categories[node] = category
    
    return categories            
                

def write_subtrees(subtrees : TreeNode, data_rootdir : str):
    """
    Write all subtrees to file
    """
    
    # Write each subtree to file
    for subtree in subtrees:
        filepath = data_rootdir + '/' + str(subtree.name) + ".txt"
        with open(filepath, 'w') as f:
            f.write(str(subtree))


def write_all(trees : list[TreeNode], subtrees : list[TreeNode], data_rootdir : str):
    """
    Run all data writing routines
    """
    write_counts(trees, data_rootdir)
    write_nodes(subtrees, data_rootdir)
    write_subtrees(subtrees, data_rootdir)
    
    
def init_data(src_rootdir : str, data_rootdir : str):
    """
    Initialize data parsed from source files
    """
    
    # Read source files and generate trees
    trees, subtrees = init_trees(src_rootdir)
    
    # Generate and write all data to file
    write_all(trees, subtrees, data_rootdir)
    
    
if __name__ == "__main__":

    # Initialize data
    src_rootdir = "codes"
    data_rootdir = "data"
    init_data(src_rootdir, data_rootdir)
