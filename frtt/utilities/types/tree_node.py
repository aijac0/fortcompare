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
        queue = [child for child in self.children]

        # Breadth first search
        while len(queue):
            node = queue.pop(0)
            queue.extend(child for child in node.children)
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
        queue = [child for child in self.children]

        # Breadth first search
        while len(queue):
            node = queue.pop(0)
            if node.children:
                queue.extend(child for child in node.children)
            else:
                return node

        # Handle exception if enabled
        if exception_handling:
            raise Exception("Node not found during leaf()")
        
        return None


    def deep_copy(self):
        head = TreeNode(self.value)
        stack = [(head, next) for next in self.children]
        while stack:
            prev, curr = stack.pop()
            new = TreeNode(curr.value)
            prev.children.append(new)
            stack.extend([(new, next) for next in curr.children])
        return head

    def __str__(self):
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