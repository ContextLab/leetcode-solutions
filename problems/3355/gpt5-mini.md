# [Problem 3355: Zero Array Transformation I](https://leetcode.com/problems/zero-array-transformation-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
[I start by reading the statement: each query gives a range [l, r] and for that query we may pick any subset of indices inside [l, r] to decrement by 1. We process queries sequentially but each query is just one opportunity to decrement selected indices in its range by exactly 1. That suggests each index i can be decremented at most as many times as there are queries covering i. We need every nums[i] to become exactly 0, so each nums[i] must be achievable by choosing that index in some of the queries that cover it. Because for each query we can independently decide for each index in its range whether to decrement that index, choices for different indices in the same query don't constrain each other. So the condition seems to reduce to: for every i, nums[i] <= (# of queries that cover i). If any nums[i] is larger than its coverage count, it's impossible. Otherwise it's possible.]

## Refining the problem, round 2 thoughts
[Refine: confirm independence of indices within a query — yes, "select a subset" means we can include or exclude each index individually, so no coupling constraints across indices. So the only thing that matters per index is how many queries include it (the maximum possible decrements for that index). Implementation approach: compute coverage counts for all indices efficiently using a difference array / prefix-sum of the queries. Then check nums[i] <= coverage[i] for all i. Edge cases: large n and many queries => need O(n+q) time, O(n) extra space. If queries cover nothing (none), check zeros. If nums are 0 it's trivially OK. Complexity: build diff array in O(q), prefix sum in O(n), checks in O(n). Space O(n).]

## Attempted solution(s)
```python
from typing import List

class Solution:
    def canBeZeroArray(self, nums: List[int], queries: List[List[int]]) -> bool:
        n = len(nums)
        # Difference array for coverage counts
        diff = [0] * (n + 1)
        for l, r in queries:
            diff[l] += 1
            diff[r + 1] -= 1  # r+1 is safe because diff has length n+1

        cur = 0
        for i in range(n):
            cur += diff[i]
            # cur is number of queries that cover index i
            if nums[i] > cur:
                return False
        return True
```
- Notes:
  - Approach: use a difference array to compute for each index how many queries cover it (coverage count). For each index i, we require nums[i] <= coverage[i]. If any index requires more decrements than available queries cover it, return False; otherwise True.
  - Time complexity: O(n + q), where n = len(nums) and q = len(queries).
  - Space complexity: O(n) additional for the difference array.
  - Implementation detail: diff has length n+1 so we can safely increment at l and decrement at r+1; then a single pass prefix sum gives coverage per index.