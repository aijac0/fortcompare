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
    initial_program_unit = True

    # Current line number
    line_num = 1

    # Iterate over each line of output 
    for line in raw_parse_tree.split('\n'):

        if not line: continue

        # Extract the depth of the node indicated by line and its associated "->" separated keywords
        curr_depth = 0
        curr_is_extended = False
        keyword = ""
        keywords = []
        depth_state = 0
        string_state = 1
        gap_state = 2
        keyword_state = 3
        state = depth_state
        for i in range(len(line)):
            c = line[i]
            match state:
                case 0:                                         # Depth state
                    match c:
                        case " ":
                            continue
                        case "|":
                            curr_depth += 1
                        case "'":
                            keyword = c
                            state = string_state
                        case default:
                            keyword = c
                            state = keyword_state
                case 1:                                         # String state
                    match c:
                        case "'":
                            keyword += c
                            if i == len(line) - 1:
                                keywords.append(keyword)
                        case default:
                            keyword += c
                case 2:                                         # Gap state
                    match c:
                        case " " | "=":
                            continue
                        case "-" | ">":
                            curr_is_extended = True
                        case "'":
                            keyword = c
                            state = string_state
                            curr_is_extended = False
                        case default:
                            keyword = c
                            state = keyword_state
                            curr_is_extended = False
                case 3:                                         # Keyword state
                    match c:
                        case " ":
                            keywords.append(keyword)
                            state = gap_state
                        case default:
                            keyword += c
                            if i == len(line) - 1:
                                keywords.append(keyword)

        # Add 1 to the depth of lines excluding the lines in the first program unit
        if curr_depth == 0 and head is not None:
            initial_program_unit = False
        curr_depth += not initial_program_unit

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
        prev_is_extended = curr_is_extended
        prev_depth = curr_depth
        line_num += 1

    return head