# [Problem 3418: Maximum Amount of Money Robot Can Earn](https://leetcode.com/problems/maximum-amount-of-money-robot-can-earn/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the maximum sum along a monotone (right/down) path from top-left to bottom-right, but with the twist that up to 2 negative cells (robbers) encountered can be "neutralized" (treated as 0 instead of subtracting). This looks like a dynamic programming on the grid with an extra dimension for how many neutralizations have been used (0, 1, 2). At each cell we can come from top or left; if the cell value is non-negative, we always add it; if negative, we have two choices: accept the negative (add it) or use one neutralization (if we still have quota) and add 0 instead. So a DP state dp[i][j][k] = best profit arriving at (i,j) having used exactly k neutralizations seems natural. We take the maximum of dp[m-1][n-1][0..2] at the end.

Memory/time look manageable: m,n up to 500 -> 500*500*3 states, transitions O(1) each → ~750k states, fine.

## Refining the problem, round 2 thoughts
- State details: dp dimensions m x n x 3 (k = 0..2). Initialize with very negative values. Carefully handle the start cell: if it's negative we can either not neutralize (dp[0][0][0] = value) or neutralize (dp[0][0][1] = 0).
- For each other cell, for each k:
  - From previous dp with same k (top or left) we can move and if cell >= 0 add value, if cell < 0 add value (not neutralizing).
  - If cell < 0 and k > 0, we can also come from previous with k-1 and "spend" a neutralization -> add 0.
- We don't need to model intentionally "wasting" a neutralization on a non-negative cell; there's never a benefit to reduce the number of available neutralizations without using them on negatives.
- Edge cases: cells with no valid incoming path will remain -inf; ensure boundaries handled.
- Complexity: O(m * n * K) with K=3 -> O(mn) time, O(mn) memory. Memory can be reduced to two rows if needed.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxCoins(self, coins: List[List[int]]) -> int:
        m = len(coins)
        n = len(coins[0])
        NEG_INF = -10**18
        
        # dp[i][j][k] = max profit at (i,j) having used exactly k neutralizations (k in {0,1,2})
        dp = [[[NEG_INF]*3 for _ in range(n)] for __ in range(m)]
        
        v0 = coins[0][0]
        # starting cell: either take its value or neutralize if negative
        if v0 >= 0:
            dp[0][0][0] = v0
        else:
            dp[0][0][0] = v0        # not neutralized
            dp[0][0][1] = 0         # neutralized here (used 1)
        
        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    continue
                v = coins[i][j]
                for k in range(3):
                    # come from top/left without changing neutralization count
                    best_prev_same_k = NEG_INF
                    if i > 0:
                        best_prev_same_k = max(best_prev_same_k, dp[i-1][j][k])
                    if j > 0:
                        best_prev_same_k = max(best_prev_same_k, dp[i][j-1][k])
                    if best_prev_same_k != NEG_INF:
                        # if non-negative, add v; if negative and not neutralizing, add v (may reduce total)
                        dp[i][j][k] = max(dp[i][j][k], best_prev_same_k + v)
                    
                    # if v is negative and we have k>0, we could neutralize this cell,
                    # coming from a state that used k-1 neutralizations
                    if v < 0 and k > 0:
                        best_prev_k_minus_1 = NEG_INF
                        if i > 0:
                            best_prev_k_minus_1 = max(best_prev_k_minus_1, dp[i-1][j][k-1])
                        if j > 0:
                            best_prev_k_minus_1 = max(best_prev_k_minus_1, dp[i][j-1][k-1])
                        if best_prev_k_minus_1 != NEG_INF:
                            # neutralize here -> add 0
                            dp[i][j][k] = max(dp[i][j][k], best_prev_k_minus_1)
        
        ans = max(dp[m-1][n-1])
        return ans
```
- Notes:
  - We used a 3D DP where the third dimension counts exactly how many neutralizations were used; at the end we take the best among 0, 1, or 2 used.
  - Time complexity: O(m * n * 3) = O(m * n).
  - Space complexity: O(m * n * 3). This can be reduced to O(n * 3) by rolling rows if needed.
  - We use a large negative sentinel (NEG_INF) to represent unreachable states.
  - We do not model wasting neutralizations on non-negative cells because doing so can never improve the final result — keeping neutralizations available is always at least as good.