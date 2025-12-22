# [Problem 960: Delete Columns to Make Sorted III](https://leetcode.com/problems/delete-columns-to-make-sorted-iii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We are allowed to delete some columns (same indices across all rows) so that each resulting row (string) is non-decreasing (characters left-to-right do not decrease). We want to minimize number of deleted columns.

Thinking: Equivalent to keep as many columns as possible such that for each row, the kept columns form a non-decreasing sequence. If we think of columns indices 0..m-1, we need to select a subsequence of columns (in increasing index order) where for every adjacent chosen columns i < j we have for every row r: strs[r][i] <= strs[r][j]. That is a "compatible" relation between columns. So the problem reduces to finding the longest subsequence of columns that is pairwise compatible in the left-to-right order. That is a longest non-decreasing subsequence in a partial order defined by the per-row comparisons.

A direct DP: dp[j] = length of longest valid subsequence ending at column j. For each j, check all i < j and if column i <= column j for all rows then dp[j] = max(dp[j], dp[i] + 1). The answer is m - max(dp). Complexity: O(m^2 * n) checks, which with m,n ≤ 100 is fine.

## Refining the problem, round 2 thoughts
Edge cases:
- Single column (m = 1): no deletions needed if single character is trivially non-decreasing in each row -> answer 0.
- Single row: problem reduces to deleting columns to make the single string non-decreasing — same DP still works because comparisons are over one row.
- Many rows: need to ensure the pairwise column check verifies all rows.

Optimization thoughts:
- We can early-break when a row violates s[row][i] <= s[row][j].
- Optionally precompute a boolean matrix ok[i][j] indicating compatibility to avoid repeating checks, but with constraints it's unnecessary.
- Space O(m) for dp; time O(m^2 * n), worst-case 1e6 character comparisons, which is acceptable.

Correctness:
- The DP enumerates all subsequences in order because dp[j] considers extending any valid subsequence ending before j that is compatible. This yields longest compatible subsequence (classic DP for LIS in O(m^2) with custom comparator).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minDeletionSize(self, strs: List[str]) -> int:
        if not strs:
            return 0
        n = len(strs)
        m = len(strs[0])
        # dp[j] = length of longest compatible subsequence of columns ending at j
        dp = [1] * m
        best = 1
        for j in range(m):
            for i in range(j):
                # check if column i can precede column j (for all rows s[row][i] <= s[row][j])
                ok = True
                for r in range(n):
                    if strs[r][i] > strs[r][j]:
                        ok = False
                        break
                if ok:
                    dp[j] = max(dp[j], dp[i] + 1)
            if dp[j] > best:
                best = dp[j]
        # minimum deletions = total columns - length of longest kept subsequence
        return m - best
```
- Notes:
  - Approach: DP for longest subsequence of compatible columns. For columns i < j, column j can extend column i if for every row r, strs[r][i] <= strs[r][j].
  - Time complexity: O(m^2 * n) where m = number of columns, n = number of rows. With constraints (<=100), this is efficient.
  - Space complexity: O(m) for dp.
  - Implementation details: early break on row violation to avoid unnecessary checks. The result is m - max(dp).