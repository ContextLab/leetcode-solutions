# [Problem 1382: Balance a Binary Search Tree](https://leetcode.com/problems/balance-a-binary-search-tree/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can't share private chain-of-thought or stream-of-consciousness. Instead, here's a concise summary of the intended approach:
- Use an inorder traversal to collect node values in sorted order.
- Rebuild a balanced BST from the sorted values by recursively choosing the middle element as the root of each subtree.

## Refining the problem, round 2 thoughts
- Inorder traversal of a BST yields sorted values, so converting the tree to a sorted array then building a balanced BST is straightforward and guarantees the same values.
- Edge cases: single-node tree, already balanced tree, and highly skewed input BST.
- Implementation detail: use an iterative inorder traversal to avoid Python recursion depth limits on skewed trees (n up to 10^4). The reconstruction step uses recursion but its depth is O(log n) for the balanced output, which is safe.
- Time complexity: O(n) to traverse + O(n) to rebuild = O(n). Space complexity: O(n) extra for the array of values (plus recursion stack O(log n) for rebuild).

## Attempted solution(s)
```python
# Definition for a binary tree node.
from typing import Optional, List

class TreeNode:
    def __init__(self, val: int = 0, left: 'Optional[TreeNode]' = None, right: 'Optional[TreeNode]' = None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def balanceBST(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        # Iterative inorder traversal to collect sorted values (avoid recursion depth issues)
        vals: List[int] = []
        stack: List[TreeNode] = []
        node = root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            vals.append(node.val)
            node = node.right

        # Build balanced BST from sorted values
        def build(l: int, r: int) -> Optional[TreeNode]:
            if l > r:
                return None
            mid = (l + r) // 2
            root = TreeNode(vals[mid])
            root.left = build(l, mid - 1)
            root.right = build(mid + 1, r)
            return root

        return build(0, len(vals) - 1)
```
- Notes:
  - Approach: inorder -> sorted list -> build balanced BST by choosing middle element as root recursively.
  - Time complexity: O(n), where n is number of nodes (O(n) to traverse and O(n) to rebuild).
  - Space complexity: O(n) extra for the list of values. The recursion stack during rebuild is O(log n) (balanced).
  - Implementation detail: iterative inorder avoids recursion depth issues on skewed input trees.