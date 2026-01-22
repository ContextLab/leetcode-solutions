# [Problem 1905: Count Sub Islands](https://leetcode.com/problems/count-sub-islands/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to count islands in grid2 that are completely contained within islands of grid1. A straightforward idea: for each island in grid2, check whether every cell of that island corresponds to a 1 in grid1. If so, it's a sub-island. That suggests a flood-fill (DFS/BFS) over grid2 islands, checking cells against grid1 as we go.

An alternate trick I remember: first "erase" any part of grid2 that lands on water in grid1 (i.e., any grid2 cell that is 1 while the same position in grid1 is 0), by flood-filling from those cells to remove their entire connected component in grid2. After this pruning, any remaining island in grid2 must be fully contained in grid1, so counting remaining islands is enough. This is simpler to implement and easy to reason about.

Be careful about recursion depth (m, n up to 500 => 250k cells), so use an iterative stack/queue rather than recursion.

## Refining the problem, round 2 thoughts
Plan:
1. Iterate all cells. If grid2[i][j] == 1 and grid1[i][j] == 0, do an iterative DFS/BFS starting from (i,j) to set all reachable grid2 land cells to 0 (erase that island).
2. After pruning, iterate again and count the remaining islands in grid2 using iterative DFS/BFS to clear them as counted.

Edge cases:
- Entire grid2 is water -> answer 0.
- Large contiguous island sizes -> prefer iterative stack/queue to avoid recursion limit.
- Time complexity should be O(m*n) since each cell is visited O(1) times across both passes. Space complexity O(m*n) worst-case for stack, typically less.

I'll use an explicit stack for DFS and mutate grid2 in-place.

## Attempted solution(s)
```python
from collections import deque
from typing import List

class Solution:
    def countSubIslands(self, grid1: List[List[int]], grid2: List[List[int]]) -> int:
        m = len(grid1)
        n = len(grid1[0])
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        
        # Helper: iterative DFS to erase an island in grid2 starting from (r,c)
        def erase_island(r: int, c: int) -> None:
            stack = [(r,c)]
            grid2[r][c] = 0
            while stack:
                x,y = stack.pop()
                for dx,dy in dirs:
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < m and 0 <= ny < n and grid2[nx][ny] == 1:
                        grid2[nx][ny] = 0
                        stack.append((nx, ny))
        
        # 1) Remove parts of grid2 that are on water in grid1
        for i in range(m):
            for j in range(n):
                if grid2[i][j] == 1 and grid1[i][j] == 0:
                    erase_island(i, j)
        
        # 2) Count remaining islands in grid2
        count = 0
        for i in range(m):
            for j in range(n):
                if grid2[i][j] == 1:
                    count += 1
                    erase_island(i, j)
        
        return count
```
- Notes:
  - Approach: Two-pass flood-fill. First pass removes any grid2 land connected to a cell where grid1 has water, since such grid2 islands cannot be sub-islands. Second pass counts and erases remaining grid2 islands, each of which must be fully contained in grid1.
  - Time complexity: O(m * n). Each cell is visited a constant number of times across the flood-fills.
  - Space complexity: O(m * n) worst-case stack usage (for one very large island), typically less. Using iterative DFS avoids recursion depth issues.