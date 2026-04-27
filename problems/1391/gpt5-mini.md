# [Problem 1391: Check if There is a Valid Path in a Grid](https://leetcode.com/problems/check-if-there-is-a-valid-path-in-a-grid/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Sorry — I can’t share my internal stream-of-consciousness. I can, however, give a concise summary of the high-level idea I would use:

Summary: Treat the grid as a graph where each cell connects to adjacent cells only if the street type in the current cell allows movement in that direction and the neighbor's street type allows movement back (i.e., they are mutually connected). Do a BFS/DFS from (0,0) and check whether (m-1,n-1) is reachable.

## Refining the problem, round 2 thoughts
I can’t provide internal chain-of-thought details, but here is a brief refined plan and edge cases to consider:

- Represent directions as indices and map each street type to the allowed outgoing directions.
- When moving from a cell in direction d, ensure the neighbor exists and its street type contains the opposite direction.
- Use BFS (or DFS) with a visited set to avoid cycles.
- Edge cases: single-cell grid (m=n=1) should return True; ensure bounds checks; ensure correct direction/opposite mapping.

Time complexity: O(m * n) because each cell is visited at most once.
Space complexity: O(m * n) for the visited set / queue.

## Attempted solution(s)
```python
from collections import deque
from typing import List

class Solution:
    def hasValidPath(self, grid: List[List[int]]) -> bool:
        if not grid:
            return False
        m, n = len(grid), len(grid[0])
        # If single cell, trivially true
        if m == 1 and n == 1:
            return True

        # Directions: 0=up, 1=right, 2=down, 3=left
        dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        # For each street type, which directions it connects to
        type_dirs = {
            1: [3, 1],   # left, right
            2: [0, 2],   # up, down
            3: [3, 2],   # left, down
            4: [1, 2],   # right, down
            5: [3, 0],   # left, up
            6: [1, 0],   # right, up
        }
        # Opposite direction mapping
        opp = {0: 2, 1: 3, 2: 0, 3: 1}

        visited = [[False] * n for _ in range(m)]
        q = deque()
        q.append((0, 0))
        visited[0][0] = True

        while q:
            i, j = q.popleft()
            if i == m - 1 and j == n - 1:
                return True
            cur_type = grid[i][j]
            for d in type_dirs[cur_type]:
                ni, nj = i + dirs[d][0], j + dirs[d][1]
                if not (0 <= ni < m and 0 <= nj < n):
                    continue
                if visited[ni][nj]:
                    continue
                neigh_type = grid[ni][nj]
                # Check if neighbor has the opposite direction to connect back
                if opp[d] in type_dirs[neigh_type]:
                    visited[ni][nj] = True
                    q.append((ni, nj))

        return False
```
- Solution approach: BFS from (0,0), only traverse to neighbors that the current street can reach and that have a street that connects back (mutual connectivity). Use a visited matrix to avoid revisiting cells.
- Time complexity: O(m * n) — each cell is visited at most once and neighbor checks are constant-time.
- Space complexity: O(m * n) — for visited and BFS queue in worst case.
- Implementation details: Careful mapping of street types to directions and correct opposite direction checks are crucial. The code handles the single-cell trivial case and respects grid boundaries.