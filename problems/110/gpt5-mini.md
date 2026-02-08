# [Problem 110: Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to check whether a binary tree is height-balanced: for every node, the heights of left and right subtrees differ by at most 1. The naive approach is to compute height for each node by calling a height function on left and right, and checking abs(left - right) <= 1. But if implemented naively this can lead to repeated height computations and O(n^2) time on skewed trees.

A better approach is to do a single post-order traversal that computes the height of a subtree and also indicates if it's unbalanced. The traversal returns height if balanced, or a sentinel (e.g., -1) to indicate unbalanced. If any subtree is unbalanced, propagate the sentinel up immediately, allowing early termination.

This leads to O(n) time and O(h) recursion space, where h is tree height.

## Refining the problem, round 2 thoughts
- Edge cases: empty tree should be balanced (return True). Single node is balanced.
- Use post-order (left, right, node) to compute heights bottom-up and detect imbalance early.
- Implementation detail: using -1 as sentinel is convenient because heights are non-negative.
- Alternative: track balanced boolean separately and compute heights; but combining into one return value is simpler and more efficient.
- Complexity: each node visited once -> O(n) time. Recursion depth equals tree height -> O(h) space (stack).

## Attempted solution(s)
```python
# Definition for a binary tree node (provided by LeetCode environment).
# Included here for completeness.
from typing import Optional

class TreeNode:
    def __init__(self, val: int = 0, left: 'Optional[TreeNode]' = None, right: 'Optional[TreeNode]' = None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        """
        Returns True if the tree is height-balanced, False otherwise.
        Uses post-order traversal and returns -1 as a sentinel for unbalanced subtree.
        """
        def height_or_minus_one(node: Optional[TreeNode]) -> int:
            if node is None:
                return 0
            left_h = height_or_minus_one(node.left)
            if left_h == -1:
                return -1  # left subtree unbalanced, propagate
            right_h = height_or_minus_one(node.right)
            if right_h == -1:
                return -1  # right subtree unbalanced, propagate
            if abs(left_h - right_h) > 1:
                return -1  # current node unbalanced
            return 1 + max(left_h, right_h)

        return height_or_minus_one(root) != -1
```
- Notes:
  - Approach: single post-order DFS that returns subtree height or -1 if subtree is unbalanced.
  - Time complexity: O(n), each node visited once.
  - Space complexity: O(h) recursion stack, where h is the tree height (O(n) worst-case skewed, O(log n) best-case balanced).
  - This implementation allows early exit when an unbalanced subtree is discovered, avoiding unnecessary work.