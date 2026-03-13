# [Problem 3296: Minimum Number of Seconds to Make Mountain Height Zero](https://leetcode.com/problems/minimum-number-of-seconds-to-make-mountain-height-zero/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to distribute mountainHeight units of "work" among workers. If worker i does x units, their time is workerTimes[i] * (1 + 2 + ... + x) = workerTimes[i] * x*(x+1)/2. Workers operate simultaneously, so the total time is the maximum time any worker spends; we want to minimize that maximum subject to sum x_i = mountainHeight. This looks like a feasibility check: for a given time T, each worker can do at most k_i units where workerTimes[i] * k_i*(k_i+1)/2 <= T. If sum k_i >= mountainHeight, T is feasible. So binary search on T is natural. Need to compute k_i efficiently (solve quadratic or use integer math). Watch out for large numbers (T up to ~5e15), use integer sqrt (math.isqrt) to avoid floating point error.

## Refining the problem, round 2 thoughts
- For a candidate T, compute M = 2*T // workerTimes[i], solve k^2 + k <= M => k = floor((-1 + sqrt(1 + 4*M))/2). Using integer math (math.isqrt) is safe and exact.
- Early exit the capacity sum when it reaches mountainHeight.
- Binary search bounds: low = 0, high = max(workerTime) * mountainHeight*(mountainHeight+1)//2 (one worker does everything) — fits in 64-bit integer for given constraints.
- Complexity: O(n * log(maxT)). With n <= 1e4 and log(maxT) ~ ~52, this is fine.
- Edge cases: single worker, many workers faster than needed (sum capacities exceed height quickly), and very large workerTimes produce small capacities for given T.

## Attempted solution(s)
```python
import math
from typing import List

class Solution:
    def minimumTime(self, mountainHeight: int, workerTimes: List[int]) -> int:
        # Helper: given time T, compute total units of height workers can reduce
        def capacity(T: int) -> int:
            total = 0
            for w in workerTimes:
                if T < w:  # can't even do 1 unit
                    continue
                # Solve k*(k+1)/2 * w <= T  => k^2 + k <= 2*T//w (use integer division)
                M = (2 * T) // w
                # discriminant for k^2 + k - M <= 0 is 1 + 4*M
                d = 1 + 4 * M
                sqrt_d = math.isqrt(d)
                k = (sqrt_d - 1) // 2
                total += k
                if total >= mountainHeight:
                    return total
            return total

        # Binary search on time T
        lo = 0
        # Upper bound: slowest single worker doing all mountainHeight
        max_w = max(workerTimes)
        hi = max_w * mountainHeight * (mountainHeight + 1) // 2

        while lo < hi:
            mid = (lo + hi) // 2
            if capacity(mid) >= mountainHeight:
                hi = mid
            else:
                lo = mid + 1
        return lo
```
- Notes about the solution:
  - Approach: binary search on time T; for each T compute how many units each worker can remove using integer solution of quadratic inequality.
  - Time complexity: O(n * log U) where U is the search space upper bound (roughly max worker time * H*(H+1)/2). With constraints this is efficient (n ≤ 1e4, log U ≲ 60).
  - Space complexity: O(1) extra space (besides input).
  - Implementation detail: use math.isqrt on integer discriminant to avoid floating-point inaccuracies and ensure correctness for large values. Early exit when accumulated capacity reaches mountainHeight to save work.