# [Problem 2536: Increment Submatrices by One](https://leetcode.com/problems/increment-submatrices-by-one/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem asks to apply many range-add operations on submatrices of an n x n zero matrix. The naive approach (for each query, loop over all cells in the submatrix and increment) could be O(n^2) per query and will be too slow when n is up to 500 and queries up to 10^4.

This looks like a classic use-case for a 2D difference array (2D prefix-sum trick): record 4 corner updates per query and then convert the difference array to the final matrix via prefix sums. That should reduce the updates to O(1) per query and O(n^2) to build the final matrix.

## Refining the problem, round 2 thoughts
Use a (n+1) x (n+1) difference array diff initialized to zero. For a query [r1, c1, r2, c2] do:
- diff[r1][c1] += 1
- diff[r1][c2+1] -= 1
- diff[r2+1][c1] -= 1
- diff[r2+1][c2+1] += 1

Because r2+1 and c2+1 can equal n, diff must be sized n+1 to safely index up to n. After applying all queries, compute prefix sums to recover the matrix values. One safe way: first do horizontal prefix (row-wise) for columns 0..n-1, then vertical prefix (column-wise) for rows 0..n-1. The final mat[i][j] will be diff[i][j] for 0 <= i,j < n.

Edge cases: queries may touch the border (r2 or c2 == n-1), but using n+1 depth handles that. Complexity: O(q + n^2) time, O(n^2) space.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def rangeAddQueries(self, n: int, queries: List[List[int]]) -> List[List[int]]:
        # difference array with extra row and column
        diff = [[0] * (n + 1) for _ in range(n + 1)]
        
        # apply 4-corner updates for each query
        for r1, c1, r2, c2 in queries:
            diff[r1][c1] += 1
            diff[r1][c2 + 1] -= 1
            diff[r2 + 1][c1] -= 1
            diff[r2 + 1][c2 + 1] += 1
        
        # build horizontal prefix sums for first n columns
        for i in range(n):
            for j in range(1, n):
                diff[i][j] += diff[i][j - 1]
        
        # build vertical prefix sums for first n rows
        for j in range(n):
            for i in range(1, n):
                diff[i][j] += diff[i - 1][j]
        
        # extract resulting n x n matrix
        return [[diff[i][j] for j in range(n)] for i in range(n)]
```
- Notes:
  - Approach: 2D difference array (size (n+1)x(n+1)) with O(1) update per query, then 2 passes of prefix sums to recover values.
  - Time complexity: O(q + n^2) where q = number of queries. Each query does O(1) work; the final prefix and extraction over n x n cells is O(n^2).
  - Space complexity: O(n^2) for the (n+1) x (n+1) diff array (dominant).
  - Implementation details: Using n+1 size avoids boundary checks when updating at r2+1 or c2+1; only the first n rows and columns are used when computing the final matrix.