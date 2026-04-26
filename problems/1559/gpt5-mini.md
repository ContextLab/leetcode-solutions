# [Problem 1559: Detect Cycles in 2D Grid](https://leetcode.com/problems/detect-cycles-in-2d-grid/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to detect any cycle of length >= 4 formed by same letters in the grid. This is graph cycle detection on a grid where each cell is a node and edges connect 4-directionally adjacent cells with the same character. Because the graph is undirected, a standard DFS that ignores the immediate parent and flags back-edges to earlier visited nodes (that are not the parent) should find cycles. I must ensure cycles of length >=4 only are reported (so trivial two-node back-and-forth is not a cycle). Recursion may overflow on large grids (500x500), so an iterative DFS or increasing recursion limit is preferable.

A DFS that records discovery depths works: when we encounter a visited neighbor that's not the parent, we can compute cycle length as current_depth - neighbor_depth + 1; if >= 4, return True. Use a depth matrix initialized to 0 to mark unvisited cells and store discovery depth.

## Refining the problem, round 2 thoughts
- We should run a DFS starting from every unvisited cell. Depth values need to be persistent for the connected component so that encountering a previously visited node means it was discovered in this component (we only start DFS on unvisited nodes).
- Use iterative DFS to avoid recursion depth issues. Stack entries store (r, c, parent_r, parent_c). When first pushing a neighbor, set its depth = depth[current] + 1 to avoid pushing it multiple times.
- When exploring a neighbor:
  - skip out-of-bounds or different character;
  - skip the immediate parent (pr, pc) since that is allowed;
  - if depth[neighbor] == 0, it's unvisited -> set depth and push;
  - else (visited), compute cycle length = depth[current] - depth[neighbor] + 1; if >=4 return True.
- Time complexity: O(m * n) since each cell is visited once and each edge considered constant times.
- Space complexity: O(m * n) for depth matrix and stack worst-case.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def containsCycle(self, grid: List[List[str]]) -> bool:
        m = len(grid)
        n = len(grid[0])
        # depth[r][c] = discovery time (0 means unvisited)
        depth = [[0] * n for _ in range(m)]
        dirs = [(1,0), (-1,0), (0,1), (0,-1)]
        
        for i in range(m):
            for j in range(n):
                if depth[i][j] != 0:
                    continue
                # start iterative DFS from (i, j)
                depth[i][j] = 1
                stack = [(i, j, -1, -1)]  # (r, c, parent_r, parent_c)
                
                while stack:
                    r, c, pr, pc = stack.pop()
                    for dr, dc in dirs:
                        nr, nc = r + dr, c + dc
                        if nr < 0 or nr >= m or nc < 0 or nc >= n:
                            continue
                        if grid[nr][nc] != grid[r][c]:
                            continue
                        # ignore the immediate parent cell
                        if nr == pr and nc == pc:
                            continue
                        if depth[nr][nc] == 0:
                            depth[nr][nc] = depth[r][c] + 1
                            stack.append((nr, nc, r, c))
                        else:
                            # visited before; check cycle length
                            # cycle length = depth[r][c] - depth[nr][nc] + 1
                            if depth[r][c] - depth[nr][nc] + 1 >= 4:
                                return True
        return False
```
- Notes:
  - We perform an iterative DFS for each unvisited cell, using a depth matrix to store discovery order.
  - The parent check (nr == pr and nc == pc) prevents counting the immediate reverse move as a cycle.
  - When we visit an already discovered neighbor that is not the parent, we compute the cycle length using discovery depths. If it's >= 4, a valid cycle is found.
  - Time complexity: O(m * n). Each cell is discovered once and each neighbor edge is considered a constant number of times.
  - Space complexity: O(m * n) for the depth matrix and worst-case stack usage.