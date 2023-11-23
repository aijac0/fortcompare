from typing import Iterable
from initial.initialize import initialize
from static_analysis.parsing.abstract_syntax_tree import get_abstract_syntax_tree
from utilities.types.tree_node import TreeNode
from exploratory.data.adjacency_counts import write_adjacency_counts
from exploratory.data.path_counts import write_path_counts


def get_trees(src_rootdir : str):
    """
    Get list of abstract syntax trees from Fortran source files under a root directory
    """

    # Get source files
    filepaths = initialize(src_rootdir)
    
    # Get list of abstract syntax trees parsed from each source file
    trees = [get_abstract_syntax_tree(filepath) for filepath in filepaths]
    
    return trees


def write_data(trees : Iterable[TreeNode], data_rootdir : str):
    """
    Run all data writing routines
    """
    
    # Get and write adjacency counts
    write_adjacency_counts(trees, data_rootdir)
    
    # Get and write path counts
    write_path_counts(trees, data_rootdir)


def init_data(src_rootdir : str, data_rootdir : str):
    """
    Initialize data parsed from source files
    """
    
    # Read source files and generate trees
    trees = get_trees(src_rootdir)
    
    # Generate and write all data to file
    write_data(trees, data_rootdir)

    
if __name__ == "__main__":

    # Initialize data
    src_rootdir = "codes"
    data_rootdir = "data"
    init_data(src_rootdir, data_rootdir)