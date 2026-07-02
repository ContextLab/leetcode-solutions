# [Problem 3286: Find a Safe Walk Through a Grid](https://leetcode.com/problems/find-a-safe-walk-through-a-grid/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to know whether there exists a path from (0,0) to (m-1,n-1) such that the number of unsafe cells (grid value 1) visited never reduces health to 0. Since each unsafe cell reduces health by 1 and the health must remain positive, after finishing we must have visited at most health-1 unsafe cells. So the problem reduces to: is there a path whose sum of cell weights (weight = grid[i][j]) is <= health-1? This is a shortest-path problem on a grid with edge costs 0 or 1 (cost is the destination cell's grid value). 0-1 BFS (or Dijkstra) computes the minimum number of unsafe cells along any path efficiently.

## Refining the problem, round 2 thoughts
- Include the starting cell's value in the cost (if grid[0][0] == 1 you immediately lose 1 health).
- We want the minimum number of 1s encountered along any path; if that minimum <= health-1, return True.
- Use 0-1 BFS (deque) because moves into a 0-cost cell are pushed to the front and moves into 1-cost cells pushed to the back. This runs in O(m*n).
- Edge cases: start or end being 1 is handled naturally by counting them. If the minimal required unsafe count is INF/unreachable or > health-1, return False.
- Space: we keep a distance matrix of size m*n.

## Attempted solution(s)
```python
from collections import deque
from typing import List

class Solution:
    def findSafeWalk(self, grid: List[List[int]], health: int) -> bool:
        m, n = len(grid), len(grid[0])
        INF = 10**9
        # dist[r][c] = minimum number of unsafe cells (1's) encountered to reach (r,c), including that cell
        dist = [[INF] * n for _ in range(m)]
        start_cost = grid[0][0]
        dist[0][0] = start_cost

        # Early rejection: if start already makes health zero or negative
        if start_cost > health - 1:
            return False

        dq = deque()
        dq.append((0, 0))
        directions = [(1,0),(-1,0),(0,1),(0,-1)]

        while dq:
            r, c = dq.popleft()
            curr = dist[r][c]

            # If cost already exceeds allowed (health-1), no need to expand this node
            if curr > health - 1:
                continue

            # Early success if we reached target with acceptable cost
            if r == m - 1 and c == n - 1:
                return True

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    new_cost = curr + grid[nr][nc]
                    if new_cost < dist[nr][nc]:
                        dist[nr][nc] = new_cost
                        # 0-1 BFS: move to front if cost 0, back if cost 1
                        if grid[nr][nc] == 0:
                            dq.appendleft((nr, nc))
                        else:
                            dq.append((nr, nc))

        return dist[m-1][n-1] <= health - 1
```
- Notes:
  - Approach: Model each cell's weight as grid[i][j] (0 or 1), compute minimum sum of weights along any path including the start cell. Use 0-1 BFS to get the minimum number of unsafe cells encountered.
  - Time complexity: O(m * n) — each cell is processed a constant number of times in 0-1 BFS.
  - Space complexity: O(m * n) for the distance matrix + O(m * n) worst-case deque space.
  - Implementation detail: We check the start cell cost early and also skip expanding states whose current unsafe count already exceeds health-1 to prune unnecessary work.