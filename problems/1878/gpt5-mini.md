# [Problem 1878: Get Biggest Three Rhombus Sums in a Grid](https://leetcode.com/problems/get-biggest-three-rhombus-sums-in-a-grid/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to compute sums of rhombus borders in a grid and return the top three distinct values. A rhombus here is a square rotated 45 degrees whose corners are cell centers. One way is to consider every possible rhombus (position + size) and compute its border sum. The border can be walked along four diagonal directions. For a top vertex at (i, j) and size k, the rhombus will extend k steps down-right, k down-left, k up-left, and k up-right; bounds must permit i + 2*k < m and j - k >= 0 and j + k < n. For k = 0 the rhombus is a single cell. A naive border-walk per rhombus is straightforward and likely fast enough given m, n ≤ 50.

I also recall an optimized approach using diagonal prefix sums to compute each border in O(1), but the simple walk approach yields acceptable complexity here and is simpler to implement correctly and clearly.

## Refining the problem, round 2 thoughts
Refinements and edge cases:
- Include k = 0 rhombus (single cell).
- Avoid double-counting corners: if I walk edge-by-edge and always move from one corner to the next adding each newly visited cell, and add the top corner explicitly at start, every border cell is added exactly once.
- Valid k must satisfy bounds so all intermediate cells are within grid.
- Collect distinct sums in a set, then sort descending and return up to three.
- Complexity: For each top vertex (m*n) and each k up to ~min(m,n)/2, we walk O(k) cells per rhombus => roughly O(m * n * k^2) worst-case but with constraints this is fine.

Alternative: Using diagonal prefix sums for O(1) per rhombus border sum yields O(m*n*k) overall; but not needed here.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def getBiggestThree(self, grid: List[List[int]]) -> List[int]:
        m, n = len(grid), len(grid[0])
        vals = set()
        # Iterate over possible top vertices (i, j)
        for i in range(m):
            for j in range(n):
                k = 0
                # while rhombus of size k fits with top at (i,j)
                while i + 2 * k < m and j - k >= 0 and j + k < n:
                    # compute border sum by walking around the perimeter
                    if k == 0:
                        vals.add(grid[i][j])
                    else:
                        s = grid[i][j]  # start with top corner
                        r, c = i, j
                        # move down-right k steps
                        for _ in range(k):
                            r += 1; c += 1
                            s += grid[r][c]
                        # move down-left k steps
                        for _ in range(k):
                            r += 1; c -= 1
                            s += grid[r][c]
                        # move up-left k steps
                        for _ in range(k):
                            r -= 1; c -= 1
                            s += grid[r][c]
                        # move up-right k steps
                        for _ in range(k):
                            r -= 1; c += 1
                            s += grid[r][c]
                        vals.add(s)
                    k += 1
        # Extract top three distinct values in descending order
        res = sorted(vals, reverse=True)
        return res[:3]
```
- Notes on approach:
  - We treat each cell (i, j) as the top vertex of potential rhombi with varying sizes k >= 0.
  - For size k, we ensure i + 2*k < m and j - k >= 0 and j + k < n (so all four edges fit).
  - Border sum is computed by starting at the top corner, then walking the four diagonal edges; this adds each border cell exactly once.
  - Distinct sums are kept in a set; final result is the three largest values sorted in descending order.

- Complexity:
  - Time: O(m * n * K^2) in the worst case, where K = O(min(m, n)) is the maximum rhombus half-height. With m, n ≤ 50 this is easily acceptable.
  - Space: O(m * n) worst-case for the set of distinct sums (actually bounded by number of rhombi), plus O(1) extra beyond input and output.