"""
Utility functions for working with binary trees.
"""

from typing import Optional, List
from collections import deque
from .data_structures import TreeNode


def list_to_tree(values: List[Optional[int]]) -> Optional[TreeNode]:
    """
    Convert a list to a binary tree (level-order representation).
    
    This matches LeetCode's format where None represents null nodes.
    
    Args:
        values: List of values in level-order, with None for null nodes
        
    Returns:
        Root node of the created binary tree, or None if input is empty
        
    Example:
        >>> tree = list_to_tree([1, 2, 3, 4, 5, None, 7])
        >>> # Creates:
        >>>      1
        >>>     / \\
        >>>    2   3
        >>>   / \\   \\
        >>>  4   5   7
    """
    if not values or values[0] is None:
        return None
    
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    
    while queue and i < len(values):
        node = queue.popleft()
        
        # Process left child
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        
        # Process right child
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    
    return root


def tree_to_list(root: Optional[TreeNode]) -> List[Optional[int]]:
    """
    Convert a binary tree to a list (level-order representation).
    
    This matches LeetCode's format where None represents null nodes.
    Trailing None values are removed.
    
    Args:
        root: Root node of the binary tree
        
    Returns:
        List of values in level-order, with None for null nodes
        
    Example:
        >>> tree = TreeNode(1)
        >>> tree.left = TreeNode(2)
        >>> tree.right = TreeNode(3)
        >>> tree_to_list(tree)
        [1, 2, 3]
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        
        if node is None:
            result.append(None)
        else:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    
    # Remove trailing None values
    while result and result[-1] is None:
        result.pop()
    
    return result


def visualize_tree(root: Optional[TreeNode], level: int = 0, prefix: str = "Root: ") -> str:
    """
    Create a visual string representation of a binary tree.
    
    Args:
        root: Root node of the binary tree
        level: Current depth level (used for recursion, default 0)
        prefix: Prefix string for the current node (default "Root: ")
        
    Returns:
        String representation of the tree structure
        
    Example:
        >>> tree = list_to_tree([1, 2, 3, 4, 5])
        >>> print(visualize_tree(tree))
        Root: 1
        ├─ L: 2
        │  ├─ L: 4
        │  └─ R: 5
        └─ R: 3
    """
    if not root:
        return ""
    
    lines = []
    lines.append(prefix + str(root.val))
    
    if root.left or root.right:
        if root.left:
            extension = "│  " if root.right else "   "
            lines.append(visualize_tree(root.left, level + 1, 
                                       ("│  " * level) + "├─ L: ").rstrip())
        
        if root.right:
            lines.append(visualize_tree(root.right, level + 1,
                                       ("│  " * level) + "└─ R: ").rstrip())
    
    return "\n".join(lines)


def print_tree(root: Optional[TreeNode]) -> None:
    """
    Print a visual representation of a binary tree.
    
    Args:
        root: Root node of the binary tree
        
    Example:
        >>> tree = list_to_tree([1, 2, 3, 4, 5])
        >>> print_tree(tree)
        Root: 1
        ├─ L: 2
        │  ├─ L: 4
        │  └─ R: 5
        └─ R: 3
    """
    if not root:
        print("Empty tree")
    else:
        print(visualize_tree(root))


def get_tree_height(root: Optional[TreeNode]) -> int:
    """
    Calculate the height of a binary tree.
    
    Args:
        root: Root node of the binary tree
        
    Returns:
        Height of the tree (number of edges on longest path from root to leaf)
        
    Example:
        >>> tree = list_to_tree([1, 2, 3, 4, 5])
        >>> get_tree_height(tree)
        2
    """
    if not root:
        return -1
    
    return 1 + max(get_tree_height(root.left), get_tree_height(root.right))


def count_nodes(root: Optional[TreeNode]) -> int:
    """
    Count the total number of nodes in a binary tree.
    
    Args:
        root: Root node of the binary tree
        
    Returns:
        Total number of nodes in the tree
        
    Example:
        >>> tree = list_to_tree([1, 2, 3, 4, 5])
        >>> count_nodes(tree)
        5
    """
    if not root:
        return 0
    
    return 1 + count_nodes(root.left) + count_nodes(root.right)
