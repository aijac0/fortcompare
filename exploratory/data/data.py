from initial.initialize import initialize
from static_analysis.parsing.abstract_syntax_tree import get_abstract_syntax_tree
from exploratory.data.edge_counts import init_edge_counts
from exploratory.data.adjacent_counts import init_adjacent_counts
from exploratory.data.path_counts import init_path_counts
from exploratory.data.node_classes import init_node_classes


def get_trees(src_rootdir : str):
    """
    Get list of abstract syntax trees from Fortran source files under a root directory
    """

    # Get source files
    filepaths = initialize(src_rootdir)
    
    # Get list of abstract syntax trees parsed from each source file
    trees = [get_abstract_syntax_tree(filepath) for filepath in filepaths]
    
    return trees


def init_data(src_rootdir : str, data_rootdir : str):
    """
    Initialize data parsed from source files
    """
    
    # Read source files and generate trees
    trees = get_trees(src_rootdir)
    
    # Get and write edge counts to file
    edge_counts = init_edge_counts(trees, data_rootdir)
    
    # Get and write adjacent counts to file
    adj_counts = init_adjacent_counts(trees, data_rootdir)
    
    # Get and write path counts to file
    path_counts = init_path_counts(trees, data_rootdir)
    
    # Get and write node class parameters and node class declarations to file
    node_classes = init_node_classes(edge_counts, adj_counts, data_rootdir)

    return edge_counts, adj_counts, path_counts
    
    
if __name__ == "__main__":

    # Initialize data
    src_rootdir = "codes"
    data_rootdir = "data"
    init_data(src_rootdir, data_rootdir)