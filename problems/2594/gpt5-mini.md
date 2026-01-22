# [Problem 2594: Minimum Time to Repair Cars](https://leetcode.com/problems/minimum-time-to-repair-cars/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the minimum time T such that all cars can be repaired when mechanics work simultaneously. For a mechanic of rank r, if they repair n cars it takes r * n^2 minutes, so given a time T the maximum cars that mechanic can finish is the largest n with r * n^2 <= T, i.e. n = floor(sqrt(T / r)). That suggests a decision problem: for a candidate time T, compute total cars fixable = sum floor(sqrt(T / r_i)) and check if >= cars. The decision function is monotonic in T, so binary search on T is natural. Need careful integer sqrt and bounds for T.

## Refining the problem, round 2 thoughts
Choose a search range: lower bound can be 1, upper bound can be min(ranks) * cars^2 (putting all cars to the fastest mechanic). That's safe and not too large for Python integers. For each mid T, sum math.isqrt(T // r) for each r (using integer division then integer sqrt avoids floating precision). Early break when sum >= cars to speed up. Complexity: O(n log U) where U ~ min_rank * cars^2. With constraints n <= 1e5 and cars <= 1e6, log U ~ ~40, so it's fine. Edge cases: ranks values >=1 so division safe; when T < r, T // r == 0, isqrt(0) == 0, so fine.

## Attempted solution(s)
```python
import math
from typing import List

class Solution:
    def repairCars(self, ranks: List[int], cars: int) -> int:
        # Binary search on time
        lo = 1
        lo_rank = min(ranks)
        hi = lo_rank * cars * cars  # worst-case: fastest mechanic fixes all cars
        
        while lo < hi:
            mid = (lo + hi) // 2
            total = 0
            # count how many cars can be repaired in 'mid' minutes
            for r in ranks:
                # max n such that r * n^2 <= mid  ->  n <= sqrt(mid / r)
                total += math.isqrt(mid // r)
                if total >= cars:
                    break
            if total >= cars:
                hi = mid
            else:
                lo = mid + 1
        return lo
```
- Approach: Binary search the minimum time T such that sum floor(sqrt(T / r_i)) >= cars. Use integer arithmetic (mid // r and math.isqrt) to avoid floating-point errors.
- Time complexity: O(n * log U) where U = min(ranks) * cars^2 (log U ~ up to ~40). With n up to 1e5, this is efficient.
- Space complexity: O(1) extra space (ignoring input).