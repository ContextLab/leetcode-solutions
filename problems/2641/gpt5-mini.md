# [Problem 2641: Cousins in Binary Tree II](https://leetcode.com/problems/cousins-in-binary-tree-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to replace each node's value with the sum of all its cousins' values. "Cousins" are nodes on the same depth but with different parents. That suggests grouping by depth. A natural approach is level-order traversal (BFS): for each depth, we can know the total sum of node values at that depth. For a node, its cousins are all nodes at the same depth excluding its siblings (nodes with the same parent). So if we know the total sum at a level and the sum of a node's siblings, we can compute the cousin-sum = level_total - siblings_sum.

We must be careful with in-place updates: if we overwrite node values too early, later computations that rely on original values could be wrong. But if we process level by level and compute next-level totals using original child values before overwriting them, we can safely set new values for the next level. Alternatively, we could store original values in separate arrays, but BFS-level approach can avoid extra arrays.

Edgecases: root has no cousins -> 0. Nodes with a single child should be handled: siblings_sum is just that child's value.

## Refining the problem, round 2 thoughts
Refine BFS approach:
- Start from root. Set root.val = 0 because no cousins.
- For each level (nodes in queue), first compute total sum of all children of these nodes (this is the sum of values for the next depth).
- For each parent in the current level, compute sibling_sum = (left.val if exists) + (right.val if exists). For each child, set child.val = total_children_sum - sibling_sum.
- Enqueue the children (their values have just been updated) for processing the next level's children next iteration. That is safe because next iteration only needs the children's children original values (which haven't been modified yet).
- This runs in O(n) time (each node is touched O(1) times) and O(width) space.

Corner cases:
- Single-node tree: root becomes 0.
- Nodes with one child: sibling_sum equals that single child, result equals total - that child.
- Null child checks are important.

## Attempted solution(s)
```python
from collections import deque

# Definition for a binary tree node.
# (LeetCode provides this; included here for completeness)
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def replaceValueInTree(self, root: TreeNode) -> TreeNode:
        if not root:
            return None

        # Root has no cousins
        root.val = 0

        q = deque([root])
        while q:
            # Compute total sum of children values for the next level
            total_children_sum = 0
            for parent in q:
                if parent.left:
                    total_children_sum += parent.left.val
                if parent.right:
                    total_children_sum += parent.right.val

            # For every parent, compute sibling sum and assign new values to children
            next_level = deque()
            for parent in q:
                sibling_sum = 0
                if parent.left:
                    sibling_sum += parent.left.val
                if parent.right:
                    sibling_sum += parent.right.val

                # For each child, its new value is total_children_sum - sibling_sum
                if parent.left:
                    parent.left.val = total_children_sum - sibling_sum
                    next_level.append(parent.left)
                if parent.right:
                    parent.right.val = total_children_sum - sibling_sum
                    next_level.append(parent.right)

            q = next_level

        return root
```
- Notes about the solution:
  - Approach: Level-order traversal (BFS). At each level we compute the sum of all nodes at the next level (children of current nodes). For each parent, subtract the sum of its own children (siblings sum) from the total to get the cousin-sum for each child of that parent.
  - Important implementation detail: compute the total sum of children before updating any child's value so computations rely on original values.
  - Time complexity: O(n), where n is the number of nodes (each node is visited a constant number of times).
  - Space complexity: O(w), where w is the maximum width of the tree (queue size), worst-case O(n) for a very wide tree.