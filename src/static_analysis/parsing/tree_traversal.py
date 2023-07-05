import subprocess
from static_analysis.parsing.program_units import parse_programunit

class TreeNode:

    def __init__(self, value):
        self.value = value
        self.children = []


    def walk(self, targets, exception_handling=False):
        """
        Traverse parse tree and return all nodes with a value equal to one of the target values
        :targets: Value to search for / List of values to search for
        :exception_handling: Whether or not to raise exception if no nodes are found
        :return: List of nodes matching one of the target values
        """

        # Convert targets to list if not already
        if not type(targets) == list:
            targets = [targets]

        # List to return
        nodes = []

        # Stack to hold next node to search
        stack = [child for child in reversed(self.children)]

        # Depth first search
        while len(stack):
            node = stack.pop()
            stack.extend(child for child in reversed(node.children))
            if node.value in targets: nodes.append(node)

        # Handle exception if enabled
        if exception_handling and len(nodes) == 0:
            raise Exception("Node not found during walk(): targets = {}".format(targets))

        return nodes


    def step(self, targets, exception_handling=False):
        """
        Get the first descendent of parse tree with a value equal to one of the target values
        :targets: Value to search for / List of values to search for
        :exception_handling: Whether or not to raise exception if no nodes are found
        :return: First node (least depth) matching one of the target values
        """

        # Convert targets to list if not already
        if not type(targets) == list:
            targets = [targets]

        # Queue to hold next node to search
        queue = [child for child in reversed(self.children)]

        # Breadth first search
        while len(queue):
            node = queue.pop(0)
            queue.extend(child for child in reversed(node.children))
            if node.value in targets: return node

        # Handle exception if enabled
        if exception_handling:
            raise Exception("Node not found during step(): targets = {}".format(targets))

        return None

    
    def kins(self, targets, exception_handling=False):
        """
        Get all the immediate children of parse tree with a value equal to one of the target values
        :targets: Value to search for / List of values to search for
        :exception_handling: Whether or not to raise exception if no nodes are found
        :return: List of immediate children nodes matching one of the target values
        """

        # Convert targets to list if not already
        if not type(targets) == list:
            targets = [targets]

        # List to return
        nodes = []

        # Iterate over each child of node
        for child in self.children:
            if child.value in targets:
                nodes.append(child)

        # Handle exception if enabled
        if exception_handling and len(nodes) == 0:
            raise Exception("Node not found during kins(): targets = {}".format(targets))

        return nodes


    def kin(self, targets, exception_handling=False):
        """
        Get the first immediate child of parse tree with a value equal to one of the target values
        :targets: Value to search for / List of values to search for
        :exception_handling: Whether or not to raise exception if no nodes are found
        :return: Immediate child node matching one of the target values
        """

        # Convert targets to list if not already
        if not type(targets) == list:
            targets = [targets]
        
        # Iterate over each child of node
        for child in self.children:
            if child.value in targets:
                return child

        # Handle exception if enabled
        if exception_handling:
            raise Exception("Node not found during kin(): targets = {}".format(targets))

        return None


    def leaves(self, exception_handling=False):
        """
        Traverse parse tree and return a list of all leaf nodes (nodes with no children)
        :exception_handling: Whether or not to raise exception if no nodes are found
        :return: List of leaf nodes
        """

        # List to return
        nodes = []

        # Stack to hold next node to search
        stack = [child for child in reversed(self.children)]

        # Depth first search
        while len(stack):
            node = stack.pop()
            if node.children:
                stack.extend(child for child in reversed(node.children))
            else:
                nodes.append(node)

        # Handle exception if enabled
        if exception_handling and len(nodes) == 0:
            raise Exception("Node not found during leaves()")

        return nodes


    def leaf(self, exception_handling=False):
        """
        Traverse parse tree and return the first leaf node (nodes with no children)
        :exception_handling: Whether or not to raise exception if no nodes are found
        :return: First leaf node (least depth)
        """
        
        # Queue to hold next node to search
        queue = [child for child in reversed(self.children)]

        # Breadth first search
        while len(queue):
            node = queue.pop(0)
            if node.children:
                queue.extend(child for child in reversed(node.children))
            else:
                return node

        # Handle exception if enabled
        if exception_handling:
            raise Exception("Node not found during leaf()")
        
        return None


    def to_string(self):
        """
        DFS search the parse tree and append each node to string with '|' symbols to indicate depth
        :return: String representation of tree
        """
        
        # String to return
        out_str = str(self.value) + '\n'

        # Stack to hold next node to search and its associated depth
        stack = [(1, child) for child in reversed(self.children)]

        # Depth first search
        while len(stack):
            depth, node = stack.pop()
            stack.extend([(depth + 1, child) for child in reversed(node.children)])
            out_str += ("| " * depth if depth else "") + str(node.value) + '\n'
        return out_str


class ParseTree:

    def __init__(self, source_filepath):
        self.head = ParseTree.generate_parse_tree(source_filepath)

    def parse(self):
        """
        Get a list of ProgramUnit objects containing information about each program unit (module, function, subroutine) in parse tree
        :rvalue: List of ProgramUnits
        """
    
        # Get a list of the subtrees representing a program unit
        subtrees = self.head.walk("ProgramUnit")
        
        # Get the ProgramUnit representation of each subtree
        return [parse_programunit(subtree) for subtree in subtrees]


    @classmethod
    def generate_parse_tree(cls, source_filepath):
        """
        Generate a flang parse tree of source_filepath and create a nested Node representation.
        :source_filepath: Fortran source file to generate flang parse tree for
        :return: TreeNode representation of flang parse tree
        """

        # Get the raw string representation of parse tree
        raw_parse_tree = subprocess.check_output("flang-new -fc1 -fdebug-dump-parse-tree-no-sema {}".format(source_filepath), shell=True, text=True)  

        # Stack to hold all parent nodes to backtrack to
        stack = []

        # Initialize variables
        head = TreeNode(source_filepath)
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

            # Add new node as a child of its parent
            parent.children.append(new_node)
        
            # Update vars
            prev_node = curr_node
            prev_is_extended = (tokens[-1] == "->")
            prev_depth = curr_depth
            line_num += 1

        return head