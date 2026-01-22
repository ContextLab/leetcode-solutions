# [Problem 2658: Maximum Number of Fish in a Grid](https://leetcode.com/problems/maximum-number-of-fish-in-a-grid/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I see a grid where water cells have positive fish counts and land cells are zeros. The fisher can start at any water cell and move to adjacent water cells collecting all fish in visited water cells. That means the fisher can collect fish from any connected component of non-zero cells (connectivity via 4-directional adjacency). So the problem reduces to: find each connected component of cells with grid[r][c] > 0 and compute the sum of values in that component, then return the maximum sum among components. Depth-first search or breadth-first search works well; grid is small (m,n <= 10) so recursion depth won't be an issue but iterative DFS/BFS is simple and safe. Mark visited cells to avoid recounting (either a visited set or set grid cells to 0).

## Refining the problem, round 2 thoughts
Refinements / edge cases:
- If there are no water cells (all zeros), answer should be 0.
- Grid size is at most 10x10, so an O(m*n) traversal is trivial. We must ensure we don't reprocess cells.
- Alternatives: union-find could group components, but DFS/BFS is simpler and efficient.
- Complexity: we'll visit each cell at most once; time O(m*n). Space for visited is O(m*n) (or worst-case stack/queue size O(m*n)).
- Implementation detail: use iterative stack or queue to avoid recursion issues (though recursion is fine here). I'll use iterative DFS with a stack and a visited set (or mark cells to 0).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def findMaxFish(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0
        m, n = len(grid), len(grid[0])
        visited = [[False]*n for _ in range(m)]
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        max_fish = 0

        for i in range(m):
            for j in range(n):
                if grid[i][j] > 0 and not visited[i][j]:
                    # iterative DFS to sum component
                    stack = [(i,j)]
                    visited[i][j] = True
                    comp_sum = 0
                    while stack:
                        r, c = stack.pop()
                        comp_sum += grid[r][c]
                        for dr, dc in dirs:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < m and 0 <= nc < n and not visited[nr][nc] and grid[nr][nc] > 0:
                                visited[nr][nc] = True
                                stack.append((nr, nc))
                    max_fish = max(max_fish, comp_sum)
        return max_fish
```
- Notes:
  - Approach: iterate over grid, and for each unvisited water cell, run iterative DFS to compute the sum of that connected component. Track the maximum component sum.
  - Time complexity: O(m * n) because each cell is visited at most once.
  - Space complexity: O(m * n) worst-case for the visited array and the DFS stack. Grid constraints (m, n <= 10) make this trivial to run.
  - Implementation detail: used a visited 2D boolean array to avoid modifying the input grid. Alternatively, one could set visited water cells to 0 in the grid itself.