# [Problem 2661: First Completely Painted Row or Column](https://leetcode.com/problems/first-completely-painted-row-or-column/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to process arr in order, painting cells in mat. As soon as any row or column becomes fully painted we return the index i. Because arr and mat contain the numbers 1..m*n uniquely, we can map each value to its (row, col) in mat so we can quickly find where each arr[i] paints. Then maintain counters for each row and column; increment the appropriate row and column counters on each paint, and check if either reached the required count (n for a row, m for a column). This gives O(1) per arr element after mapping.

I'm thinking to build a map val -> (r,c) by scanning mat once. Then iterate arr from i=0.., look up (r,c), increment rowCnt[r] and colCnt[c], check equality to n or m, and return i. Edge cases: 1x1 matrix (first paint finishes both), tall or wide matrices; constraints guarantee product <= 1e5 so mapping fits memory.

## Refining the problem, round 2 thoughts
Confirm complexity: building the map costs O(m*n), arr length is m*n so total time O(m*n). Space: O(m*n) for the map, plus O(m + n) for counters. Could reduce memory slightly by storing positions in an array indexed by value (size m*n + 1) instead of dict; but dict is fine. Must be careful with 0 vs 1-based values (values are 1..m*n). Also we should return the index in arr (0-based), not the value.

Alternative: Instead of storing tuple, could store single encoded integer (r*n + c) but tuple is fine and clear. Handle immediate return when counts hit required size.

Now implement cleanly in Python with LeetCode signature.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def firstCompleteIndex(self, arr: List[int], mat: List[List[int]]) -> int:
        m = len(mat)
        n = len(mat[0]) if m > 0 else 0

        # Map value -> (row, col)
        pos = {}
        for r in range(m):
            for c in range(n):
                pos[mat[r][c]] = (r, c)

        row_cnt = [0] * m
        col_cnt = [0] * n

        for i, val in enumerate(arr):
            r, c = pos[val]
            row_cnt[r] += 1
            col_cnt[c] += 1
            if row_cnt[r] == n or col_cnt[c] == m:
                return i

        # Problem guarantees an answer exists, but return -1 as fallback
        return -1
```
- Notes:
  - Approach: Precompute positions for O(1) lookup, maintain counters for each row/column, iterate arr and check after each paint.
  - Time complexity: O(m * n) to build the map + O(m * n) to process arr = O(m * n) overall.
  - Space complexity: O(m * n) for the position map + O(m + n) for counters.