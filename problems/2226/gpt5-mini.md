# [Problem 2226: Maximum Candies Allocated to K Children](https://leetcode.com/problems/maximum-candies-allocated-to-k-children/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have piles, can split a pile into sub-piles but cannot merge piles. Each child must get candies from exactly one pile (i.e., a sub-pile), and all children must get the same number x. For a candidate x, each pile of size c can contribute floor(c / x) such sub-piles. We need to know if sum(floor(c / x)) >= k. That check is monotonic in x (if x is feasible, any smaller x is feasible), so we can binary search on x (the number of candies per child). Upper bound for x is max(candies), lower bound 1 (but answer may be 0 if total candies < k). So binary search for largest feasible x.

## Refining the problem, round 2 thoughts
- Edge case: if total candies < k, no positive x is possible; result should be 0. The binary search will naturally return 0 if no x >= 1 is feasible, but we can also short-circuit by checking total < k.
- Performance: candies length up to 1e5 and max value up to 1e7, k up to 1e12. Binary search over values up to 1e7 gives about 24 iterations; each iteration sums over up to 1e5 piles — acceptable.
- Implementation detail: while summing counts for a mid, break early once count >= k to save work.
- Complexity: O(n log M) time (M = max(candies)), O(1) extra space.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maximumCandies(self, candies: List[int], k: int) -> int:
        if not candies:
            return 0
        # Optional quick check: if total candies < k, can't give at least 1 to each child
        if sum(candies) < k:
            return 0

        left, right = 1, max(candies)
        ans = 0

        while left <= right:
            mid = (left + right) // 2
            # Count how many pieces of size mid we can get
            count = 0
            for c in candies:
                count += c // mid
                if count >= k:
                    break

            if count >= k:
                ans = mid  # mid is feasible, try larger
                left = mid + 1
            else:
                right = mid - 1

        return ans
```
- Solution approach: Binary search on the answer x (candies per child). For each candidate x, compute total sub-piles sum(c // x) and check if >= k. Use early termination when the count reaches k.
- Time complexity: O(n log M) where n = len(candies) and M = max(candies). Space complexity: O(1) extra space.