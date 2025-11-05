"""
Common algorithms for tree and graph traversal.
"""

from typing import Optional, List, Callable
from collections import deque
from .data_structures import TreeNode


def bfs_traversal(root: Optional[TreeNode]) -> List[int]:
    """
    Breadth-First Search (BFS) traversal of a binary tree.
    Also known as level-order traversal.
    
    Args:
        root: Root node of the binary tree
        
    Returns:
        List of node values in BFS order
        
    Example:
        >>> from helpers.tree_utils import list_to_tree
        >>> tree = list_to_tree([1, 2, 3, 4, 5])
        >>> bfs_traversal(tree)
        [1, 2, 3, 4, 5]
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        result.append(node.val)
        
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    
    return result


def dfs_preorder(root: Optional[TreeNode]) -> List[int]:
    """
    Depth-First Search (DFS) traversal - Pre-order (Root, Left, Right).
    
    Args:
        root: Root node of the binary tree
        
    Returns:
        List of node values in pre-order
        
    Example:
        >>> from helpers.tree_utils import list_to_tree
        >>> tree = list_to_tree([1, 2, 3, 4, 5])
        >>> dfs_preorder(tree)
        [1, 2, 4, 5, 3]
    """
    if not root:
        return []
    
    result = [root.val]
    result.extend(dfs_preorder(root.left))
    result.extend(dfs_preorder(root.right))
    
    return result


def dfs_inorder(root: Optional[TreeNode]) -> List[int]:
    """
    Depth-First Search (DFS) traversal - In-order (Left, Root, Right).
    For Binary Search Trees, this gives sorted order.
    
    Args:
        root: Root node of the binary tree
        
    Returns:
        List of node values in in-order
        
    Example:
        >>> from helpers.tree_utils import list_to_tree
        >>> tree = list_to_tree([1, 2, 3, 4, 5])
        >>> dfs_inorder(tree)
        [4, 2, 5, 1, 3]
    """
    if not root:
        return []
    
    result = []
    result.extend(dfs_inorder(root.left))
    result.append(root.val)
    result.extend(dfs_inorder(root.right))
    
    return result


def dfs_postorder(root: Optional[TreeNode]) -> List[int]:
    """
    Depth-First Search (DFS) traversal - Post-order (Left, Right, Root).
    
    Args:
        root: Root node of the binary tree
        
    Returns:
        List of node values in post-order
        
    Example:
        >>> from helpers.tree_utils import list_to_tree
        >>> tree = list_to_tree([1, 2, 3, 4, 5])
        >>> dfs_postorder(tree)
        [4, 5, 2, 3, 1]
    """
    if not root:
        return []
    
    result = []
    result.extend(dfs_postorder(root.left))
    result.extend(dfs_postorder(root.right))
    result.append(root.val)
    
    return result


def level_order_traversal(root: Optional[TreeNode]) -> List[List[int]]:
    """
    Level-order traversal returning nodes grouped by level.
    
    Args:
        root: Root node of the binary tree
        
    Returns:
        List of lists, where each inner list contains values at that level
        
    Example:
        >>> from helpers.tree_utils import list_to_tree
        >>> tree = list_to_tree([1, 2, 3, 4, 5])
        >>> level_order_traversal(tree)
        [[1], [2, 3], [4, 5]]
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level_nodes = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level_nodes.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level_nodes)
    
    return result


def find_path_to_node(root: Optional[TreeNode], target: int) -> Optional[List[int]]:
    """
    Find the path from root to a target node value.
    
    Args:
        root: Root node of the binary tree
        target: Value to search for
        
    Returns:
        List of node values representing the path, or None if not found
        
    Example:
        >>> from helpers.tree_utils import list_to_tree
        >>> tree = list_to_tree([1, 2, 3, 4, 5])
        >>> find_path_to_node(tree, 5)
        [1, 2, 5]
    """
    if not root:
        return None
    
    if root.val == target:
        return [root.val]
    
    # Search in left subtree
    left_path = find_path_to_node(root.left, target)
    if left_path:
        return [root.val] + left_path
    
    # Search in right subtree
    right_path = find_path_to_node(root.right, target)
    if right_path:
        return [root.val] + right_path
    
    return None


def lowest_common_ancestor(root: Optional[TreeNode], p: int, q: int) -> Optional[TreeNode]:
    """
    Find the lowest common ancestor (LCA) of two nodes in a binary tree.
    
    Args:
        root: Root node of the binary tree
        p: Value of first node
        q: Value of second node
        
    Returns:
        The LCA node, or None if either node is not found
        
    Example:
        >>> from helpers.tree_utils import list_to_tree
        >>> tree = list_to_tree([3, 5, 1, 6, 2, 0, 8])
        >>> lca = lowest_common_ancestor(tree, 5, 1)
        >>> lca.val
        3
    """
    if not root:
        return None
    
    if root.val == p or root.val == q:
        return root
    
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    
    if left and right:
        return root
    
    return left if left else right


def search_bst(root: Optional[TreeNode], target: int) -> Optional[TreeNode]:
    """
    Search for a value in a Binary Search Tree.
    
    Args:
        root: Root node of the BST
        target: Value to search for
        
    Returns:
        Node with the target value, or None if not found
        
    Example:
        >>> from helpers.tree_utils import list_to_tree
        >>> tree = list_to_tree([4, 2, 7, 1, 3])
        >>> node = search_bst(tree, 2)
        >>> node.val
        2
    """
    if not root or root.val == target:
        return root
    
    if target < root.val:
        return search_bst(root.left, target)
    else:
        return search_bst(root.right, target)


def is_valid_bst(root: Optional[TreeNode], min_val: float = float('-inf'), 
                 max_val: float = float('inf')) -> bool:
    """
    Check if a binary tree is a valid Binary Search Tree.
    
    Args:
        root: Root node of the binary tree
        min_val: Minimum allowed value (used internally for recursion)
        max_val: Maximum allowed value (used internally for recursion)
        
    Returns:
        True if the tree is a valid BST, False otherwise
        
    Example:
        >>> from helpers.tree_utils import list_to_tree
        >>> tree = list_to_tree([2, 1, 3])
        >>> is_valid_bst(tree)
        True
    """
    if not root:
        return True
    
    if root.val <= min_val or root.val >= max_val:
        return False
    
    return (is_valid_bst(root.left, min_val, root.val) and 
            is_valid_bst(root.right, root.val, max_val))
