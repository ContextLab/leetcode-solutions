# [Problem 1261: Find Elements in a Contaminated Binary Tree](https://leetcode.com/problems/find-elements-in-a-contaminated-binary-tree/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We are given a binary tree where every node value has been set to -1. The original (recovered) tree follows a deterministic rule: root = 0, left child = 2*x+1, right child = 2*x+2. We need to (1) recover the tree and (2) implement find(target) to check whether a value exists.

First thought: we can traverse the contaminated tree starting from the root, assign the correct values using the rules, and record all values we encounter in a set. Then find(target) is just a set membership test (O(1)). This seems straightforward and efficient.

An alternative approach (not necessary here) is: given a target, reconstruct the path from the root using the binary representation / reverse the parent relation (target -> parent = (target-1)//2 or (target-2)//2 depending on parity) and verify nodes exist by walking down the tree. That would avoid storing all values but complicates checks and likely be slower for repeated queries. Given constraints (up to 10^4 nodes and 10^4 find calls), storing values is fine.

Edge cases: root could be None (though problem states at least 1 node). Values can go up to around 2^20 so fit within constraints.

## Refining the problem, round 2 thoughts
Decide to perform a single DFS or BFS to recover values and populate a set. Use iterative stack/queue to avoid recursion depth issues (height <= 20 so recursion is safe, but iterative is simple). Complexity: building set is O(n) time, O(n) space. Each find is O(1). This is optimal for repeated queries.

We should ensure we set node.val for children before pushing them to stack/queue, otherwise we cannot compute their children. Also handle None root gracefully.

## Attempted solution(s)
```python
# Definition for a binary tree node is provided by LeetCode:
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

from typing import Optional

class FindElements:
    def __init__(self, root: Optional['TreeNode']):
        """
        Recover the contaminated tree and store all node values in a set for O(1) find queries.
        """
        self.seen = set()
        if root is None:
            return
        # Recover using iterative DFS
        root.val = 0
        stack = [root]
        while stack:
            node = stack.pop()
            self.seen.add(node.val)
            if node.right:
                node.right.val = 2 * node.val + 2
                stack.append(node.right)
            if node.left:
                node.left.val = 2 * node.val + 1
                stack.append(node.left)

    def find(self, target: int) -> bool:
        return target in self.seen
```
- Notes:
  - Approach: one traversal to recover values and store them in a hash set.
  - Time complexity: O(n) to build (n = number of nodes), and O(1) per find query.
  - Space complexity: O(n) extra for the set (plus implicit stack usage which is O(h), h ≤ 20).
  - Implementation detail: iterative DFS avoids recursion depth concerns; we set child values before pushing them so their children can be computed consistently.