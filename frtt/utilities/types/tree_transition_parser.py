from __future__ import annotations
from utilities.types.tree_node import TreeNode

class TreeTransitionParser:
    """
    Class for implementing a tree parser by locally specifying state transitions and state functions for each node.
    """

    def __init__(self, data = None):
        """
        data : Input passed to each state function
        """
        self.data = data if data else dict()
        self.transitions = dict()       # curr_node -> curr_state -> next_node -> next_state
        self.functions = dict()         # node -> state -> f where f: data -> data  

    def is_transition(self, node1, node2, state1):
        """
        True if (node1, state1) -> (node2, state2) is a valid state transition
        False o.w.
        """
        return node1 in self.transitions and state1 in self.transitions[node1] and node2 in self.transitions[node1][state1]

    def get_transition(self, node1, node2, state1):
        """
        stateX if (node1, state1) -> (node2, stateX) is a valid state transition for some stateX 
        Error o.w.
        """
        if not self.is_transition(node1, node2, state1):
            raise Exception("Nonexistent state transition attempted: ({}, {}) -> ({}, ?)".format(node1, state1, node2))
        return self.transitions[node1][state1][node2]

    def add_transition(self, node1 : str, node2 : str, state1 : int, state2 : int):
        """
        Add (node1, state1) -> (node2, state2) as a valid state transition
        """
        if node1 not in self.transitions:
            self.transitions[node1] = dict()
        if state1 not in self.transitions[node1]:
            self.transitions[node1][state1] = dict()
        self.transitions[node1][state1][node2] = state2
        
    def get_function(self, node : str, state : int):
        """
        f if (node, state) has state function f specified
        Identity function o.w.
        """
        if node in self.functions and state in self.functions[node]:
            return self.functions[node][state]
        return (lambda x : x)                                           # Return identity function if none found                  
        
    def add_function(self, node : str, state : int, f):
        """
        Add f as the state function associated with (node, state)
        """
        if node not in self.functions:
            self.functions[node] = dict()
        self.functions[node][state] = f
        
    def parse(self, node : TreeNode, state : int):
        """
        Execute function associated with (node, state) if it exists.
        Depth first transition to the applicable state of each child node.
        """
        self.get_function(node.name(), state)(self.data)
        for next_node in node.children:
            next_state = self.get_transition(node.name(), next_node.name(), state)
            self.parse(next_node, next_state)
            
    def to_file(self, filepath : str):
        pass
            
    @classmethod
    def from_file(cls, filepath : str) -> TreeTransitionParser:
        pass
            
    @classmethod
    def from_tree(cls, tree : TreeNode) -> TreeTransitionParser:
        
        # Tree transition parser to create
        ttp = TreeTransitionParser()
        
        # Keep track of number of states allocated to each node
        n_states = dict()
        
        # DFS tree for node occurrences
        stack = [(tree, 0)]
        n_states[tree.name()] = 1
        while stack:
            curr_node, curr_state = stack.pop()
            curr_name = curr_node.name()
            
            # Iterate over next nodes
            for next_node in curr_node.children:
                next_name = next_node.name()
                
                # Add new state for next node to uniquely identify path from head
                if next_name not in n_states: n_states[next_name] = 0
                next_state = n_states[next_name]
                n_states[next_name] += 1
                
                # Add state transition
                ttp.add_transition(curr_name, next_name, curr_state, next_state)
                
                # Add next node to stack
                stack.append((next_node, next_state))
                
        return ttp