# [Problem 827: Making A Large Island](https://leetcode.com/problems/making-a-large-island/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the largest island size after flipping at most one 0 to 1. The straightforward idea: find connected components (islands) of 1s and their sizes, then for each 0 consider flipping it and summing the sizes of distinct neighboring islands (plus the flipped cell). That requires knowing which island each 1 belongs to and how big each island is. Label islands with unique ids and record sizes. For each 0, gather unique neighbor ids and sum sizes + 1. Also handle edge cases: all ones (no zero to flip) so answer is n*n; all zeros (flip one -> 1).

Time should be O(n^2) since we visit each cell a constant number of times. Need to avoid recursion depth issues for n up to 500 — iterative BFS/DFS or use deque.

## Refining the problem, round 2 thoughts
- Use an integer id starting from 2 to avoid confusion with 0 and 1 in the grid.
- Use iterative DFS (stack) or BFS (deque) to label components and compute sizes.
- Keep a dictionary (or list) mapping id -> size.
- Track whether there's any zero in the grid. If none, return n*n immediately.
- For each zero, look at up to 4 neighbors, collect distinct neighbor island ids (set), sum their sizes, add 1, and maximize.
- If there are no islands (all zeros), the maximum after one flip is 1.
- Space complexity is O(n^2) in the worst-case for labels (we overwrite the grid) and storage for the sizes mapping (up to number of islands).
- Time complexity O(n^2): one pass to label all islands, another pass to evaluate all zeros.

## Attempted solution(s)
```python
from collections import deque
from typing import List

class Solution:
    def largestIsland(self, grid: List[List[int]]) -> int:
        n = len(grid)
        if n == 0:
            return 0

        # Directions for 4-neighbor connectivity
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]

        # Map island id -> size. We'll label islands starting from 2.
        island_size = {}
        island_id = 2

        # Helper: BFS/DFS to label an island starting at (r,c)
        for r in range(n):
            for c in range(n):
                if grid[r][c] == 1:
                    # BFS to label all connected 1s with current island_id
                    size = 0
                    dq = deque()
                    dq.append((r,c))
                    grid[r][c] = island_id
                    while dq:
                        x,y = dq.popleft()
                        size += 1
                        for dx,dy in dirs:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == 1:
                                grid[nx][ny] = island_id
                                dq.append((nx, ny))
                    island_size[island_id] = size
                    island_id += 1

        # If no island existed, island_size will be empty.
        # Track if there's any zero cell to decide whether we must flip.
        has_zero = any(grid[r][c] == 0 for r in range(n) for c in range(n))

        # If there is no zero, the whole grid might already be one big island.
        if not has_zero:
            # All cells are 1 (or labeled), return n*n
            return n * n

        # Otherwise, try flipping each zero and compute the resulting island size.
        res = 0
        for r in range(n):
            for c in range(n):
                if grid[r][c] == 0:
                    seen = set()
                    total = 1  # flipping this zero
                    for dx,dy in dirs:
                        nx, ny = r + dx, c + dy
                        if 0 <= nx < n and 0 <= ny < n:
                            nid = grid[nx][ny]
                            if nid > 1 and nid not in seen:
                                seen.add(nid)
                                total += island_size[nid]
                    res = max(res, total)

        # If there were islands but flipping didn't yield more than existing island sizes,
        # compare with largest existing island (in case flipping doesn't increase)
        if island_size:
            res = max(res, max(island_size.values()))
        else:
            # no islands, flipping any zero yields 1
            res = max(res, 1)

        return res
```

- Notes about the solution:
  - Approach: label each island with a unique id (>=2) and store sizes. For each 0, collect distinct adjacent island ids, sum their sizes plus 1 for the flipped cell. Track the maximum.
  - Time complexity: O(n^2). Each cell is visited a constant number of times: once for labeling, and up to once more when evaluating neighbor sums for zeros.
  - Space complexity: O(n^2) worst-case due to in-place labeling of the grid (overwriting values) and the island_size mapping storing sizes for up to O(n^2) islands in pathological checkerboard cases.
  - Implementation details:
    - Use BFS (deque) to avoid recursion limit issues for large n.
    - Label islands starting from 2 to distinguish from original 0/1 values.
    - Use a set when summing neighbor islands to avoid double-counting the same island that touches the zero from multiple sides.
    - Handle edge cases:
      - No zeros -> return n*n (entire grid is already filled with 1s).
      - No ones -> flipping any zero yields 1.