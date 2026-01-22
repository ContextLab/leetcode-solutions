# [Problem 1751: Maximum Number of Events That Can Be Attended II](https://leetcode.com/problems/maximum-number-of-events-that-can-be-attended-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to pick up to k non-overlapping events (end day inclusive) to maximize sum of values. This is like weighted interval scheduling but with a limit k on how many intervals we can take. A typical approach for weighted interval scheduling is sorting by start (or end) day and using binary search to find the next compatible event, then dynamic programming (either recursion+memo or iterative DP). Because k * n <= 1e6 (given), an O(n*k) DP is feasible.

We need to be careful about the "inclusive end" rule: if an event ends on day d, the next event must start at day > d (not >=). So when finding the next compatible event's index we should bisect for first start > end.

A straightforward DP: sort events by start, precompute next_index for each event (index of first event with start > current end). Then dp[i][j] = maximum value achievable starting from event i when allowed to attend up to j events. Recurrence:
- skip current event: dp[i+1][j]
- take current event (if j>0): value[i] + dp[next_index[i]][j-1]
Take max. Compute bottom-up from i=n-1..0, j=1..k. Answer is dp[0][k].

## Refining the problem, round 2 thoughts
Edge cases:
- k could be >= number of events; still DP handles it.
- Inclusive end handled by bisect_right (first start > end).
- Memory: dp table size (n+1)*(k+1) is safe because problem constraint gives k*n <= 1e6.
- Time: sort O(n log n), precompute next indices O(n log n), DP O(n*k). All acceptable under constraints.

Alternative: top-down memoized recursion with binary search for next index; same complexity but iterative DP is simple and avoids recursion depth concerns.

I'll implement iterative bottom-up DP with precomputed next indices using bisect_right.

## Attempted solution(s)
```python
from bisect import bisect_right
from typing import List

class Solution:
    def maxValue(self, events: List[List[int]], k: int) -> int:
        # Sort events by start day
        events.sort(key=lambda x: x[0])
        n = len(events)
        starts = [e[0] for e in events]
        
        # Precompute next index for each event: first event with start > events[i].end
        next_idx = [0] * n
        for i in range(n):
            end_i = events[i][1]
            # need start > end_i, so bisect_right on starts with end_i
            next_idx[i] = bisect_right(starts, end_i)
        
        # DP table: dp[i][j] = max value using events[i:] with at most j events
        # dimensions (n+1) x (k+1), initialized to 0
        dp = [[0] * (k + 1) for _ in range(n + 1)]
        
        # Fill DP bottom-up
        for i in range(n - 1, -1, -1):
            val = events[i][2]
            ni = next_idx[i]
            for j in range(1, k + 1):
                # Option 1: skip current event
                skip = dp[i + 1][j]
                # Option 2: take current event (if we have quota j)
                take = val + dp[ni][j - 1]
                dp[i][j] = max(skip, take)
            # dp[i][0] stays 0 (can't take any events)
        
        return dp[0][k]
```
- Notes on approach:
  - Sort events by start day to allow binary searching the next compatible event.
  - next_idx uses bisect_right because end day is inclusive; next event must have start > end.
  - Bottom-up DP over events and remaining picks yields O(n*k) time for the DP part.
- Complexity:
  - Time: O(n log n) for sorting + O(n log n) for computing next indices (bisect) + O(n * k) for DP -> overall O(n log n + n * k).
  - Space: O(n * k) for DP table plus O(n) for starts and next_idx -> O(n * k). This fits constraints because k * n <= 1e6.