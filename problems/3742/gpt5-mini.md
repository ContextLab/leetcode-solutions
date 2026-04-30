# [Problem 3742: Maximum Path Score in a Grid](https://leetcode.com/problems/maximum-path-score-in-a-grid/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the maximum sum of values along a path from (0,0) to (m-1,n-1) moving only right/down, but with a constraint that the total "cost" (number of cells with value 1 or 2) is <= k. Each cell with value 1 or 2 contributes cost 1 but different score (1 or 2). This looks like a DP with an extra dimension for cost: for each cell (i,j) and for each allowed cost c (0..k) track the maximum score achievable reaching (i,j) with exactly cost c. Then take the maximum over c<=k at the destination. Because m,n up to 200 and k up to 1000, an O(m*n*k) DP is acceptable. Memory needs to be careful: storing full 3D dp would be huge, but we can keep only the previous row (and current row) of dp arrays, each cell holding an array of length k+1.

## Refining the problem, round 2 thoughts
Refined approach:
- Let dp[i][j][c] = max score to reach (i,j) with cost exactly c (or -inf if unreachable).
- Transition: from top dp[i-1][j][c0] or left dp[i][j-1][c0], if c0 + cost_here <= k, update dp[i][j][c0 + cost_here] = max(prev + value_here).
- Initialize dp[0][0][0] = 0 (grid[0][0] guaranteed 0).
- Answer is max(dp[m-1][n-1][c]) for c in 0..k; if all unreachable return -1.

Edge cases:
- k = 0: can only go through zeros; algorithm naturally handles this.
- If no path respects cost <= k, return -1.
- grid[0][0] == 0 guaranteed simplifies start.

Time complexity: O(m * n * k).
Space complexity: O(n * (k+1)) if we store only one row (prev) and one current row.

The DP loops are straightforward but pay attention to implementation performance in Python: use local variables and avoid repeated global lookups where possible.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maximumPath(self, grid: List[List[int]], k: int) -> int:
        m = len(grid)
        n = len(grid[0])
        NEG = -10**12  # sufficiently small sentinel for unreachable states

        # prev_row[j] will be a list of length k+1: best scores to reach (i-1, j) with cost c
        # We'll build the first row (i = 0) separately, then iterate rows 1..m-1.
        # Initialize prev_row for the "row before the first" as not used; we'll build row0 directly.
        # Build row 0
        prev_row = [ [NEG] * (k + 1) for _ in range(n) ]
        for j in range(n):
            val = grid[0][j]
            cost_here = 1 if val > 0 else 0
            cur = [NEG] * (k + 1)
            if j == 0:
                # start cell (0,0), grid[0][0] == 0 per constraints
                if cost_here <= k:
                    cur[cost_here] = val
            else:
                # can only come from left (same row)
                left = prev_row[j-1]
                # try all previous costs
                limit = k - cost_here
                for c_prev in range(limit + 1):
                    if left[c_prev] != NEG:
                        newc = c_prev + cost_here
                        score = left[c_prev] + val
                        if score > cur[newc]:
                            cur[newc] = score
            prev_row[j] = cur

        # Process remaining rows
        for i in range(1, m):
            curr_row = [ [NEG] * (k + 1) for _ in range(n) ]
            for j in range(n):
                val = grid[i][j]
                cost_here = 1 if val > 0 else 0
                cur = [NEG] * (k + 1)

                limit = k - cost_here
                # From top (prev_row[j])
                top = prev_row[j]
                for c_prev in range(limit + 1):
                    if top[c_prev] != NEG:
                        newc = c_prev + cost_here
                        score = top[c_prev] + val
                        if score > cur[newc]:
                            cur[newc] = score

                # From left (curr_row[j-1]) if j > 0
                if j > 0:
                    left = curr_row[j-1]
                    for c_prev in range(limit + 1):
                        if left[c_prev] != NEG:
                            newc = c_prev + cost_here
                            score = left[c_prev] + val
                            if score > cur[newc]:
                                cur[newc] = score

                curr_row[j] = cur
            prev_row = curr_row

        # At destination (m-1, n-1) find maximum score among costs <= k
        dest = prev_row[n-1]
        ans = max(dest)
        return ans if ans > NEG else -1
```
- Notes about the solution:
  - dp is implemented row-by-row to save memory: prev_row holds arrays of length k+1 for each column.
  - We use NEG as a sentinel for unreachable states.
  - Time complexity: O(m * n * k), each cell does ~2 * (k+1) checks (from top and left).
  - Space complexity: O(n * (k+1)) for the two rows (prev/current) held across iterations.
  - This approach is straightforward and deterministic; in many practical cases a sparse/dictionary-based DP could be more efficient, but the array approach is simple and fits problem constraints.