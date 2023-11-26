from typing import Iterable
from collections import deque
from utilities.types.tree_node import TreeNode


def partially_relocate(trees : Iterable[TreeNode]):
    """
    Create a tree that is structurally equivalent to a set of trees
    Assumes that two nodes are equal if and only if:
    1. They have the same identifier
    2. Identifier is not statically recursive
    """
    pass