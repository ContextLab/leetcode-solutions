# [Problem 1110: Delete Nodes And Return Forest](https://leetcode.com/problems/delete-nodes-and-return-forest/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I recall this problem: we need to remove some nodes from a binary tree and return the forest of remaining trees. A natural approach is to traverse the tree and, whenever a node is deleted, its non-null children become new roots in the resulting forest. A post-order traversal (process children first) makes sense because whether a node should remain can depend on its children being pruned first. If a node is deleted, its parent must sever the pointer to it — returning None from the recursion is convenient to do that. Use a set for to_delete lookups.

## Refining the problem, round 2 thoughts
- Use a DFS (post-order): recurse left and right, update left/right pointers with returned values. If current node is in to_delete set:
  - if left child returned non-None, add left to answer list
  - same for right child
  - return None to parent (parent will drop this node)
- If current node is not deleted, return it (with possibly modified children).
- After full traversal, if the root itself is not deleted, add it to the results.
Edge cases:
- root is None -> return []
- to_delete empty -> return [root]
- all nodes deleted -> return list of children that were attached as roots (possibly empty)
Complexity:
- Time: O(n) visiting each node once.
- Space: O(n) for result + recursion stack O(h) (h <= n). Using a set for fast deletion lookups.

## Attempted solution(s)
```python
# Definition for a binary tree node.
from typing import Optional, List

class TreeNode:
    def __init__(self, val: int = 0, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def delNodes(self, root: Optional[TreeNode], to_delete: List[int]) -> List[TreeNode]:
        to_delete_set = set(to_delete)
        ans: List[TreeNode] = []
        
        def dfs(node: Optional[TreeNode]) -> Optional[TreeNode]:
            if not node:
                return None
            # post-order: process children first
            node.left = dfs(node.left)
            node.right = dfs(node.right)
            if node.val in to_delete_set:
                # If deleted, add non-null children as new roots
                if node.left:
                    ans.append(node.left)
                if node.right:
                    ans.append(node.right)
                return None  # parent will drop this node
            return node
        
        root_after = dfs(root)
        if root_after:  # if root wasn't deleted, it's a root of one tree in the forest
            ans.append(root_after)
        return ans
```
- Notes:
  - Approach: post-order DFS returning None for deleted nodes so parent pointers automatically get severed.
  - We use a set for O(1) lookup of nodes to delete.
  - Time complexity: O(n), where n is number of nodes (each node visited once).
  - Space complexity: O(n) in worst case (output list + recursion stack up to O(n) for skewed tree). Additional O(k) for the to_delete set where k = len(to_delete).