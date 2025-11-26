# [Problem 2435: Paths in Matrix Whose Sum Is Divisible by K](https://leetcode.com/problems/paths-in-matrix-whose-sum-is-divisible-by-k/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to count number of down/right paths from (0,0) to (m-1,n-1) such that the sum of visited grid values is divisible by k. This is a classic DP over grid where each DP state must remember sum modulo k. Natural DP: dp[i][j][r] = number of ways to reach (i,j) with current sum % k == r. Transition from top or left: shift remainder by grid[i][j] and add counts.

However naive 3D DP storing states for all cells may be memory-heavy in Python because k ≤ 50 and m*n ≤ 5e4 — worst-case could be many integers. We can reduce memory by only keeping previous row and current row (since transitions only from top and left). Also we can transpose the grid so the number of columns is the smaller dimension (to minimize memory for per-column arrays). Complexity will be O(m * n * k) time and O(n * k) memory (after transpose ensuring n ≤ m).

Edge cases: single row or single column (only one path), k = 1 (everything divisible), but DP handles these naturally. Transposing when n > m keeps memory small.

## Refining the problem, round 2 thoughts
- Ensure we transpose the grid so the number of columns (n) ≤ number of rows (m) — that makes O(n*k) memory safe because n ≤ sqrt(m*n) ≤ sqrt(5e4) ≈ 224.
- Use two arrays (prev row and cur row) where each entry is a length-k list of counts.
- Initialize dp at (0,0) with remainder grid[0][0] % k = 1 way.
- For cell (i,j) add contributions from prev[j] (top) and cur[j-1] (left), shifting indices by cell value modulo k.
- Use modulo 10^9+7 for counts.
- Time complexity O(m*n*k) with m*n ≤ 5e4 and k ≤ 50 so ≲ 2.5e6 remainder-updates; memory O(n*k).

Now provide the full Python solution.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def numberOfPaths(self, grid: List[List[int]], k: int) -> int:
        MOD = 10**9 + 7
        m = len(grid)
        n = len(grid[0])
        # Transpose if columns > rows to minimize number of columns (and memory)
        if n > m:
            grid = [list(row) for row in zip(*grid)]
            m, n = n, m  # swapped

        # prev[j] is a list of length k: counts for column j in previous row
        prev = [ [0]*k for _ in range(n) ]

        for i in range(m):
            cur = [ [0]*k for _ in range(n) ]
            for j in range(n):
                val = grid[i][j] % k
                if i == 0 and j == 0:
                    cur[0][val] = 1
                else:
                    # from top (prev row same column)
                    if i > 0:
                        top = prev[j]
                        # shift each remainder by val
                        if val == 0:
                            # small optimization: if val 0, remainders don't shift
                            for r in range(k):
                                cnt = top[r]
                                if cnt:
                                    cur[j][r] = (cur[j][r] + cnt) % MOD
                        else:
                            for r in range(k):
                                cnt = top[r]
                                if cnt:
                                    newr = (r + val) % k
                                    cur[j][newr] = (cur[j][newr] + cnt) % MOD

                    # from left (current row previous column)
                    if j > 0:
                        left = cur[j-1]
                        if val == 0:
                            for r in range(k):
                                cnt = left[r]
                                if cnt:
                                    cur[j][r] = (cur[j][r] + cnt) % MOD
                        else:
                            for r in range(k):
                                cnt = left[r]
                                if cnt:
                                    newr = (r + val) % k
                                    cur[j][newr] = (cur[j][newr] + cnt) % MOD
            prev = cur

        # answer is number of ways to reach last cell with remainder 0
        return prev[n-1][0] % MOD
```
- Notes on approach:
  - We transpose grid when needed to ensure the number of columns n ≤ rows m so memory O(n*k) is small.
  - prev and cur store counts per remainder for each column. For each cell we combine contributions from top (prev[j]) and left (cur[j-1]) after shifting remainders by grid[i][j] % k.
  - Time complexity: O(m * n * k). Given constraints m * n ≤ 5e4 and k ≤ 50, this is at most about 2.5e6 remainder-updates — efficient.
  - Space complexity: O(n * k) after transpose (n ≤ sqrt(m*n)), which fits comfortably in memory.