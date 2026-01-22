# [Problem 1937: Maximum Number of Points with Cost](https://leetcode.com/problems/maximum-number-of-points-with-cost/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This is a DP over rows: we must pick one cell per row; picking column c in row r gives points[r][c] but we subtract distance between consecutive column choices. A naive DP dp[r][c] = points[r][c] + max_j(dp[r-1][j] - abs(c-j)) would be O(n^2) per row and too slow when n is large. But abs(c-j) structure suggests we can transform the max over j into two passes (left-to-right and right-to-left) that propagate the best possible previous value with distance penalty in O(n) per row. I recall the trick: for fixed previous row values prev[j], compute for each c the best value considering penalty by computing prefix maxima where moving one step left/right reduces value by 1.

## Refining the problem, round 2 thoughts
We can maintain prev = dp for previous row. To get the best achievable "prev - abs(c-j)" for each c:
- left-to-right: bestL[c] = max(prev[c], bestL[c-1] - 1)
- right-to-left: bestR[c] = max(prev[c], bestR[c+1] - 1)
Then bestPrev[c] = max(bestL[c], bestR[c]). New dp[c] = points[r][c] + bestPrev[c].
Initialize dp with first row values. Repeat for each subsequent row. Complexity O(m*n) time, O(n) extra space. Edge cases: n == 1 trivial but handled. Use integers; values fit in Python int.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        # rows m, cols n
        m = len(points)
        n = len(points[0])
        # dp for previous row: start with first row's points
        prev = points[0][:]  # copy

        # iterate rows 1..m-1
        for r in range(1, m):
            # compute left-to-right maxima considering -1 per step
            left = [0] * n
            left[0] = prev[0]
            for c in range(1, n):
                # either start from prev[c] or come from left[c-1] and pay 1 for moving right
                left[c] = max(prev[c], left[c-1] - 1)

            # compute right-to-left maxima
            right = [0] * n
            right[-1] = prev[-1]
            for c in range(n-2, -1, -1):
                right[c] = max(prev[c], right[c+1] - 1)

            # combine and form current dp
            curr = [0] * n
            for c in range(n):
                best_prev = left[c] if left[c] >= right[c] else right[c]
                curr[c] = points[r][c] + best_prev

            prev = curr  # reuse for next row

        # answer is max over last dp
        return max(prev)
```
- Notes:
  - Approach: dynamic programming with optimization using two directional passes to incorporate the linear penalty of distance. For each column c, we compute the best previous-row value minus distance efficiently.
  - Time complexity: O(m * n), where m is number of rows and n is number of columns (product m*n <= 1e5, so this is fine).
  - Space complexity: O(n) extra space (arrays left, right, curr; prev reused).
  - Implementation detail: using max of left and right arrays yields the best prev[j] - abs(c-j) for each c. Initialization uses the first row directly as base dp.