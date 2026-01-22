# [Problem 2503: Maximum Number of Points From Grid Queries](https://leetcode.com/problems/maximum-number-of-points-from-grid-queries/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need for each query q the maximum number of distinct cells we can get points from starting at (0,0) when we can only move through cells with value strictly less than q. That is essentially "how many cells reachable from (0,0) have value < q". Doing a fresh BFS/DFS per query would be too slow (k up to 1e4 and cells up to 1e5). Queries are independent but monotonic: increasing q only allows more cells. So sort queries and process them in increasing order, expanding a region only when q increases. We can either use union-find and activate cells in order of their value, or maintain a min-heap frontier (by cell value) and pop cells with value < current q, adding their neighbors to the heap. The heap approach is straightforward: push (grid[0][0]) initially; for each query pop while heap.top.value < q, count popped cells and push unseen neighbors. Keep track of seen so we don't push duplicates. Record count for each query (in original order).

## Refining the problem, round 2 thoughts
- Sort queries with indices to answer in original order.
- Use a min-heap keyed by cell value. Initially push the top-left (0,0) cell and mark it "in-heap" (seen).
- For each sorted query q:
  - While heap not empty and heap[0].value < q: pop -> this cell becomes visited (count++), push its neighbors that are not yet seen (mark seen when pushing to avoid duplicates).
  - After that loop, the current count is exactly the number of reachable cells with value < q.
- Edge cases:
  - If grid[0][0] >= q for a query, count remains 0 (heap top won't be popped).
  - We must mark "seen" on push so we don't push duplicates; don't mark as visited until popped and counted.
- Complexity:
  - Each cell is pushed at most once and popped at most once: O(N log N) where N = m*n.
  - Sorting queries O(k log k). Total O((N + k) log N) time, O(N) extra space.

## Attempted solution(s)
```python
import heapq
from typing import List, Tuple

class Solution:
    def maxPoints(self, grid: List[List[int]], queries: List[int]) -> List[int]:
        m = len(grid)
        n = len(grid[0])
        k = len(queries)

        # Pair queries with original indices and sort by value
        sorted_q: List[Tuple[int,int]] = sorted((q, i) for i, q in enumerate(queries))
        ans = [0] * k

        # Min-heap of (value, i, j). We'll push neighbors when we expand.
        heap: List[Tuple[int,int,int]] = []
        seen = [[False] * n for _ in range(m)]  # seen means "pushed to heap (or processed)"
        # Start from top-left: push it (even if its value >= first query; we will pop only when allowed)
        heapq.heappush(heap, (grid[0][0], 0, 0))
        seen[0][0] = True

        count = 0  # number of visited (popped and counted) cells so far
        dirs = [(1,0), (-1,0), (0,1), (0,-1)]

        for q_val, q_idx in sorted_q:
            # Expand while smallest available cell value < q_val
            while heap and heap[0][0] < q_val:
                val, i, j = heapq.heappop(heap)
                # This popped cell is strictly less than q_val, so we can visit it (count it)
                count += 1
                # Push neighbors that are not yet seen
                for di, dj in dirs:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < m and 0 <= nj < n and not seen[ni][nj]:
                        seen[ni][nj] = True
                        heapq.heappush(heap, (grid[ni][nj], ni, nj))
            ans[q_idx] = count

        return ans
```
- Approach: sort queries and process in increasing order; maintain a min-heap frontier from the starting cell, pop cells with value < current query and push unseen neighbors. Each cell is pushed and popped at most once.
- Time complexity: O((m*n) log (m*n) + k log k) ≈ O(N log N + k log k), where N = m*n.
- Space complexity: O(N) for heap and seen array.