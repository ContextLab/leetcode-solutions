# [Problem 2583: Kth Largest Sum in a Binary Tree](https://leetcode.com/problems/kth-largest-sum-in-a-binary-tree/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the sums at each level, so a level-order traversal (BFS) is the natural first thought — accumulate node values per level. Once I have all level sums I need the k-th largest among them (not distinct). Simple approach: gather sums into a list and sort descending and pick the (k-1)-th index. That is straightforward and correct. For large trees, number of levels L can be up to n (skewed tree), but sorting L values (L ≤ 1e5) is fine in practice — O(L log L). Alternatively, I can keep a min-heap of size k while scanning level sums to get O(L log k) time and O(k) extra space, which is better when k is much smaller than L.

## Refining the problem, round 2 thoughts
Refinements and edge cases:
- If the tree has fewer than k levels, we must return -1.
- Node values are positive (>=1), so comparison logic is straightforward.
- BFS memory is O(width) and total nodes processed O(n).
- Two implementation choices:
  - Collect all level sums, sort descending, return sums[k-1] if exists.
  - Maintain a min-heap of size k while producing level sums (more efficient when k << L).
I'll implement the min-heap approach (keeping the k largest sums) for better worst-case efficiency. Complexity:
- Time: O(n) to traverse + O(L log k) for heap operations (L = number of levels, L ≤ n) → overall O(n + L log k).
- Space: O(max(width, k)), where width is BFS maximum width.

## Attempted solution(s)
```python
from collections import deque
import heapq
from typing import Optional

# Definition for a binary tree node (LeetCode standard).
class TreeNode:
    def __init__(self, val: int = 0, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def kthLargestLevelSum(self, root: Optional[TreeNode], k: int) -> int:
        if not root:
            return -1

        # BFS to compute level sums
        q = deque([root])
        # min-heap to keep k largest level sums
        min_heap = []

        while q:
            level_size = len(q)
            level_sum = 0
            for _ in range(level_size):
                node = q.popleft()
                level_sum += node.val
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)

            # maintain a min-heap of at most k largest sums
            if len(min_heap) < k:
                heapq.heappush(min_heap, level_sum)
            else:
                # if current sum larger than smallest in heap, replace it
                if level_sum > min_heap[0]:
                    heapq.heapreplace(min_heap, level_sum)

        # If fewer than k levels, return -1
        if len(min_heap) < k:
            return -1
        # The root of min-heap is the k-th largest
        return min_heap[0]
```
- Approach: BFS to compute sum per level, maintain a min-heap of size k to track the k largest sums seen so far. After traversal, if we have fewer than k level sums return -1; otherwise heap[0] is the k-th largest.
- Time complexity: O(n + L log k) where n is number of nodes and L is number of levels (L ≤ n). In practice O(n) dominates for traversal.
- Space complexity: O(max(width, k)) where width is maximum number of nodes stored in the BFS queue (tree width) and k for the heap.