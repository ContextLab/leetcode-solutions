# [Problem 1368: Minimum Cost to Make at Least One Valid Path in a Grid](https://leetcode.com/problems/minimum-cost-to-make-at-least-one-valid-path-in-a-grid/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the minimum number of sign changes (costs) to get from (0,0) to (m-1,n-1). Each cell points in one of four directions. If I follow the arrow in a cell to move to the intended neighbor, that move costs 0 (no change). If I move to any other neighbor, that's equivalent to changing the sign on the current cell (cost 1). This sounds like a shortest-path problem on a grid where edges have weight 0 or 1. 0-1 BFS (deque) is a natural fit: push zero-cost moves to the front and one-cost to the back. Alternatively Dijkstra works but is heavier. Edge cases: 1x1 grid -> cost 0.

## Refining the problem, round 2 thoughts
Represent four directions in the order corresponding to values 1..4: right, left, down, up. For each cell, iterate all 4 neighbors; if the neighbor direction matches grid[i][j], cost addition is 0, else 1. Use dist array initialized to inf, and 0-1 BFS from (0,0). Stop when we reach (m-1,n-1) or exhaust queue. Complexity should be O(V + E) ~ O(m*n). Memory O(m*n). Make sure to check bounds. Also note some arrows might point outside grid — that's fine; we still consider moving to valid neighbors but following an arrow that points outside simply won't produce a valid 0-cost neighbor.

## Attempted solution(s)
```python
from collections import deque

class Solution:
    def minCost(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        m = len(grid)
        n = len(grid[0])
        # Directions mapped to 1..4: right, left, down, up
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        # dist array
        INF = 10**9
        dist = [[INF] * n for _ in range(m)]
        dist[0][0] = 0
        dq = deque()
        dq.append((0, 0))
        
        while dq:
            i, j = dq.popleft()
            # If we reached target, we can continue until deque empties or optionally early return
            if i == m - 1 and j == n - 1:
                # We can return early because 0-1 BFS processes in nondecreasing cost order
                return dist[i][j]
            
            for k, (di, dj) in enumerate(dirs, start=1):
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n:
                    # cost 0 if the direction matches the arrow in (i,j), else 1
                    add = 0 if k == grid[i][j] else 1
                    new_cost = dist[i][j] + add
                    if new_cost < dist[ni][nj]:
                        dist[ni][nj] = new_cost
                        if add == 0:
                            dq.appendleft((ni, nj))
                        else:
                            dq.append((ni, nj))
        return dist[m-1][n-1]
```
- Notes:
  - Approach: 0-1 BFS on the grid treating following the arrow as an edge of weight 0 and any other neighbor move as weight 1 (change sign). Use deque: appendleft for 0-cost moves and append for 1-cost.
  - Correctness: 0-1 BFS yields shortest path distances for graphs with edge weights 0 or 1. We can early-return when we pop the target because nodes are processed in nondecreasing distance order.
  - Time complexity: O(V + E) where V = m*n and E ~ 4*m*n, so O(m*n).
  - Space complexity: O(m*n) for dist and queue in the worst case.
  - Implementation details: map directions to indices 1..4 to directly compare with grid values; check bounds before updating.