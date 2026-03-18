# [Problem 3070: Count Submatrices with Top-Left Element and Sum Less Than k](https://leetcode.com/problems/count-submatrices-with-top-left-element-and-sum-less-than-k/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The phrase "contain the top-left element of the grid" means every valid submatrix must include cell (0,0). For an axis-aligned submatrix to include (0,0), its top-left corner must be (0,0) (indices are 0-based). Thus every candidate is just a prefix rectangle from (0,0) to (i,j). So we only need to check all O(m * n) prefix rectangles and count those whose sum <= k. Computing each rectangle's sum quickly suggests using a 2D prefix-sum matrix so each prefix rectangle sum is available in O(1).

## Refining the problem, round 2 thoughts
We can build a 2D prefix sum (standard DP): prefix[i][j] = grid[i][j] + prefix[i-1][j] + prefix[i][j-1] - prefix[i-1][j-1]. Then iterate all i,j and check prefix[i][j] <= k. Complexity will be O(m * n) time and O(m * n) space for the prefix array. Since m,n ≤ 1000, m*n ≤ 1e6 — both time and memory are acceptable. If desired, we could compute prefix sums in-place in grid to save memory (modifies input), or use streaming accumulation to reduce extra space to O(1) or O(n), but the explicit prefix matrix is simple and clear. Edge cases: small grids 1x1, large sums (Python int handles big integers), k up to 1e9 but sums can exceed that — still fine.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def countSubmatrices(self, grid: List[List[int]], k: int) -> int:
        m = len(grid)
        n = len(grid[0])
        prefix = [[0] * n for _ in range(m)]
        ans = 0
        
        for i in range(m):
            for j in range(n):
                top = prefix[i-1][j] if i > 0 else 0
                left = prefix[i][j-1] if j > 0 else 0
                diag = prefix[i-1][j-1] if i > 0 and j > 0 else 0
                prefix[i][j] = grid[i][j] + top + left - diag
                if prefix[i][j] <= k:
                    ans += 1
        return ans
```
- Notes:
  - Approach: compute a 2D prefix sum and count how many prefix rectangles (from (0,0) to (i,j)) have sum <= k.
  - Time complexity: O(m * n) — we visit each cell once and do O(1) work per cell.
  - Space complexity: O(m * n) for the prefix matrix. This can be reduced to O(1) extra by modifying grid in-place or to O(n) by streaming column accumulations, but O(m * n) is acceptable given constraints.