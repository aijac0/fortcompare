from typing import Iterable
from collections import deque
from utilities.types.tree_node import TreeNode


def write_adjacency_counts(trees : Iterable[TreeNode], data_rootdir : str):
    """
    For each distinct ordered pair of nodes (n1, n2), write the following:
    1. Minimum number of times n2 appears as a child of n1 for any instance of n1
    2. Maximum number of times n2 appears as a child for n1 for an instance of n1
    """
    
    # Dictionary containing min/max counts
    adj_counts = __get_adjacency_counts(trees)
    
    # Open file
    f = open(data_rootdir + '/' + "adjacency_counts.txt", 'w')
    
    # Iterate over each distinct pair of nodes with an entry in adj_counts
    for node1, node_counts in adj_counts.items():
        for node2, counts in node_counts.items():
            
            # Get min, max counts
            mn, mx = counts
                
            # Write min, max counts
            entry = "{} {} {} {}\n".format(node1, node2, mn, mx)
            f.write(entry)
    
    # Close file
    f.close()


def __get_adjacency_counts(trees : Iterable[TreeNode]):
    """
    For each distinct ordered pair of nodes (n1, n2), get the following:
    1. Minimum number of times n2 appears as a child of n1 for any instance of n1
    2. Maximum number of times n2 appears as a child for n1 for an instance of n1
    Mapping will have an entry (n1 -> ...) for all n1
    Mapping may not have an entry (n1 -> n2 -> ...) for all n1 for all n2
    """
    
    # Initialize dictionary containing min/max counts
    counts = dict()
    
    # Iterate over each tree
    for tree in trees:
        
        # Initialize stack
        stack = deque()
        stack.append(tree)
        
        # DFS
        while stack:
            
            # Get current node from stack
            curr = stack.pop()
            if curr.name not in counts: 
                counts[curr.name] = dict()
            
            # Number of times each node is a child
            temp_counts = dict()
            
            # Iterate over each child
            for next in curr.children:
                
                # Add 1 to count
                if next.name not in temp_counts: 
                    temp_counts[next.name] = 1
                else:
                    temp_counts[next.name] += 1
                
                # Add child to stack
                stack.append(next)
                
            # Update counts
            for node, count in temp_counts.items():
                if node not in counts[curr.name]: 
                    counts[curr.name][node] = (count, count)
                else: 
                    mn, mx = counts[curr.name][node]
                    counts[curr.name][node] = (min(count, mn), max(count, mx))
                    
    return counts