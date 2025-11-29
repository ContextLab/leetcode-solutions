# [Problem 3512: Minimum Operations to Make Array Sum Divisible by K](https://leetcode.com/problems/minimum-operations-to-make-array-sum-divisible-by-k/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The operation decreases any single element by 1. Each operation reduces the total sum by exactly 1. To make the sum divisible by k we need to reduce the sum by an amount equal to sum(nums) % k (call it r). So at first glance the minimum number of operations should be r — the remainder itself — because every operation reduces sum by one and we need to remove exactly r (mod k) from the sum.

Potential concerns: Are we allowed to keep decrementing elements below zero? The statement doesn't explicitly forbid negatives, but even if we cannot go negative, we can always distribute at most sum(nums) decrements across elements (down to zero). Note r = sum % k is strictly less than k and ≤ sum (if sum < k then r = sum), so we can always perform r decrements without needing to go below zero. Thus r operations are feasible. If r == 0 we need 0 ops.

So the answer should be sum(nums) % k.

## Refining the problem, round 2 thoughts
Edge cases:
- If sum % k == 0, return 0.
- If sum < k, sum % k == sum; we can zero out elements with exactly sum operations, which is valid.
- Large arrays or values: just summing is O(n) and fits constraints (n ≤ 1000, nums[i] ≤ 1000).

No need for complex greedy or DP. Time complexity O(n) to compute the sum, space O(1).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minOperations(self, nums: List[int], k: int) -> int:
        """
        Each decrement operation reduces the total sum by exactly 1.
        Let r = sum(nums) % k. We must reduce the sum by r (mod k) to make it divisible by k.
        Thus the minimum number of operations is r.
        """
        return sum(nums) % k
```
- Notes:
  - Approach: compute remainder r = sum(nums) % k and return r.
  - Time complexity: O(n) where n = len(nums) to compute the sum.
  - Space complexity: O(1) additional space.