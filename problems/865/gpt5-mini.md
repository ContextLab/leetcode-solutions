# [Problem 865: Smallest Subtree with all the Deepest Nodes](https://leetcode.com/problems/smallest-subtree-with-all-the-deepest-nodes/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I want the smallest subtree that contains all nodes at the maximum depth. That sounds like finding the deepest leaves, then returning their lowest common ancestor (LCA). A straightforward approach: compute depth information bottom-up and decide at each node whether its left and right subtrees contain deepest nodes and pick the node accordingly. I recall a neat post-order trick: for each node return the height (max depth of leaves under it) and the best subtree root that contains all deepest nodes in that subtree. If left and right heights are equal, current node is the answer for that subtree; otherwise pick the side with greater height. This will give O(n) time and O(h) recursion stack.

## Refining the problem, round 2 thoughts
Edge cases: single node tree (should return root). Skewed tree (LCA is deepest node). Multiple deepest leaves spread across subtrees (LCA could be above them). Alternative solutions: BFS to find all deepest leaves then compute their LCA using parent map; that also works but requires extra passes. The bottom-up DFS that returns (height, candidate) is concise and single-pass.

Time complexity: O(n) where n is number of nodes (visiting each node once). Space complexity: O(h) recursion stack where h is tree height (worst-case O(n) if skewed).

## Attempted solution(s)
```python
# Definition for a binary tree node.
from typing import Optional, Tuple

class TreeNode:
    def __init__(self, val: int = 0, left: 'Optional[TreeNode]' = None, right: 'Optional[TreeNode]' = None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def subtreeWithAllDeepest(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        # Returns a pair (height, node) where height is the max depth of leaves under `node`
        # and `node` is the smallest subtree root that contains all deepest nodes in this subtree.
        def dfs(node: Optional[TreeNode]) -> Tuple[int, Optional[TreeNode]]:
            if node is None:
                return 0, None
            left_h, left_node = dfs(node.left)
            right_h, right_node = dfs(node.right)
            if left_h == right_h:
                # deepest nodes are equally deep on both sides -> current node is LCA
                return left_h + 1, node
            elif left_h > right_h:
                return left_h + 1, left_node
            else:
                return right_h + 1, right_node

        return dfs(root)[1]
```
- Notes on approach: The DFS returns the height (number of nodes on longest path from current node down to a deepest leaf) and the candidate subtree root that contains all deepest nodes in that subtree. When both child heights are equal, the current node is the smallest subtree containing all deepest nodes under it. Otherwise we propagate the candidate from the deeper side.
- Complexity: Time O(n) visiting each node once; Space O(h) recursion stack (h = tree height, worst-case O(n)).