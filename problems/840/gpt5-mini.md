# [Problem 840: Magic Squares In Grid](https://leetcode.com/problems/magic-squares-in-grid/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count 3x3 subgrids that are magic squares: they must contain distinct numbers from 1 to 9 and each row, column and both diagonals sum to the same value. For a 3x3 magic square containing numbers 1..9 the magic sum is 15 (since sum 1..9 = 45, divided by 3 rows = 15). Also I recall a useful property: in any 3x3 1..9 magic square the center must be 5. That gives a quick filter. So for each possible 3x3 window, check that all 9 numbers are exactly the set {1..9} (or at least distinct and in 1..9) and that rows/cols/diagonals each sum to 15 (or check center==5 then sums). The grid is small (<=10x10) so brute force over all windows with O(1) checks per window is fine.

## Refining the problem, round 2 thoughts
Refine checks to be fast and simple:
- Iterate over top-left corners i in [0..rows-3], j in [0..cols-3].
- For each window, quickly check center == 5 (prune many windows).
- Validate all 9 numbers are in 1..9 and all distinct (use set equality with set(range(1,10)) or check set size 9 and range).
- Check sums: each of 3 rows and 3 columns and both diagonals sum to 15. If all true, increment count.

Edge cases:
- grid smaller than 3x3 → return 0.
- grid may contain zeros or values up to 15; those will fail the 1..9 check.

Time complexity: O(rows * cols) windows, each window constant work (9 element checks and fixed number of sums) → O(R*C). Space is O(1) extra (ignoring negligible temporary list/set of size 9).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def numMagicSquaresInside(self, grid: List[List[int]]) -> int:
        rows = len(grid)
        cols = len(grid[0]) if rows else 0
        if rows < 3 or cols < 3:
            return 0

        target_set = set(range(1, 10))
        count = 0

        for i in range(rows - 2):
            for j in range(cols - 2):
                # Quick center check: center must be 5 in any 3x3 magic square with numbers 1..9
                if grid[i+1][j+1] != 5:
                    continue

                # Collect the 3x3 values
                vals = [
                    grid[i + r][j + c]
                    for r in range(3)
                    for c in range(3)
                ]

                # Must contain all numbers 1..9 exactly once
                if set(vals) != target_set:
                    continue

                # Check rows
                if (grid[i][j] + grid[i][j+1] + grid[i][j+2] != 15 or
                    grid[i+1][j] + grid[i+1][j+1] + grid[i+1][j+2] != 15 or
                    grid[i+2][j] + grid[i+2][j+1] + grid[i+2][j+2] != 15):
                    continue

                # Check columns
                if (grid[i][j] + grid[i+1][j] + grid[i+2][j] != 15 or
                    grid[i][j+1] + grid[i+1][j+1] + grid[i+2][j+1] != 15 or
                    grid[i][j+2] + grid[i+1][j+2] + grid[i+2][j+2] != 15):
                    continue

                # Check diagonals
                if (grid[i][j] + grid[i+1][j+1] + grid[i+2][j+2] != 15 or
                    grid[i][j+2] + grid[i+1][j+1] + grid[i+2][j] != 15):
                    continue

                # Passed all checks
                count += 1

        return count
```
- Notes:
  - Approach: brute-force all 3x3 windows with constant-time validation. Center==5 and set=={1..9} prune most candidates and ensure uniqueness and correct range.
  - Time complexity: O(R * C) windows, constant time per window => O(R*C). Given constraints (max 10x10), this is efficient.
  - Space complexity: O(1) extra (temporary list/set of size 9).