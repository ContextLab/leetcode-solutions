# [Problem 2415: Reverse Odd Levels of Binary Tree](https://leetcode.com/problems/reverse-odd-levels-of-binary-tree/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The tree is perfect, so every internal node has two children and all leaves are at the same depth. We need to reverse node *values* at every odd level (level counting edges from root, root at level 0). One straightforward way is level-order traversal: collect nodes per level, and for odd levels swap their values. But because the tree is perfect, we can do better with a symmetric (mirror) DFS: pair nodes that are mirror images (left subtree node vs corresponding right subtree node). For any odd level, swapping values of each mirror pair achieves the full reversal across that level. This lets us do the transformation in-place with O(n) time and O(h) additional space (recursion stack).

## Refining the problem, round 2 thoughts
- Start by pairing root.left and root.right at level 1. If level is odd, swap their .val.
- Recurse into the next pairs in mirrored order:
  - pair left.left with right.right
  - pair left.right with right.left
- Stop when leaf level (or either node is None).
- Edge cases: single node tree (nothing to change). Because tree is perfect, once one of a pair is None both are None, but we still guard.
- Complexity: each node visited once -> O(n) time. Recursion depth = tree height = O(log n) for perfect tree, so O(log n) space.

## Attempted solution(s)
```python
# Definition for a binary tree node (included for completeness).
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def reverseOddLevels(self, root: TreeNode) -> TreeNode:
        if not root:
            return root

        def helper(left: TreeNode, right: TreeNode, level: int) -> None:
            if not left or not right:
                return
            # If current level is odd, swap the values of mirror nodes
            if level % 2 == 1:
                left.val, right.val = right.val, left.val
            # Recurse to the next level with mirrored pairs
            helper(left.left, right.right, level + 1)
            helper(left.right, right.left, level + 1)

        # Start with the pair of nodes at level 1
        helper(root.left, root.right, 1)
        return root
```
- Notes:
  - Approach: mirror-pair DFS. For each pair of mirror nodes at an odd level, swap their values. Recurse into mirrored children pairs.
  - Time complexity: O(n) — each node is visited a constant number of times.
  - Space complexity: O(h) recursion stack where h is tree height. For a perfect binary tree h = O(log n).