from subprocess import check_output
from frtt.utilities.types.tree_node import TreeNode

def get_abstract_syntax_tree(source_filepath):
    """
    Get the abstract syntax tree representation of a Fortran source file from the Flang command
    :source_filepath: Fortran source file to generate flang parse tree for
    :return: TreeNode representation of flang abstract syntax tree
    """

    # Get the raw string representation of AST
    raw_parse_tree = check_output("flang-new -fc1 -fdebug-dump-parse-tree-no-sema {}".format(source_filepath), shell=True, text=True)  

    # Stack to hold all parent nodes to backtrack to
    stack = []

    # Initialize variables
    head = None
    parent = None
    parent_is_extended = False
    prev_node = head
    prev_is_extended = False
    prev_depth = -1

    # Current line number
    line_num = 1

    # Iterate over each line of output 
    for line in raw_parse_tree.split('\n'):

        # Separate line into tokens
        tokens = line.split(' ')
        tokens = [i for i in tokens if i]
        if not tokens: continue

        # Extract the depth of the node indicated by line and its associated "->" separated keywords
        curr_depth = 0
        keywords = []
        for t in range(len(tokens)):
            if tokens[t] == "|":
                if not keywords:
                    curr_depth += 1
                    continue
            if (tokens[t] != "->" and tokens[t] != "="):
                keywords.append(tokens[t])

        # Get the parent of the current node
        if curr_depth + prev_is_extended == prev_depth + 1:  # Node is at a depth of exactly one greater than the previous node (or depths are equal and previous line is extended)
            stack.append((parent_is_extended, parent))
            parent = prev_node
            parent_is_extended = prev_is_extended
        elif curr_depth <= prev_depth:                       # Node is at a depth less than or equal to the previous node
            num_pops = prev_depth - curr_depth
            while num_pops > 0:
                if not parent_is_extended: num_pops -= 1     # For each extended parent, pop another parent off the stack (excluding the last parent)
                parent_is_extended, parent = stack.pop()
        else:                                                # Node is at a depth more than one greater than the previous node
            raise Exception("Invalid depth in parse tree at line {}".format(line_num))
    
        # Get the node associated with the current line
        new_node = None
        for kw in keywords:
            child_node = TreeNode(kw)
            if not new_node:
                new_node = curr_node = child_node
            else:
                curr_node.children.append(child_node)
                curr_node = child_node

        # Add new node as a child of its parent, or initialize head if uninitialized
        if not head:
            head = new_node
            parent = head
        else:
            parent.children.append(new_node)
            
    
        # Update vars
        prev_node = curr_node
        prev_is_extended = (tokens[-1] == "->")
        prev_depth = curr_depth
        line_num += 1

    return head