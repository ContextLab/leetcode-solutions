# [Problem 1605: Find Valid Matrix Given Row and Column Sums](https://leetcode.com/problems/find-valid-matrix-given-row-and-column-sums/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This is a reconstruction problem where we know row sums and column sums and must produce any non-negative integer matrix matching those sums. The constraints guarantee a solution exists (sum(rowSum) == sum(colSum)). My first thought is a greedy, two-pointer construction: fill the matrix starting at (0,0) and for each cell, put as much as possible without exceeding the current remaining row or column sum. That suggests assigning val = min(rowSum[i], colSum[j]) to cell (i,j), subtracting it from both, and then advancing the row pointer if its sum becomes zero or the column pointer if its sum becomes zero (or both). This should maintain feasibility because we always assign only what's available for both row and column. We will end up with at most m + n - 1 non-zero entries.

## Refining the problem, round 2 thoughts
- Edge cases: rows or columns that start with 0 should be handled (we'll put zeros and advance pointers appropriately).
- Complexity: we only need to visit each row and each column pointer advancement at most once, so the greedy loop is O(m + n) after initializing the m x n zero matrix. Initializing the matrix costs O(m * n) space/time, which is fine with limits up to 500 each.
- Correctness: assigning min(rowRemain, colRemain) is safe because it doesn't consume more than either; it never creates infeasibility for remaining rows/columns because total sums remain balanced and we only reduce either a row or a column to zero at each step.
- Alternative approaches: flows or bipartite matching analogies exist, but greedy is simplest and optimal here.
- Implementation detail: produce a zeros matrix then run two-pointer greedy filling.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def restoreMatrix(self, rowSum: List[int], colSum: List[int]) -> List[List[int]]:
        m, n = len(rowSum), len(colSum)
        # initialize matrix with zeros
        ans = [[0] * n for _ in range(m)]
        
        i = 0
        j = 0
        # greedy fill: put as much as possible at ans[i][j] = min(rowSum[i], colSum[j])
        while i < m and j < n:
            val = min(rowSum[i], colSum[j])
            ans[i][j] = val
            rowSum[i] -= val
            colSum[j] -= val
            # advance pointer(s) whose remaining sum is zero
            if rowSum[i] == 0:
                i += 1
            if colSum[j] == 0:
                j += 1
        
        return ans
```
- Notes about the solution:
  - Approach: Greedy two-pointer filling. At each step assign the maximum possible non-negative integer to the current cell without violating current row/column remainders (val = min(rowRemain, colRemain)), subtract it, then advance whichever index(s) became satisfied.
  - Correctness: The greedy choice is safe because it only uses capacity available in both the current row and column. Since total sums match and we only reduce a row or a column to zero at each step, remaining sums remain consistent and the process finishes with all sums satisfied.
  - Time complexity: O(m * n) due to creating the m x n answer matrix (initialization). The greedy loop itself runs in O(m + n) steps.
  - Space complexity: O(m * n) for the output matrix. Additional space is O(1) beyond output.