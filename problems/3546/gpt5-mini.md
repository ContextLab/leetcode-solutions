# [Problem 3546: Equal Sum Grid Partition I](https://leetcode.com/problems/equal-sum-grid-partition-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to check whether a single straight cut (horizontal between two rows or vertical between two columns) can split the grid into two non-empty parts with equal sums. That immediately suggests checking prefix sums: for horizontal cuts compute cumulative sums of whole rows; for vertical cuts compute cumulative sums of whole columns. The total sum must be even to split equally. If total is even, check whether any prefix (not including the entire grid) equals total/2. Complexity-wise we have to read every cell at least once to compute sums, which is fine because m*n <= 1e5. Edge cases: single row or single column (one type of cut impossible), but the logic of excluding the full prefix will handle that.

## Refining the problem, round 2 thoughts
Refinement: compute row sums and column sums in a single pass over the grid: build an array row_sums and an array col_sums. Compute total as sum(row_sums). If total is odd -> return False. Let target = total // 2. Then check prefix of row_sums up to m-1 (i.e., prefix after row i where i in [0..m-2]) for equality with target. If none found, check prefix of col_sums up to n-1. If either found, return True. This covers non-empty requirement automatically because we never allow prefix to be the whole grid. Time O(m*n) to compute sums and O(m + n) to check prefixes. Space O(m + n) (but arrays sizes are bounded because m*n <= 1e5). Alternative would be two passes (one for rows, one for columns) but single-pass computing both row and column sums is simple and efficient.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def equalSumGridPartition(self, grid: List[List[int]]) -> bool:
        # Build row sums and column sums in one pass
        m = len(grid)
        n = len(grid[0])
        row_sums = [0] * m
        col_sums = [0] * n
        total = 0

        for i in range(m):
            rsum = 0
            row = grid[i]
            # accumulate row sum and update column sums
            for j, val in enumerate(row):
                rsum += val
                col_sums[j] += val
            row_sums[i] = rsum
            total += rsum

        # total must be even to split into two equal integer sums
        if total % 2 != 0:
            return False
        target = total // 2

        # Check horizontal cut: prefix of row_sums equals target (exclude full prefix)
        prefix = 0
        # only consider prefix that leaves at least one row below -> i in [0..m-2]
        for i in range(m - 1):
            prefix += row_sums[i]
            if prefix == target:
                return True

        # Check vertical cut: prefix of col_sums equals target (exclude full prefix)
        prefix = 0
        for j in range(n - 1):
            prefix += col_sums[j]
            if prefix == target:
                return True

        return False
```
- Approach: compute sums per row and per column in one pass, check if total is even, then check row-prefixes and column-prefixes (excluding the full grid) for equality with total/2.
- Time complexity: O(m * n) to scan all cells once (plus O(m + n) for prefix checks). Since m * n <= 1e5 this is efficient.
- Space complexity: O(m + n) for row_sums and col_sums arrays.