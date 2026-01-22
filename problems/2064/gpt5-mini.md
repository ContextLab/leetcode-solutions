# [Problem 2064: Minimized Maximum of Products Distributed to Any Store](https://leetcode.com/problems/minimized-maximum-of-products-distributed-to-any-store/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to distribute each product type to stores, but each store can hold at most one product type (though any amount of that type). For a candidate maximum x (max items any store can hold), each quantity q must be split into chunks of size at most x, so it requires ceil(q / x) stores. If the total number of required stores across all product types is <= n, x is feasible. This suggests a decision problem that can be solved by binary search on x. Lower bound is 1, upper bound is max(quantities). Check mid by summing ceil divisions and comparing to n.

## Refining the problem, round 2 thoughts
Binary search on x from 1 to max(quantities). For a mid value, compute required_stores = sum((q + mid - 1) // mid for q in quantities). If required_stores <= n, we can try smaller x (right = mid); otherwise increase x (left = mid + 1). Edge cases: when n is large compared to total required pieces, answer can be small; when n = 1, answer is sum of all? Actually with n=1 and only one store allowed, but constraint m <= n so n >= m, so n >=1 and m <= n ensures at least one store per type available in worst-case distribution? Still algorithm handles all. Complexity: O(m * log(maxQ)), space O(1).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minimizedMaximum(self, n: int, quantities: List[int]) -> int:
        left, right = 1, max(quantities)
        while left < right:
            mid = (left + right) // 2
            # compute how many stores needed if each store can take at most mid items
            required = 0
            for q in quantities:
                required += (q + mid - 1) // mid
                # early break if already exceeding n
                if required > n:
                    break
            if required <= n:
                right = mid
            else:
                left = mid + 1
        return left
```
- Notes:
  - Approach: binary search on the maximum number x allowed per store. Check feasibility by summing ceil(q / x) over quantities to get needed stores.
  - Time complexity: O(m * log M), where m = len(quantities) and M = max(quantities) (log base 2). With constraints m, M <= 1e5 this is efficient.
  - Space complexity: O(1) extra space (ignoring input).
  - Implementation detail: use integer arithmetic for ceil via (q + mid - 1) // mid and an early break when required > n to avoid extra work.