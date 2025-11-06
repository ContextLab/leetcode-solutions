"""
LeetCode Helper Functions

This package provides utility functions and data structures for solving LeetCode problems.

Main modules:
- data_structures: Common data structures (TreeNode, ListNode)
- tree_utils: Binary tree utilities (conversions, visualization)
- linked_list_utils: Linked list utilities (conversions, helpers)
- algorithms: Common algorithms (BFS, DFS, tree search)
"""

from .data_structures import TreeNode, ListNode
from .tree_utils import (
    list_to_tree,
    tree_to_list,
    print_tree,
    visualize_tree,
    get_tree_height,
    count_nodes
)
from .linked_list_utils import (
    list_to_linked_list,
    linked_list_to_list,
    print_linked_list,
    get_linked_list_length,
    get_node_at_index
)
from .algorithms import (
    bfs_traversal,
    dfs_preorder,
    dfs_inorder,
    dfs_postorder,
    level_order_traversal,
    find_path_to_node,
    lowest_common_ancestor,
    search_bst,
    is_valid_bst
)

__all__ = [
    # Data structures
    'TreeNode',
    'ListNode',
    # Tree utilities
    'list_to_tree',
    'tree_to_list',
    'print_tree',
    'visualize_tree',
    'get_tree_height',
    'count_nodes',
    # Linked list utilities
    'list_to_linked_list',
    'linked_list_to_list',
    'print_linked_list',
    'get_linked_list_length',
    'get_node_at_index',
    # Algorithms
    'bfs_traversal',
    'dfs_preorder',
    'dfs_inorder',
    'dfs_postorder',
    'level_order_traversal',
    'find_path_to_node',
    'lowest_common_ancestor',
    'search_bst',
    'is_valid_bst',
]
