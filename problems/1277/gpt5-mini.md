# [Problem 1277: Count Square Submatrices with All Ones](https://leetcode.com/problems/count-square-submatrices-with-all-ones/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I want to count all square submatrices consisting entirely of ones. A brute force approach would check every possible top-left corner and every possible side length and verify all entries in that square are 1 — that would be O(m * n * min(m,n)^2) in the worst case, which is too slow for 300x300.

This reminds me of a classic DP: if you know the largest square ending at the cell above, left, and top-left, you can compute the largest square ending at the current cell (when it's 1). Specifically, dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) if matrix[i][j] == 1, otherwise 0. Summing all dp values gives the total number of squares (each dp[i][j] counts how many squares have bottom-right corner at (i,j)).

Edge conditions: first row or first column have dp equal to the cell value itself. We can either keep a separate dp array or reuse the input matrix to store dp values (careful but allowed usually).

## Refining the problem, round 2 thoughts
Use the DP relation described. For space, we can either:
- Modify the input matrix in-place to store dp values (O(1) extra space).
- Or use a 1D dp array of length n (O(n) extra space) updating left-to-right while tracking previous top-left value.
Either approach yields O(m*n) time. In-place is simplest and memory-efficient; LeetCode permits mutating the input.

Consider edge cases:
- Matrix with single row or single column (dp reduces to the values).
- All zeros (answer 0).
- All ones (sum of counts of squares up to min(m,n) per possible bottom-right).

Time complexity: O(m*n).
Space complexity: O(1) extra if in-place, otherwise O(n) for 1D dp or O(m*n) for full dp.

## Attempted solution(s)
```python
class Solution:
    def countSquares(self, matrix: list[list[int]]) -> int:
        if not matrix or not matrix[0]:
            return 0

        m, n = len(matrix), len(matrix[0])
        total = 0

        # Modify matrix in-place to hold dp values:
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == 1:
                    if i == 0 or j == 0:
                        # first row or first column: only 1x1 square possible here
                        total += 1
                    else:
                        # dp recurrence using neighbors (they may already have dp values)
                        matrix[i][j] = min(
                            matrix[i-1][j],
                            matrix[i][j-1],
                            matrix[i-1][j-1]
                        ) + 1
                        total += matrix[i][j]
                # if matrix[i][j] == 0, it contributes nothing and stays 0
        return total
```
- Approach: dynamic programming using the observation that if cell (i,j) is 1, the largest all-ones square ending at (i,j) equals 1 plus the minimum of largest squares ending at above, left, and top-left neighbors. Sum all dp values to count all squares.
- Time complexity: O(m * n), where m and n are matrix dimensions.
- Space complexity: O(1) extra (we modify the input matrix in-place to store dp values). If you prefer not to modify input, use a separate dp array (O(n) or O(m*n) space).