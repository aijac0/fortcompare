from typing import Iterable
from collections import deque
from utilities.types.tree_node import TreeNode


def write_edge_counts(trees : Iterable[TreeNode], data_rootdir : str):
    """
    For each distinct edge (n1, n2), write the following:
    1. Minimum number of times edge appears for any instance of n1
    2. Maximum number of times edge appears for any instance of n1
    """
    
    # Dictionary containing min/max counts
    edge_counts = __get_edge_counts(trees)
    
    # Open file
    f = open(data_rootdir + '/' + "edge_counts.txt", 'w')
    
    # Iterate over each distinct edge with an entry in adj_counts
    for node1, node_counts in edge_counts.items():
        for node2, counts in node_counts.items():
            
            # Get min, max counts
            mn, mx = counts
                
            # Write min, max counts
            entry = "{} {} {} {}\n".format(node1, node2, mn, mx)
            f.write(entry)
    
    # Close file
    f.close()


def __get_edge_counts(trees : Iterable[TreeNode]):
    """
    For each distinct edge (n1, n2), write the following:
    1. Minimum number of times edge appears for any instance of n1
    2. Maximum number of times edge appears for any instance of n1
    Mapping will have an entry (n1 -> ... -> (min, max)) for all n1
    Mapping may not have an entry (n1 -> n2 -> (min, max)) for all n1 for all n2
    """
    
    # Initialize dictionary containing min/max counts
    counts = dict()
        
    # Initialize stack
    stack = deque(trees)
    
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
            
            # Increment count
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


def read_edge_counts(data_rootdir : str):
    """
    Read edge counts from file
    """
    
    # Dictionary containing min/max counts
    edge_counts = dict()
    
    # Open file
    f = open(data_rootdir + '/' + "edge_counts.txt", 'r')
    
    # Iterate over each line in file
    for line in f.readlines():
    
        # Parse line for edge count
        node1, node2, mn_str, mx_str = line.split(' ')
        mn = int(mn_str)
        mx = int(mx_str)
        
        # Add edge count to dict
        if node1 not in edge_counts:
            edge_counts[node1] = dict()
        edge_counts[node1][node2] = (mn, mx)
    
    # Close file
    f.close()
    
    return edge_counts


def read_edges(data_rootdir : str):
    """
    Read edge lists from file
    """
    
    # Dictionary containing edge lists
    edge_lists = dict()
    
    # Open file
    f = open(data_rootdir + '/' + "edge_counts.txt", 'r')
    
    # Iterate over each line in file
    for line in f.readlines():
    
        # Parse line for edge
        node1, node2, _, _ = line.split(' ')
        
        # Add edge to dict
        if node1 not in edge_lists:
            edge_lists[node1] = [node2]
        else:
            edge_lists[node1].append(node2)
    
    # Close file
    f.close()
    
    return edge_lists