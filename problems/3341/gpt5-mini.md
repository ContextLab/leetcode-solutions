# [Problem 3341: Find Minimum Time to Reach Last Room I](https://leetcode.com/problems/find-minimum-time-to-reach-last-room-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the minimum time to get from (0,0) to (n-1,m-1). Moving between adjacent cells takes exactly 1 second. Each cell has a moveTime value describing when the room becomes available to move into. This looks like a shortest-path problem on a grid where edge "weight" depends on the current time (you can wait in a room). Dijkstra (with a min-heap) is a natural fit: treat nodes as cells and the cost to reach a neighbor depends on current time and the neighbor's opening time. I should clarify whether moveTime is inclusive or exclusive (can arrival equal moveTime?). From examples, e.g. moveTime=4 means earliest arrival is 5, so the cell becomes enterable strictly after moveTime seconds — i.e., earliest allowed arrival time is moveTime + 1. So when at time t in current cell, the earliest arrival to neighbor is max(t + 1, moveTime[neighbor] + 1).

## Refining the problem, round 2 thoughts
- We'll run Dijkstra on the grid (n*m nodes), using dist array initialized to +inf except dist[0][0] = 0.
- For a popped cell with current time cur_t, for each neighbor compute candidate = max(cur_t + 1, moveTime[ni][nj] + 1).
- If candidate < dist[ni][nj], update and push to heap.
- Return dist[n-1][m-1].
- Complexity: O(n*m log(n*m)) since each node processed and each edge considered a constant number of times.
- Edge cases: starting cell's moveTime is irrelevant because we start there at t=0. n,m up to 50 so Dijkstra is fine.

## Attempted solution(s)
```python
import heapq
from typing import List

class Solution:
    def minimumTime(self, moveTime: List[List[int]]) -> int:
        n = len(moveTime)
        m = len(moveTime[0])
        INF = 10**30
        dist = [[INF]*m for _ in range(n)]
        dist[0][0] = 0
        heap = [(0, 0, 0)]  # (time, r, c)
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        
        while heap:
            t, r, c = heapq.heappop(heap)
            if t != dist[r][c]:
                continue
            if r == n-1 and c == m-1:
                return t
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < m:
                    # The room opens strictly after moveTime[nr][nc] seconds,
                    # so earliest allowed arrival is moveTime[nr][nc] + 1.
                    candidate = max(t + 1, moveTime[nr][nc] + 1)
                    if candidate < dist[nr][nc]:
                        dist[nr][nc] = candidate
                        heapq.heappush(heap, (candidate, nr, nc))
        # If loop finishes, return final dist (should normally be found)
        return dist[n-1][m-1]
```
- Notes:
  - We interpret moveTime[i][j] as the time after which the room is enterable, i.e., earliest arrival time is moveTime[i][j] + 1 (example alignment).
  - Dijkstra-like approach: states are (cell, time), edges cost depends on current time but can be computed deterministically as candidate = max(cur_t+1, moveTime[next]+1).
  - Time complexity: O(n*m log(n*m)) due to heap operations.
  - Space complexity: O(n*m) for distance array and heap.