# [Problem 1568: Minimum Number of Days to Disconnect Island](https://leetcode.com/problems/minimum-number-of-days-to-disconnect-island/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can’t share internal chain-of-thought, but here is a brief, concise summary of the approach: check whether the grid is already disconnected (0 or multiple islands) -> return 0. Otherwise, try removing each land cell (temporarily flip it to water) and check if that produces a disconnected grid -> if any do, return 1. If no single-cell removal disconnects the island, answer is 2 (maximum needed under constraints).

## Refining the problem, round 2 thoughts
- Edge cases:
  - If initial island count is 0 or >1: already disconnected, return 0.
  - If there's exactly one cell of land: removing it yields 0 islands, so return 1.
  - If removing any single land cell results in >1 or 0 islands, return 1; otherwise return 2.
- Implementation details:
  - Grid sizes up to 30x30 => brute-force flipping each land cell and running a DFS/BFS to count islands is acceptable.
  - When counting islands, early exit once count > 1 to save time.
- Complexity:
  - Let k = number of cells (m*n). Counting islands costs O(k). Trying up to O(k) cells gives O(k^2) time worst-case, with O(k) space for visited.

## Attempted solution(s)
```python
from typing import List
class Solution:
    def minDays(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])

        def count_islands():
            visited = [[False]*n for _ in range(m)]
            dirs = [(1,0),(-1,0),(0,1),(0,-1)]
            def dfs(i,j):
                stack = [(i,j)]
                visited[i][j] = True
                while stack:
                    x,y = stack.pop()
                    for dx,dy in dirs:
                        nx, ny = x+dx, y+dy
                        if 0 <= nx < m and 0 <= ny < n and not visited[nx][ny] and grid[nx][ny] == 1:
                            visited[nx][ny] = True
                            stack.append((nx,ny))

            count = 0
            for i in range(m):
                for j in range(n):
                    if grid[i][j] == 1 and not visited[i][j]:
                        count += 1
                        if count > 1:
                            return count
                        dfs(i,j)
            return count

        # Initial check
        initial_islands = count_islands()
        if initial_islands == 0 or initial_islands > 1:
            return 0

        # Try removing one land cell
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    grid[i][j] = 0
                    islands_after = count_islands()
                    grid[i][j] = 1
                    if islands_after == 0 or islands_after > 1:
                        return 1

        # Otherwise need at least 2 removals
        return 2
```
- Notes:
  - Approach: brute-force try flipping each land cell and check connectivity via DFS; early exit optimizations (stop counting islands once >1) reduce work.
  - Time complexity: O((m*n)^2) worst-case (for each cell we may traverse the grid to count islands).
  - Space complexity: O(m*n) for visited array and DFS stack in worst-case.