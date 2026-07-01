# [Problem 2812: Find the Safest Path in a Grid](https://leetcode.com/problems/find-the-safest-path-in-a-grid/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the maximum safeness factor along a path from (0,0) to (n-1,n-1). Safeness of a path = minimum Manhattan distance from any cell on the path to any thief. So for each cell we can precompute its distance to the nearest thief (multi-source BFS from all thief cells). Then the path problem becomes: find a path that maximizes the minimum of those precomputed distances along the path. That is a classic "maximize the minimum" path which can be solved either by:
- Binary search on safeness S and check reachability through cells whose distance >= S (BFS each check), or
- A "maximum capacity path" variant using a max-heap / Dijkstra-like greedy: always expand the path with the currently largest minimum safeness and update neighbors' best known minimum safeness.

Multi-source BFS to get distances is O(n^2). Then using the max-heap approach will be O(n^2 log n^2) which is acceptable for n <= 400.

## Refining the problem, round 2 thoughts
Edge cases:
- Start or destination might be thieves (distance 0) → result 0.
- There is guaranteed at least one thief.
Alternatives: Binary search on S would do O(log n * n^2) which also works. The max-heap approach is simpler to implement and avoids repeated BFS runs.
Complexities:
- Compute thief distances: O(n^2) time and O(n^2) space.
- Max-heap path: Each cell can be pushed a few times, worst-case O(n^2 log n^2).
Memory O(n^2) for distance and best arrays.
I'll implement multi-source BFS then a max-heap greedy to get the maximum safeness.

## Attempted solution(s)
```python
from collections import deque
import heapq
from typing import List

class Solution:
    def maximumSafenessFactor(self, grid: List[List[int]]) -> int:
        n = len(grid)
        # Step 1: multi-source BFS from all thieves to compute distance to nearest thief
        dist = [[-1] * n for _ in range(n)]
        q = deque()
        for r in range(n):
            for c in range(n):
                if grid[r][c] == 1:
                    dist[r][c] = 0
                    q.append((r, c))
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        while q:
            r, c = q.popleft()
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    q.append((nr, nc))

        # Step 2: Use a max-heap to find the path that maximizes the minimum dist along it.
        # best[r][c] = best known safeness (minimum dist along the path) to reach (r,c)
        best = [[-1] * n for _ in range(n)]
        start_val = dist[0][0]
        best[0][0] = start_val
        # Python heapq is min-heap; use negative to simulate max-heap
        heap = [(-start_val, 0, 0)]

        while heap:
            neg_cur, r, c = heapq.heappop(heap)
            cur = -neg_cur
            # If this popped value is stale (worse than recorded), skip
            if cur != best[r][c]:
                continue
            # If reached destination, this is the maximum safeness factor
            if r == n - 1 and c == n - 1:
                return cur
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n:
                    new_safeness = min(cur, dist[nr][nc])
                    if new_safeness > best[nr][nc]:
                        best[nr][nc] = new_safeness
                        heapq.heappush(heap, (-new_safeness, nr, nc))

        # If unreachable (shouldn't happen given grid connectivity), return 0
        return 0
```
- Notes on approach:
  - First compute for each cell its Manhattan distance to the nearest thief via multi-source BFS from all thief cells (dist matrix).
  - Then find a path maximizing the minimum dist along it using a max-heap (greedy Dijkstra-like). Each state stores the best safeness achievable to that cell; pop the currently largest safeness, expand neighbors with new safeness = min(current, dist[neighbor]).
  - When destination is popped, its value is the optimal safeness.

- Complexity:
  - Time: O(n^2) for multi-source BFS + O(n^2 log(n^2)) = O(n^2 log n) for the heap-based path search.
  - Space: O(n^2) for dist and best arrays and the queue/heap.