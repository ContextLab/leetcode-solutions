# [Problem 3010: Divide an Array Into Subarrays With Minimum Cost I](https://leetcode.com/problems/divide-an-array-into-subarrays-with-minimum-cost-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We must split the array nums into exactly 3 contiguous nonempty subarrays. The cost of a subarray is its first element. Since the first subarray always starts at index 0, its cost is nums[0] and is constant. So the task reduces to choosing two cut points that determine the start indices of the 2nd and 3rd subarrays (call them a and b with 1 <= a < b <= n-1) and minimizing nums[a] + nums[b]. That is, pick two indices a < b in [1..n-1] to minimize the sum of their values. This suggests a simple linear scan keeping the minimum seen so far for the first cut and trying every possible position for the second cut.

## Refining the problem, round 2 thoughts
We need to ensure nonempty segments, so the valid starts for the 2nd and 3rd segments are indices a and b satisfying 1 <= a < b <= n-1. For each candidate b (start of 3rd segment), the optimal a is the index with the smallest nums value among indices 1..b-1. So we can iterate b from 2 to n-1, maintain prefix_min = min(nums[1..b-1]) and compute candidate = nums[0] + prefix_min + nums[b], taking the minimum over b. This is O(n) time and O(1) extra space. Edge case n=3 produces exactly one candidate (a=1, b=2).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minCost(self, nums: List[int]) -> int:
        n = len(nums)
        # nums[0] is fixed as the cost of the first subarray
        base = nums[0]
        # prefix_min is minimum value of nums[a] for a in [1..b-1]
        prefix_min = float('inf')
        ans = float('inf')
        # b is start index of third subarray, must be at least 2 and at most n-1
        for b in range(2, n):
            # update prefix_min with possible a = b-1
            prefix_min = min(prefix_min, nums[b-1])
            # compute total cost if we split with second subarray starting at index of prefix_min
            ans = min(ans, base + prefix_min + nums[b])
        return ans
```
- Notes:
  - Approach: iterate b (start of 3rd subarray) and maintain the minimum nums[a] over valid a < b to compute the minimal nums[a] + nums[b]. Add nums[0] as constant.
  - Time complexity: O(n), single pass.
  - Space complexity: O(1) extra space (ignoring input).
  - Correctness: enforces nonempty segments by iterating b from 2 to n-1 and using a from [1..b-1].