from typing import Iterable
from collections import deque
from utilities.types.tree_node import TreeNode


def write_path_counts(trees : Iterable[TreeNode], data_rootdir : str):
    """
    For each distinct node n, write the following:
    1. Minimum number of times n appears on a path for which it appears at least once 
    2. Maximum number of times n appears on a path for which it appears at least once
    """
    
    # List of nodes and dictionary containing min/max counts
    path_counts = __get_path_counts(trees)
    
    # Open file
    f = open(data_rootdir + '/' + "path_counts.txt", 'w')
    
    # Iterate over each (node, counts) pair
    for node, counts in path_counts.items():
            
            # Get min, max counts
            mn, mx = counts
                
            # Write min, max counts
            entry = "{} {} {}\n".format(node, mn, mx)
            f.write(entry)
    
    # Close file
    f.close()


def __get_path_counts(trees : Iterable[TreeNode]):
    """
    For each distinct node n, write the following:
    1. Minimum number of times n appears on a path for which it appears at least once 
    2. Maximum number of times n appears on a path for which it appears at least once
    Return dictionary mapping n -> (min, max)
    Mapping will have an entry (n -> ...) for all n
    """
    
    # Initialize dictionary containing min/max counts
    counts = dict()
    
    # Iterate over each tree
    for tree in trees:
        
        # Initialize stack
        stack = deque()
        stack.append(tree)

        # Initialize path
        path = deque()
        
        # DFS
        while stack:
            
            # Get current node from stack
            curr = stack.pop()
            
            # Add current node to path
            path.append(curr.name)
            
            # Curr is a leaf node
            if not curr.children:
                
                # Number of times each node appears on path
                temp_counts = dict()
                
                # Iterate over path
                for node in path:
                    
                    # Add 1 to count
                    if node not in temp_counts:
                        temp_counts[node] = 1
                    else:   
                        temp_counts[node] += 1
                
                # Update counts
                for node, count in temp_counts.items():
                    if node not in counts:
                        counts[node] = (count, count)
                    else:
                        mn, mx = counts[node]
                        counts[node] = (min(count, mn), max(count, mx))
                        
                # Remove last node from path (DFS will backtrack because curr is a leaf node)
                path.pop()
                
            # Curr is an internal node
            else:
                
                # Add each child to stack
                stack.extend(curr.children)
                    
    return counts