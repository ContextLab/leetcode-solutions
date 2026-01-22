# [Problem 2290: Minimum Obstacle Removal to Reach Corner](https://leetcode.com/problems/minimum-obstacle-removal-to-reach-corner/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This is a shortest-path problem on a grid, but edge "costs" depend on whether the destination cell is an obstacle (cost 1 to remove) or empty (cost 0). The first idea is Dijkstra treating each move into a cell with weight equal to grid[cell] (0 or 1). Since weights are only 0 or 1, a 0-1 BFS (deque-based) is more efficient and simpler than a full priority queue — push 0-cost moves to the front and 1-cost moves to the back. The start and end are guaranteed empty, so initial cost is 0.

## Refining the problem, round 2 thoughts
- Use 0-1 BFS to get O(m * n) time since each cell is processed at most a few times and operations are O(1).
- Keep a dist array initialized to infinity; update when we find a smaller cost.
- Early exit when we pop the target cell from the deque (its distance is finalized).
- Edge cases: tiny grids (2 cells, narrow rectangles) are naturally handled; constraints guarantee grid[0][0] and grid[m-1][n-1] are 0. Memory is O(m * n) which is fine given m*n <= 1e5.
- Alternative: Dijkstra with priority queue (O(E log V)), but 0-1 BFS reduces overhead and is optimal for binary weights.

## Attempted solution(s)
```python
from collections import deque
from typing import List

class Solution:
    def minimumObstacles(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        INF = float('inf')
        dist = [[INF] * n for _ in range(m)]
        dq = deque()
        dist[0][0] = 0
        dq.append((0, 0))
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        
        while dq:
            x, y = dq.popleft()
            # Early exit if we've reached target
            if x == m-1 and y == n-1:
                return dist[x][y]
            cur = dist[x][y]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n:
                    cost = cur + grid[nx][ny]
                    if cost < dist[nx][ny]:
                        dist[nx][ny] = cost
                        # If moving into empty cell (0), prioritize by appending to left
                        if grid[nx][ny] == 0:
                            dq.appendleft((nx, ny))
                        else:
                            dq.append((nx, ny))
        return dist[m-1][n-1]
```
- Notes:
  - Approach: 0-1 BFS where moving into a cell incurs cost grid[nx][ny] (0 or 1). We update distances and push neighbors with 0-cost to the front of the deque and 1-cost to the back.
  - Time complexity: O(m * n). Each cell is relaxed a small constant number of times; deque operations are O(1).
  - Space complexity: O(m * n) for the distance array and deque in the worst case.
  - Implementation detail: early return when target is popped (its distance is final), which can save work in many cases.