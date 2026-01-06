# [Problem 1161: Maximum Level Sum of a Binary Tree](https://leetcode.com/problems/maximum-level-sum-of-a-binary-tree/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Sorry — I can’t share my internal stream-of-consciousness. Instead, here is a concise summary of the approach I will use: perform a breadth-first traversal (level-order) of the tree, compute the sum of node values at each level, and keep track of the level with the maximum sum (return the smallest such level in case of ties).

## Refining the problem, round 2 thoughts
- A BFS (queue) is a natural fit because the problem asks about level sums.
- Maintain a running best sum and the level index (1-based). Initialize with the root level.
- For each BFS layer, compute the sum of nodes in that layer, then compare to the best sum; update best level if strictly greater (ties are resolved by keeping the earlier/smaller level).
- Edge cases:
  - The tree has only one node — return 1.
  - Node values can be negative — initialize best sum using the root value (or use -inf).
- Time complexity: O(n) since every node is visited once.
- Space complexity: O(w) where w is the maximum width of the tree (O(n) worst-case).

## Attempted solution(s)
```python
# Definition for a binary tree node.
# Provided by LeetCode environment; included here for completeness.
from typing import Optional
from collections import deque

class TreeNode:
    def __init__(self, val: int = 0, left: 'Optional[TreeNode]' = None, right: 'Optional[TreeNode]' = None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def maxLevelSum(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0  # problem constraints guarantee at least one node, but keep safe behavior

        q = deque([root])
        level = 1
        best_level = 1
        best_sum = root.val  # initialize with root value to handle negative values correctly

        while q:
            size = len(q)
            level_sum = 0
            for _ in range(size):
                node = q.popleft()
                level_sum += node.val
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)

            if level_sum > best_sum:
                best_sum = level_sum
                best_level = level

            level += 1

        return best_level
```
- Notes:
  - Approach: level-order traversal (BFS) computing sums per level and tracking the maximum sum and associated smallest level.
  - Time complexity: O(n), n = number of nodes (each node visited once).
  - Space complexity: O(w), w = maximum width of the tree (queue size), worst-case O(n).