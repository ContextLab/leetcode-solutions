# [Problem 73: Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to set entire rows and columns to zero when any element in them is zero. The naive way is to record which rows and columns must be zeroed (two sets) and then do another pass to zero them — that uses O(m + n) space, which is acceptable but the follow-up asks for constant space. Can I reuse the matrix itself to store the markers? Yes: use the first row and first column as marker storage for which rows/columns to zero. But I must remember whether the first row/first column themselves originally had any zeros so I can zero them at the end if needed. Also be careful to avoid prematurely overwriting markers when scanning. Overall approach: two passes — first pass mark in first row/col, second pass zero based on those markers, then handle the first row/col separately.

## Refining the problem, round 2 thoughts
Edge cases:
- Single row or single column
- Matrix with zero in (0,0) — this affects both first row and first column flags
- Negative values and zero values; only zero matters

Algorithm:
1. Determine if first row has any zero (first_row_zero) and if first column has any zero (first_col_zero).
2. Use the rest of the matrix (i from 1..m-1, j from 1..n-1) to set matrix[i][0] = 0 and matrix[0][j] = 0 when matrix[i][j] == 0.
3. Use those markers to set matrix cells to 0 for i from 1..m-1, j from 1..n-1.
4. Finally zero first row if first_row_zero, and first column if first_col_zero.

Time complexity: O(m * n).
Space complexity: O(1) extra space (apart from input).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        if not matrix or not matrix[0]:
            return

        m, n = len(matrix), len(matrix[0])

        # Check if first row has any zero
        first_row_zero = any(matrix[0][j] == 0 for j in range(n))
        # Check if first column has any zero
        first_col_zero = any(matrix[i][0] == 0 for i in range(m))

        # Use first row and first column as markers for rows and columns to be zeroed
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0

        # Zero cells based on markers in first row and first column
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0

        # Zero the first row if needed
        if first_row_zero:
            for j in range(n):
                matrix[0][j] = 0

        # Zero the first column if needed
        if first_col_zero:
            for i in range(m):
                matrix[i][0] = 0
```
- Notes:
  - This solution uses the first row and first column of the matrix itself to store which rows and columns should be zeroed, avoiding extra arrays or sets.
  - Time complexity: O(m * n) — we scan the matrix a constant number of times.
  - Space complexity: O(1) extra space (only a couple of boolean flags).
  - Important implementation detail: we must record whether the first row/column originally contained a zero before using them as markers. We also must avoid using the first row/column as markers while scanning them for zeros (hence scanning starts from index 1 for marker-setting and zeroing phases).