# [Problem 1970: Last Day Where You Can Still Cross](https://leetcode.com/problems/last-day-where-you-can-still-cross/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the last day when a path of land (0s) exists from the top row to the bottom row while cells become water (1s) one by one according to the given order. One natural idea is to simulate days and check connectivity each day, but simulating every day naively and running a BFS/DFS each time would be O(n^2) where n = row*col which could be expensive.

I recall a typical approach is binary search on the day: for a candidate day d, mark the first d cells as water and check if there's any path from top to bottom using only land. If a path exists at day d, then it's possible at all days <= d, so try larger days; otherwise try smaller days. Checking connectivity for a fixed day is a BFS/DFS over the grid (O(row*col)). Since row*col <= 2e4, binary searching over n days (log n ≈ <= 15) * O(n) per check is fine.

An alternative is reverse simulation with Union-Find: start with all water and add land cells in reverse order; when a land cell joining causes a top-connected component to connect to a bottom-connected component, the corresponding day is the answer. That's also efficient but slightly more code.

I'll implement binary search + BFS for clarity.

## Refining the problem, round 2 thoughts
- Days are 1-based in the input: on day i, cells[i-1] becomes water. On day d, the first d entries in cells are water.
- We want the last day when crossing is still possible. I'll binary search for the maximum d where crossing is possible. Search range is [0, n], where 0 means no water (all land) and n means all flooded.
- For the BFS/DFS check on a given day:
  - Build a grid (row x col) initialized to land (0), mark the first d cells as water (1).
  - Start BFS from every land cell in the top row; if BFS reaches the bottom row, crossing is possible.
- Complexity: each check O(row * col), binary search gives O(row * col * log(row*col)). Memory O(row*col) for the grid and visited flags.
- Edge cases: day = 0 (should return True if there's a path on all-land grid, which obviously exists unless rows==0, but constraints guarantee rows>=2), day = n (all water -> no path).
- Implementation details: convert 1-based cells coordinates to 0-based when marking the grid. Use deque for BFS. Use visited boolean grid.

## Attempted solution(s)
```python
from collections import deque
from typing import List

class Solution:
    def latestDayToCross(self, row: int, col: int, cells: List[List[int]]) -> int:
        n = len(cells)

        def can_cross(day: int) -> bool:
            # day: number of flooded cells (first 'day' entries in cells are water)
            grid = [[0] * col for _ in range(row)]  # 0 = land, 1 = water
            for i in range(day):
                r, c = cells[i]
                grid[r - 1][c - 1] = 1

            q = deque()
            visited = [[False] * col for _ in range(row)]
            # Enqueue all land cells in top row
            for j in range(col):
                if grid[0][j] == 0:
                    q.append((0, j))
                    visited[0][j] = True

            dirs = [(1,0), (-1,0), (0,1), (0,-1)]
            while q:
                r0, c0 = q.popleft()
                if r0 == row - 1:  # reached bottom
                    return True
                for dr, dc in dirs:
                    nr, nc = r0 + dr, c0 + dc
                    if 0 <= nr < row and 0 <= nc < col and not visited[nr][nc] and grid[nr][nc] == 0:
                        visited[nr][nc] = True
                        q.append((nr, nc))
            return False

        # Binary search for the last day where crossing is possible
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if can_cross(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
```
- Notes on approach:
  - We binary search the last day d in [0, n] such that a top-to-bottom land-only path exists when the first d cells are flooded.
  - can_cross(day) constructs the grid with the first 'day' cells flooded and runs BFS from all top-row land cells; if BFS reaches any bottom-row cell, return True.
- Complexity:
  - Time: O(n * log n) where n = row * col. More precisely, each can_cross is O(row * col) and binary search does O(log n) checks, so O(row*col*log(row*col)).
  - Space: O(row * col) for grid and visited arrays.
- Alternative:
  - A union-find solution adding land in reverse order can achieve O(n * α(n)) time and is slightly more optimal in practice; the binary search + BFS is simpler and well within limits for the given constraints.