# [Problem 983: Minimum Cost For Tickets](https://leetcode.com/problems/minimum-cost-for-tickets/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I recognize this as a dynamic programming problem: on any travel day, you can choose one of three ticket options and each covers a range of future days. A greedy approach (always pick cheapest per-day) can fail because longer passes may be better when several travel days cluster. Two common DP formulations come to mind:
- DP indexed by calendar day (1..365): dp[d] = min cost to cover all travel up to day d. If d is not a travel day, dp[d] = dp[d-1]; otherwise consider dp[d-1] + cost1, dp[d-7] + cost7, dp[d-30] + cost30.
- DP by travel-day index: dp[i] = min cost to cover travel days[i..end], using binary search to skip to the first day not covered by a chosen pass.

Calendar-day DP is straightforward and easy to implement (fixed 365 iterations). Travel-index DP is slightly faster if days array is sparse (O(n log n) with binary search) but not necessary given small fixed year length.

Edge cases: travel includes day 1 (avoid negative indices), days near start when considering 7- or 30-day passes.

## Refining the problem, round 2 thoughts
I'll implement the calendar-day DP for clarity and simplicity: dp size 366 with dp[0] = 0. Use a set for O(1) membership check of travel days. For each day d from 1..365:
- if d not in travel set => dp[d] = dp[d-1]
- else dp[d] = min(dp[d-1] + costs[0], dp[max(0, d-7)] + costs[1], dp[max(0, d-30)] + costs[2])

Time complexity O(365) (constant), space O(366) => effectively O(1). Alternatively, iterating only over travel days and using indices with binary search would be O(n log n) and use O(n) space; both are acceptable but calendar DP is simplest.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def mincostTickets(self, days: List[int], costs: List[int]) -> int:
        # Use DP over calendar days 1..365
        travel = set(days)
        last_day = 365  # constraints allow up to 365
        dp = [0] * (last_day + 1)  # dp[d] = min cost to cover travel up to day d
        
        for d in range(1, last_day + 1):
            if d not in travel:
                dp[d] = dp[d-1]
            else:
                cost1 = dp[d-1] + costs[0]
                cost7 = dp[max(0, d-7)] + costs[1]
                cost30 = dp[max(0, d-30)] + costs[2]
                dp[d] = min(cost1, cost7, cost30)
        
        return dp[last_day]
```
- Notes:
  - Approach: dynamic programming over calendar days with set lookup for travel days.
  - Time complexity: O(365) = O(1) in practice; more generally O(max_day) where max_day <= 365.
  - Space complexity: O(365) = O(1) auxiliary (dp array).
  - Implementation detail: using max(0, d-7) and max(0, d-30) avoids negative indices and naturally handles passes bought at the start of the year.