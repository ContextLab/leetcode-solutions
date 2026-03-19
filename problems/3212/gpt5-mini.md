# [Problem 3212: Count Submatrices With Equal Frequency of X and Y](https://leetcode.com/problems/count-submatrices-with-equal-frequency-of-x-and-y/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to count submatrices that (1) contain grid[0][0], (2) have equal counts of 'X' and 'Y', and (3) contain at least one 'X'. "Contain grid[0][0]" means the submatrix must include the cell (0,0). For a submatrix (contiguous rows and columns) to include (0,0) and be valid indices, its top row and left column must be 0. So every valid submatrix is actually a prefix submatrix anchored at (0,0) with some bottom-right corner (i, j). That simplifies the problem: we only need to check the rectangle from (0,0) to (i,j) for all i, j.

So for each cell (i,j) compute the counts of 'X' and 'Y' in the prefix rectangle (0,0)-(i,j). Count how many such prefixes have countX == countY and countX >= 1.

We can compute prefix counts efficiently with a per-row running sum plus adding the previous-row prefix sums, keeping only O(n) space.

## Refining the problem, round 2 thoughts
- Because top-left is fixed to (0,0), there are m * n candidate submatrices only, so an O(m * n) solution is ideal and easy to achieve.
- Compute prefix counts for 'X' and 'Y' for each (i, j) using running row sums plus previous-row prefix totals.
- Edge cases:
  - All dots ('.'): equal counts (0 == 0) but must have at least one 'X' — so answer should be 0.
  - Very large grid up to 1000x1000: O(mn) time and O(n) extra space is fine.
- No need for hashing or complicated transforms.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def countSubmatrices(self, grid: List[List[str]]) -> int:
        """
        Count prefix submatrices anchored at (0,0) whose counts of 'X' and 'Y' are equal
        and contain at least one 'X'.
        """
        if not grid or not grid[0]:
            return 0
        m, n = len(grid), len(grid[0])
        # prevX[j] and prevY[j] store the prefix sums for rows 0..i-1 and cols 0..j
        prevX = [0] * n
        prevY = [0] * n
        ans = 0

        for i in range(m):
            runningX = 0
            runningY = 0
            prefX = [0] * n
            prefY = [0] * n
            for j in range(n):
                ch = grid[i][j]
                if ch == 'X':
                    runningX += 1
                elif ch == 'Y':
                    runningY += 1
                # prefix up to (i, j) = running sum in current row up to j + prefix of rows above up to j
                prefX[j] = runningX + (prevX[j] if i > 0 else 0)
                prefY[j] = runningY + (prevY[j] if i > 0 else 0)
                # check conditions: equal counts and at least one X
                if prefX[j] == prefY[j] and prefX[j] > 0:
                    ans += 1
            prevX = prefX
            prevY = prefY

        return ans
```
- Notes:
  - We exploit that any submatrix containing (0,0) must be the prefix (0,0)-(i,j).
  - For each row i we maintain runningX and runningY (row cumulative sums up to column j). Adding prevX[j] / prevY[j] (sums from earlier rows up to col j) yields full prefix sums.
  - Time complexity: O(m * n) where m and n are grid dimensions.
  - Space complexity: O(n) extra space (two arrays prevX and prevY of length n, and O(n) temporary arrays prefX/prefY per row).