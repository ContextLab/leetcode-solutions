# [Problem 1123: Lowest Common Ancestor of Deepest Leaves](https://leetcode.com/problems/lowest-common-ancestor-of-deepest-leaves/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the lowest common ancestor (LCA) of the deepest leaves. That suggests we must first know which leaves are deepest (or at least the maximum depth) and then find the LCA of that set. A natural approach is a single post-order DFS that computes the depth of the deepest leaf in each subtree and simultaneously determines the LCA for the deepest leaves under that subtree.

For each node:
- get deepest depth (distance from node down to deepest leaf) for left and right children
- if left_depth == right_depth, then the deepest leaves under this node are in both sides so this node is the LCA for those deepest leaves
- if one side deeper, propagate that side's LCA upward

This gives a straightforward O(n) recursion.

## Refining the problem, round 2 thoughts
Edge cases: tree with a single node (answer is root), tree skewed (answer is deepest node itself), multiple deepest leaves on different subtrees (answer is their LCA). Implementation detail: choose a consistent depth convention for None nodes (e.g., -1) so that leaf nodes compute depth 0.

Alternative approaches: BFS to find deepest level nodes, then use parent pointers to compute LCA iteratively. That also works but requires storing parent map and then taking intersection or repeated parent moves — still O(n) time and extra space. The single DFS postorder is simpler and uses only recursion stack O(h) extra space.

Time complexity: O(n) because each node visited once.
Space complexity: O(h) recursion stack (h = tree height), worst-case O(n).

## Attempted solution(s)
```python
from typing import Optional, Tuple

# Definition for a binary tree node (LeetCode standard).
class TreeNode:
    def __init__(self, val: int = 0, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def lcaDeepestLeaves(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Returns (depth, node) where depth is the max distance from `root` to a deepest leaf
        (leaf depth relative to this node), and node is the LCA of deepest leaves in this subtree.
        For None, return (-1, None) so leaf nodes compute depth 0.
        """
        def dfs(node: Optional[TreeNode]) -> Tuple[int, Optional[TreeNode]]:
            if not node:
                return -1, None  # depth -1 for null to make leaf depth 0
            left_depth, left_lca = dfs(node.left)
            right_depth, right_lca = dfs(node.right)
            if left_depth == right_depth:
                # both sides have deepest leaves at same depth => current node is LCA
                return left_depth + 1, node
            elif left_depth > right_depth:
                return left_depth + 1, left_lca
            else:
                return right_depth + 1, right_lca

        _, lca_node = dfs(root)
        return lca_node
```
- Approach: single post-order DFS that returns (max depth from current node to deepest leaf, LCA of deepest leaves in this subtree). If left and right subtrees have equal deepest depth, current node is the LCA; otherwise propagate the deeper side's LCA upward.
- Time complexity: O(n) where n is number of nodes (each node processed once).
- Space complexity: O(h) recursion stack where h is the tree height (worst-case O(n)).