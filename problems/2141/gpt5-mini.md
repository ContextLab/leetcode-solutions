# [Problem 2141: Maximum Running Time of N Computers](https://leetcode.com/problems/maximum-running-time-of-n-computers/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to run n computers simultaneously using batteries, can swap batteries any time. Initially one battery per computer but later can move batteries around. The resources are battery minutes. If I want to run all n computers for T minutes, each computer needs T minutes of battery time, so total required is n*T minutes. Each battery can contribute at most its capacity, but because a single battery can't power more than one computer at the same time, when checking for feasibility of T we should cap each battery contribution at T (a battery of size > T can't contribute more than T simultaneous-minutes toward the "per-computer T" objective). So a necessary condition: sum(min(b_i, T)) >= n*T. Is it sufficient? Intuitively yes: we can slice battery minutes arbitrarily in integer minutes and reassign; if total capped contribution suffices, we can schedule to reach T. That suggests binary searching on T.

Alternate naive approach: sort descending and greedily allocate largest batteries to computers then use remaining to extend times — but reasoning is cleaner with binary search on time and the sum(min(b_i, T)) check.

Constraints: up to 1e5 batteries with capacities up to 1e9, sums up to ~1e14 -> Python int fine. Binary search upper bound can be sum(batteries)//n because that's maximum average minutes per computer.

## Refining the problem, round 2 thoughts
Binary search T in range [0, sum(batteries)//n]. For each mid, compute total = sum(min(b, mid) for b in batteries). If total >= mid * n, mid is feasible; otherwise not. Use upper-mid bias (mid = (lo+hi+1)//2) to avoid infinite loop. Time complexity: O(m * log S) where m = len(batteries) and S is sum(batteries)//n (log S <= ~60). Space O(1).

Edge cases:
- n equals number of batteries (still works).
- Some batteries very large; capping by mid handles it.
- Very small batteries many of them; summing still fine.

This check is both necessary and sufficient because we can always split battery minutes across computers via swaps; capping per battery at T captures the fact a single battery cannot contribute more than T simultaneous minutes to the n computers' run of length T.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxRunTime(self, n: int, batteries: List[int]) -> int:
        # Upper bound: average minutes available per computer
        total_minutes = sum(batteries)
        hi = total_minutes // n
        lo = 0

        # helper to test feasibility of running for t minutes
        def can_run(t: int) -> bool:
            # sum of contributions capped at t per battery
            s = 0
            for b in batteries:
                # early break if already enough to save work
                if s >= t * n:
                    return True
                s += b if b <= t else t
            return s >= t * n

        # binary search for maximum feasible t
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if can_run(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
```
- Notes:
  - Approach: binary search on T with feasibility check sum(min(b_i, T)) >= n*T.
  - Time complexity: O(m * log S) where m = len(batteries) and S = sum(batteries)//n (log S is small; in practice <= ~60). More concretely O(m * log(total_minutes/n)).
  - Space complexity: O(1) extra space.
  - Implementation details: early exit in can_run if running sum already reaches required threshold to avoid iterating whole array unnecessarily for larger T.