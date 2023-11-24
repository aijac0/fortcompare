from __future__ import annotations
from typing import Type
from abc import ABC, abstractmethod, abstractproperty


"""
Mock constructor
Returns the constructor of the superclass of the class that self belongs to with *args passed
"""
def constructor(*args):
    def inner(self):
        self.__class__.__base__.__init__(self, *args)
    return inner

"""
Abstract node
"""
class Node(ABC):
    @property
    def adj(self):
        return list(self.adj_gen)
    @property
    def adj_gen(self):
        for adj_gen in self.adj_gens:
            for c in adj_gen:
                yield c
    @abstractproperty
    def adj_gens(self):
        pass
    @abstractmethod
    def add_adj(self, node : Node):
        pass
        
"""
Node with no children
"""
class LeafNode(Node):
    @property
    def adj_gen(self):
        return iter(())
    def add_adj(self, node : Node):
        return False
    

"""
Node with a single child from a variable number of classes
"""
class SelectorNode(Node):

    def __init__(self, *args : Type[Node]):
        self.c = None
        self.cls_map = dict()
        
        # Add classes to class map
        for i in range(len(args)):
            self.cls_map[args[i]] = i
            
    @property
    def adj_gen(self):
        if self.c: yield self.c
        
    def add_adj(self, node: Node):
        if node.__class__ in self.cls_map:
            self.c = node
            return True
        return False
    
"""
Node with a variable number of children from a variable number of classes
"""
class MultiNode(Node):
    
    def __init__(self, *args : Type[Node]):
        self.cs = list()
        self.cls_map = dict()
        
        # Add classes to class map
        for i in range(len(args)):
            self.cls_map[args[i]] = i
            self.cs.append(list())
        
    @property
    def adj_gen(self):
        for ci in self.cs:
            for c in ci:
                yield c
        
    def add_adj(self, node : Node):
        if node.__class__ in self.cls_map:
            idx = self.cls_map[node.__class__]
            self.cs[idx].append(node)
            return True
        return False