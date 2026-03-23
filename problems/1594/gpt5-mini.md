# [Problem 1594: Maximum Non Negative Product in a Matrix](https://leetcode.com/problems/maximum-non-negative-product-in-a-matrix/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Sorry — I can’t share internal stream-of-consciousness or step-by-step chain-of-thought. I can, however, provide a concise high-level outline of the approach:
- Maintain, for each cell, the maximum and minimum product achievable to that cell (because negative numbers can flip sign).
- Transition each cell from the top and left neighbors by multiplying their max/min with the current cell value and taking the appropriate new max and min.
- At the end, if the maximum product at bottom-right is negative, return -1; otherwise return it modulo 1e9+7.
- Handle zeros naturally (they produce zero products).

## Refining the problem, round 2 thoughts
I won’t provide inner deliberations, but here is a compact summary of refinements, edge cases, and complexity:
- Edge cases: zeros in grid (may produce a 0 product that is preferable to negative products); single-cell grid; all-negative grids where no non-negative product path exists.
- Use two DP arrays of size m x n storing current max and min products (Python ints handle large values; modulo only applied at the very end if result is non-negative).
- Time complexity: O(m * n) since each cell considers two neighbors and up to two candidate values from each.
- Space complexity: O(m * n) (can be optimized to O(n) by rolling arrays, but full m*n is simple and fits constraints m,n <= 15).

## Attempted solution(s)
```python
class Solution:
    def maxProductPath(self, grid: list[list[int]]) -> int:
        MOD = 10**9 + 7
        m, n = len(grid), len(grid[0])
        # dp_max[i][j] = maximum product to reach (i,j)
        # dp_min[i][j] = minimum product to reach (i,j)
        dp_max = [[None] * n for _ in range(m)]
        dp_min = [[None] * n for _ in range(m)]

        dp_max[0][0] = dp_min[0][0] = grid[0][0]

        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    continue
                candidates = []
                val = grid[i][j]

                if i > 0 and dp_max[i-1][j] is not None:
                    candidates.append(dp_max[i-1][j] * val)
                    candidates.append(dp_min[i-1][j] * val)
                if j > 0 and dp_max[i][j-1] is not None:
                    candidates.append(dp_max[i][j-1] * val)
                    candidates.append(dp_min[i][j-1] * val)

                if candidates:
                    dp_max[i][j] = max(candidates)
                    dp_min[i][j] = min(candidates)
                else:
                    dp_max[i][j] = dp_min[i][j] = None

        res = dp_max[m-1][n-1]
        if res is None or res < 0:
            return -1
        return res % MOD
```
- Notes:
  - The DP keeps track of both minimum and maximum products at every cell because multiplying by a negative flips min/max roles.
  - Zeros are naturally handled because multiplying by zero yields zero candidates.
  - Final modulo is applied only after determining the maximum non-negative product.
  - Time complexity: O(m * n). Space complexity: O(m * n) (can be reduced to O(n) with rolling arrays if desired).