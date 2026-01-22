# [Problem 1339: Maximum Product of Splitted Binary Tree](https://leetcode.com/problems/maximum-product-of-splitted-binary-tree/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to cut one edge so the tree becomes two subtrees; maximize product of their sums. A natural approach is to compute the sum of every possible subtree: if we remove the edge above a node, one subtree sum is that node's subtree sum S and the other is totalSum - S. So for each node we can consider S * (totalSum - S) and take the maximum.

To get subtree sums we can do a post-order traversal. We must maximize the product before taking modulo 1e9+7 (only apply modulo to final answer). Constraints up to 5e4 nodes — O(n) or O(n log n) is fine. Node values are positive, so splitting near half of total sum likely gives the max.

One implementation detail: collect all subtree sums in a list during a traversal, then compute the max product by iterating that list. Watch recursion depth for skewed trees; set recursionlimit if necessary.

## Refining the problem, round 2 thoughts
- Two passes: (1) compute subtree sums (post-order) collecting sums and total, (2) evaluate max product from collected sums. This is O(n) time and O(n) extra space (for sums list).
- Alternatively could compute total first then on a second traversal compute product on the fly; both are fine.
- Edge cases: total is positive (since node values >= 1) so no worry about negative products. The product for the root's subtree sum equals total * 0 = 0, so it won’t be maximal.
- Must compute the product with full integers (no intermediate modulo), and only mod the final result by 1e9+7.
- Recursive DFS is straightforward; for extreme depth you may need to increase recursion limit in Python.

## Attempted solution(s)
```python
# Definition for a binary tree node (LeetCode provided).
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

from typing import Optional
import sys
sys.setrecursionlimit(10**6)

class Solution:
    def maxProduct(self, root: Optional['TreeNode']) -> int:
        MOD = 10**9 + 7
        subtree_sums = []
        
        # Post-order DFS that returns subtree sum and records it
        def dfs(node: Optional['TreeNode']) -> int:
            if not node:
                return 0
            left_sum = dfs(node.left)
            right_sum = dfs(node.right)
            s = node.val + left_sum + right_sum
            subtree_sums.append(s)
            return s
        
        total = dfs(root)
        
        max_product = 0
        for s in subtree_sums:
            # If we cut above the subtree with sum s, other part has sum (total - s)
            product = s * (total - s)
            if product > max_product:
                max_product = product
        
        return max_product % MOD
```
- Solution approach: perform a post-order traversal to collect every subtree sum, compute the total sum, then evaluate the product s * (total - s) for each recorded subtree sum and take the maximum. Return that maximum modulo 1e9+7.
- Time complexity: O(n) — each node visited once.
- Space complexity: O(n) extra for the list of subtree sums plus recursion call stack (O(n) worst-case).