# [Problem 1530: Number of Good Leaf Nodes Pairs](https://leetcode.com/problems/number-of-good-leaf-nodes-pairs/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can't share my internal stream-of-consciousness, but here is a concise summary of the approach I will use:

- Perform a post-order DFS.
- For each node, compute a small array counts where counts[d] = number of leaf nodes in that node's subtree at distance d from the node.
- When processing a node, combine the left and right counts to count all pairs formed by one leaf in the left subtree and one leaf in the right subtree whose distances sum to <= distance.
- Shift the counts by +1 when returning to the parent (because distances increase by 1) and truncate to the given distance.

This produces an efficient solution since the maximum distance is small (<= 10).

## Refining the problem, round 2 thoughts
Refinements and important considerations:
- Base case: a null node returns an array of zeros. A leaf node should report counts[1] = 1 (distance 1 from the parent).
- When combining left and right child counts, only consider pairs (i, j) with i + j <= distance. Multiply counts from left and right for those distances to add to the global answer.
- When returning the counts up the recursion, increment distance indices by 1 and drop anything exceeding distance.
- Complexity: distance ≤ 10, so nested loops over distances are cheap. Time complexity O(n * distance^2) in the worst case, but practically fine because distance <= 10. Space complexity O(h * distance) for recursion and temporary arrays (h is tree height).
- Edge cases: single-node tree (no pairs), skewed trees, nodes with only one child — algorithm handles these naturally.

## Attempted solution(s)
```python
# Definition for a binary tree node.
# Provided here to be self-contained; LeetCode already defines this.
from typing import Optional, List

class TreeNode:
    def __init__(self, val: int = 0, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def countPairs(self, root: Optional[TreeNode], distance: int) -> int:
        # result holder
        self.ans = 0
        # dfs returns a list counts where counts[d] = number of leaves at distance d from node
        # list indices from 0..distance (we'll use 1..distance)
        def dfs(node: Optional[TreeNode]) -> List[int]:
            if not node:
                return [0] * (distance + 1)
            # leaf node
            if not node.left and not node.right:
                counts = [0] * (distance + 1)
                if distance >= 1:
                    counts[1] = 1
                return counts
            left_counts = dfs(node.left)
            right_counts = dfs(node.right)
            # count good pairs between left and right
            for i in range(1, distance + 1):
                if left_counts[i] == 0:
                    continue
                # only consider j such that i + j <= distance
                maxj = distance - i
                if maxj <= 0:
                    continue
                # sum over j
                for j in range(1, maxj + 1):
                    if right_counts[j]:
                        self.ans += left_counts[i] * right_counts[j]
            # prepare counts to return to parent (increment distance by 1)
            curr = [0] * (distance + 1)
            for d in range(1, distance):
                # leaves at distance d from child become distance d+1 from current node
                curr[d + 1] = left_counts[d] + right_counts[d]
            return curr

        dfs(root)
        return self.ans
```
- Notes about the solution:
  - Approach: Post-order traversal. Each node returns a small array counts indexed by distance from that node to leaves. Combining left and right counts lets us count cross-subtree leaf pairs whose path goes through the node.
  - Correctness: Any pair of leaves whose shortest path passes through some node will be counted exactly once at that node when combining its left and right children. Pairs inside a single subtree are counted lower in the recursion.
  - Time complexity: O(n * distance^2) due to combining counts with nested loops over distances; since distance ≤ 10 this is effectively linear in n with a small constant.
  - Space complexity: O(h * distance) where h is tree height (recursion stack and arrays per recursion frame), or more simply O(distance * n) in the worst representation if you consider all frames, but practically proportional to height * distance.