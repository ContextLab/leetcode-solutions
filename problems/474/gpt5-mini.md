# [Problem 474: Ones and Zeroes](https://leetcode.com/problems/ones-and-zeroes/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This looks like a knapsack variant: each string has a "cost" in zeros and ones, and we want the maximum number of items (strings) we can pick without exceeding m zeros and n ones. Each string is either taken or not (0/1 choice), so it maps to 0/1 knapsack with two capacity dimensions. A dynamic programming approach fits: dp[i][j] = maximum number of strings using at most i zeros and j ones. Brute-force subsets is exponential and infeasible for up to 600 strings.

## Refining the problem, round 2 thoughts
We can compute the zeros and ones count for each string first. For DP we can either use a 3D DP over index and capacities, or a 2D DP updated per string (like typical space-optimized knapsack). To avoid reusing the same string multiple times, iterate capacities in reverse (from m downwards and n downwards). Edge cases: strings that individually require more zeros or ones than capacity — those won't be used. Time complexity will be O(L * m * n) where L = len(strs), which is fine given constraints (L ≤ 600, m,n ≤ 100). Space can be O(m * n) using the optimized 2D DP.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def findMaxForm(self, strs: List[str], m: int, n: int) -> int:
        # dp[i][j] = max number of strings using at most i zeros and j ones
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for s in strs:
            zeros = s.count('0')
            ones = s.count('1')
            # If a string individually exceeds capacity, skip updates for impossible states.
            # Iterate in reverse to ensure each string is used at most once (0/1 knapsack).
            if zeros > m or ones > n:
                # Still okay to skip; it can't fit in any capacity.
                continue
            for i in range(m, zeros - 1, -1):
                for j in range(n, ones - 1, -1):
                    dp[i][j] = max(dp[i][j], dp[i - zeros][j - ones] + 1)
        
        return dp[m][n]
```
- Notes:
  - Approach: 2D dynamic programming (space-optimized 0/1 knapsack across two dimensions).
  - Time complexity: O(L * m * n), where L = len(strs). For each string we update up to (m+1)*(n+1) states.
  - Space complexity: O(m * n) for the dp table.
  - Implementation detail: iterate capacities in reverse to prevent reusing the same string multiple times. Strings that require more zeros or ones than available are skipped.