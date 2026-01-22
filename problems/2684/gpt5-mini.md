# [Problem 2684: Maximum Number of Moves in a Grid](https://leetcode.com/problems/maximum-number-of-moves-in-a-grid/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This is a grid DP / longest-path-in-DAG type problem. Moves only go one column to the right (to row-1, row, or row+1) and only if the next cell's value is strictly larger. Because column index strictly increases on each move, there are no cycles — the graph is a DAG in terms of columns. That suggests dynamic programming from right to left or memoized DFS.

A straightforward DP: dp[r][c] = maximum number of moves starting from (r,c). For the last column dp = 0. For other columns, check up to three neighbors in column c+1 with larger values and take 1 + max(dp[neighbor]). Complexity would be O(m * n) checking a constant 3 neighbors per cell. Space can be optimized to only keep the next column's dp (O(m)) rather than full m*n dp.

I'll implement right-to-left DP with O(m) extra space.

## Refining the problem, round 2 thoughts
- Edge cases: no possible moves from first column → answer 0; large m,n but m*n ≤ 1e5 so O(m*n) time is fine.
- Implement carefully boundaries for row indices.
- Use two 1D arrays: next_dp representing dp for column c+1, and compute curr_dp for column c. After processing column c, assign next_dp = curr_dp.
- Return max over dp values in column 0 (i.e., next_dp after processing c=0).
- Alternative: DFS with memoization would also work but would rely on recursion (depth ≤ n) and extra overhead; iterative DP is simpler and efficient.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxMoves(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])
        # dp for the last column: zero moves possible
        next_dp = [0] * m  # dp values for column c+1 during iteration

        # iterate columns from n-2 down to 0
        for c in range(n - 2, -1, -1):
            curr_dp = [0] * m
            for r in range(m):
                best = 0
                val = grid[r][c]
                # check r-1, r, r+1 in column c+1
                if r - 1 >= 0 and grid[r - 1][c + 1] > val:
                    best = max(best, 1 + next_dp[r - 1])
                if grid[r][c + 1] > val:
                    best = max(best, 1 + next_dp[r])
                if r + 1 < m and grid[r + 1][c + 1] > val:
                    best = max(best, 1 + next_dp[r + 1])
                curr_dp[r] = best
            next_dp = curr_dp

        # next_dp now holds dp values for column 0
        return max(next_dp) if next_dp else 0
```
- Notes about the solution:
  - Approach: Right-to-left dynamic programming across columns. dp[r][c] equals the maximum moves starting from (r,c). We only need dp for the next column to compute the current column, so space is O(m).
  - Time complexity: O(m * n). Each cell checks up to three neighbors in constant time.
  - Space complexity: O(m) extra space (two arrays of length m, reused).
  - Implementation details: handle row boundary checks for neighbors; initialize last column dp to zeros; iterate columns from n-2 down to 0. The final answer is the maximum dp value for the first column.