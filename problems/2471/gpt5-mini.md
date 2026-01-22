# [Problem 2471: Minimum Number of Operations to Sort a Binary Tree by Level](https://leetcode.com/problems/minimum-number-of-operations-to-sort-a-binary-tree-by-level/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
[We need to make each tree level strictly increasing by swapping values between nodes on the same level. Swapping nodes on the same level is equivalent to permuting the list of values of that level. For each level, we want the minimum number of swaps to sort that list. That is a classic "minimum swaps to sort an array" problem which is solved by counting cycles in the permutation that maps current indices to sorted indices. So run a BFS to collect values level-by-level, and for each level compute the min swaps via cycle detection. Sum across levels. Values are unique which simplifies mapping.]

## Refining the problem, round 2 thoughts
[Refinement: BFS (queue) to gather each level's values. For a level array arr, create sorted version and a mapping value -> sorted index. Then treat current index -> target index and count cycles: for a cycle of length k, we need k-1 swaps. Edge cases: levels of length 0 or 1 need 0 swaps. Complexity: each level sorts its values; across the tree sorting costs sum m_i log m_i <= n log n. BFS is O(n). Memory: queue + arrays O(n). Unique values guarantee mapping correctness. Implement carefully to avoid infinite loops when following permutation cycles.]

## Attempted solution(s)
```python
from collections import deque
from typing import Optional

# Definition for a binary tree node (LeetCode style).
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def minimumOperations(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        def min_swaps_to_sort(arr):
            n = len(arr)
            if n <= 1:
                return 0
            # map value -> index in sorted array
            sorted_arr = sorted(arr)
            value_to_index = {v: i for i, v in enumerate(sorted_arr)}
            visited = [False] * n
            swaps = 0
            for i in range(n):
                if visited[i]:
                    continue
                j = i
                cycle_size = 0
                # follow the cycle
                while not visited[j]:
                    visited[j] = True
                    # where should arr[j] go in sorted order?
                    j = value_to_index[arr[j]]
                    cycle_size += 1
                if cycle_size > 1:
                    swaps += cycle_size - 1
            return swaps

        total_ops = 0
        q = deque([root])
        while q:
            level_size = len(q)
            level_vals = []
            for _ in range(level_size):
                node = q.popleft()
                level_vals.append(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            total_ops += min_swaps_to_sort(level_vals)

        return total_ops
```
- Notes about the solution:
  - Approach: BFS to process nodes level-by-level, for each level compute the minimum number of swaps needed to sort the values using cycle decomposition of the permutation from current indices to sorted indices.
  - Time complexity: O(n log n) in total (collecting levels O(n), sorting values per level sums to at most O(n log n) across levels). Cycle counting and BFS are O(n).
  - Space complexity: O(n) for the queue and temporary arrays used for levels and visited bookkeeping.
  - Important details: Values are unique so mapping value -> sorted index is unambiguous. For each cycle of length k, exactly k-1 swaps are needed, which we sum.