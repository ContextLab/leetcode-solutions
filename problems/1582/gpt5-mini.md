# [Problem 1582: Special Positions in a Binary Matrix](https://leetcode.com/problems/special-positions-in-a-binary-matrix/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to count positions (i, j) where mat[i][j] == 1 and every other element in row i and column j is 0. The brute force way would be: for every 1, scan its entire row and column to verify there are no other 1s — that would be O(m + n) work per 1 and in worst case O(mn(m+n)), which is unnecessary for constraints up to 100x100 but still suboptimal.

A common pattern: precompute the count of 1s in each row and each column. If a cell is 1 and its row-count == 1 and its col-count == 1, it's special. That gives a single pass to compute counts and another pass to count special positions — overall O(mn) time.

## Refining the problem, round 2 thoughts
- Edge cases: all zeros -> answer 0. All ones -> usually 0 unless matrix is 1x1.
- Precomputing row and column sums is straightforward and stable.
- Space: need O(m + n) extra space for the counts, which is fine for m,n <= 100.
- Alternative in-place trick: you could encode counts into existing matrix to save auxiliary space, but it's unnecessary here and less clear.
- Complexity: two passes over the matrix -> O(mn) time, O(m + n) extra space.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def numSpecial(self, mat: List[List[int]]) -> int:
        if not mat or not mat[0]:
            return 0
        m, n = len(mat), len(mat[0])
        # Compute row counts
        row_count = [sum(row) for row in mat]
        # Compute column counts
        col_count = [0] * n
        for j in range(n):
            s = 0
            for i in range(m):
                s += mat[i][j]
            col_count[j] = s

        # Count special positions
        ans = 0
        for i in range(m):
            for j in range(n):
                if mat[i][j] == 1 and row_count[i] == 1 and col_count[j] == 1:
                    ans += 1
        return ans
```
- Notes:
  - Approach: precompute number of 1s in each row and column, then count cells where mat[i][j] == 1 and both corresponding counts are exactly 1.
  - Time complexity: O(m * n) — one pass to compute row counts (O(mn) inside sum across rows) and one pass for column counts (O(mn)), plus final check pass (O(mn)).
  - Space complexity: O(m + n) for row_count and col_count arrays.
  - Implementation detail: using Python's sum(row) for rows is concise; columns computed by iterating rows for each column is clear and efficient for given constraints.