# [Problem 1022: Sum of Root To Leaf Binary Numbers](https://leetcode.com/problems/sum-of-root-to-leaf-binary-numbers/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I'm thinking this is a straightforward tree traversal. Each root-to-leaf path forms a binary number with the root as the most significant bit. I can accumulate the binary value as I traverse down the tree instead of building strings and converting — keep a running integer and at each node do val = val * 2 + node.val (or val << 1 | node.val). When I hit a leaf, add that accumulated value to the total. Depth-first traversal (recursive or iterative) fits naturally. Edge cases: single node (0 or 1) and tree with only left or right branches. Complexity should be linear in number of nodes.

## Refining the problem, round 2 thoughts
Recursion is simplest and clean: pass current accumulated value down the recursion. Alternatively, an explicit stack can do iterative DFS. Make sure to stop at None nodes and detect leaves (node.left is None and node.right is None). Using bit-shift is slightly faster and cleaner than multiplication. Time complexity is O(n) because we visit each node once. Space complexity is O(h) for recursion stack where h is tree height (worst-case O(n) for skewed tree). Also ensure integers fit into 32 bits — problem guarantees that the result fits in 32-bit signed int.

## Attempted solution(s)
```python
from typing import Optional

# Definition for a binary tree node (provided here for completeness).
class TreeNode:
    def __init__(self, val: int = 0, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def sumRootToLeaf(self, root: Optional[TreeNode]) -> int:
        def dfs(node: Optional[TreeNode], curr: int) -> int:
            if not node:
                return 0
            # shift left and add current node's bit
            curr = (curr << 1) | node.val
            # if leaf, return the accumulated value
            if not node.left and not node.right:
                return curr
            # otherwise sum contributions from children
            return dfs(node.left, curr) + dfs(node.right, curr)

        return dfs(root, 0)
```
- Approach: Depth-first traversal with an integer accumulator representing the binary number so far; use bit-shift (curr << 1) | node.val to append the current bit. When a leaf is reached, return the accumulated value and sum these across leaves.
- Time complexity: O(n), where n is the number of nodes (each node visited once).
- Space complexity: O(h) recursion stack, where h is the height of the tree (worst-case O(n) for a skewed tree, best-case O(log n) for balanced tree).
- Implementation details: Uses recursion for clarity; can be converted to iterative DFS with a stack if recursion depth is a concern.