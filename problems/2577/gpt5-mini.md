# [Problem 2577: Minimum Time to Visit a Cell In a Grid](https://leetcode.com/problems/minimum-time-to-visit-a-cell-in-a-grid/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The grid gives the earliest time you are allowed to be in each cell. You start at (0,0) at time 0 and must move every second to an adjacent cell (you cannot "stand still" in place without moving). Each move takes exactly 1 second. We need the minimum time to reach bottom-right (or -1 if impossible).

A shortest-path in time problem — Dijkstra comes to mind: nodes are cells, edge cost depends on current time because of the earliest-visit constraint. When moving from a cell at time t to neighbor (i,j) with minimum allowed time g = grid[i][j], landing time would be t+1 but may need to "wait" to meet g. However you can't literally wait in place, you can only use moves to expend time; yet except for initial start constraints, once there exist cycles (or other reachable neighbors) you can adjust parity/time by moving around, so you can realize the required waiting by routing.

I recall parity/odd-even issues: if t+1 < g you might need to wait until g or g+1 depending on parity difference; specifically if (g - (t+1)) is even then you can arrive exactly at g, otherwise you must arrive at g+1. Also there's the special impossible case: at start if both first-step neighbors require >1 at t=1 you can't move at t=1 (no valid move), so unreachable.

So approach: early check for start impossibility, then Dijkstra with a min-heap storing earliest reachable time for each cell; when relaxing neighbor compute next time using parity-adjusted waiting as above.

## Refining the problem, round 2 thoughts
- Corner case: grid[0][0] == 0 guaranteed. If both grid[0][1] > 1 and grid[1][0] > 1 (when they exist), impossible because at t=1 you must move somewhere.
- For the transition formula: from time t at (x,y) to neighbor (nx,ny) with g = grid[nx][ny]:
  - If t+1 >= g => arrival = t+1.
  - Else let diff = g - (t+1). If diff % 2 == 0 => arrival = g (you can time moves to land exactly at g), else arrival = g+1.
- Use usual Dijkstra/priority queue: O(m*n log(m*n)). Memory O(m*n) for distances.
- m*n up to 1e5 so fine. Implementation must be careful to not push too many items: use distance matrix and skip outdated heap entries.

## Attempted solution(s)
```python
import heapq

class Solution:
    def minimumTime(self, grid):
        m = len(grid)
        n = len(grid[0])
        # Quick impossible check at start: at t=1 we must move to one of (0,1) or (1,0)
        if m > 1 and n > 1:
            if grid[0][1] > 1 and grid[1][0] > 1:
                return -1
        # distances
        INF = 10**18
        dist = [[INF] * n for _ in range(m)]
        dist[0][0] = 0
        pq = [(0, 0, 0)]  # (time, x, y)
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        while pq:
            t, x, y = heapq.heappop(pq)
            if t != dist[x][y]:
                continue
            if x == m-1 and y == n-1:
                return t
            for dx, dy in dirs:
                nx, ny = x+dx, y+dy
                if nx < 0 or nx >= m or ny < 0 or ny >= n:
                    continue
                need = grid[nx][ny]
                # earliest arrival if we move next second:
                if t + 1 >= need:
                    nt = t + 1
                else:
                    # must wait (via moves) until at least `need`
                    diff = need - (t + 1)
                    # if diff is even, we can land exactly at need; if odd, we need one extra second
                    if diff % 2 == 0:
                        nt = need
                    else:
                        nt = need + 1
                if nt < dist[nx][ny]:
                    dist[nx][ny] = nt
                    heapq.heappush(pq, (nt, nx, ny))
        return -1
```
- Notes about the solution:
  - This is Dijkstra over the grid where the "travel time" to move into a neighbor depends on the current time and the neighbor's minimum-visit constraint.
  - The initial check handles the special case where at t=1 there is no valid first move, which makes the entire problem impossible.
  - The parity adjustment (diff % 2) handles the fact you can only spend time by moving each second; after the initial steps there are usually cycles that let you adjust parity, so the formula yields the earliest achievable arrival time to that neighbor.
  - Time complexity: O(m * n * log(m * n)) because each cell is pushed at most a few times and each heap operation costs log(m*n).
  - Space complexity: O(m * n) for the distance matrix and heap.