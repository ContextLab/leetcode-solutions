# [Problem 3689: Maximum Total Subarray Value I](https://leetcode.com/problems/maximum-total-subarray-value-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
At first glance this looks like a complicated selection problem: choose exactly k subarrays (they can overlap and even be identical) to maximize the sum of (max - min) for each chosen subarray. My immediate thought was to consider DP or some greedy/interval reasoning — maybe try to find k best disjoint subarrays or something like that. But then I noticed subarrays may overlap and can be repeated; that makes it possible to pick the same best-scoring subarray multiple times. So the problem reduces to finding the single subarray with the largest (max - min) value, then take it k times.

What is the maximum possible value of a subarray? It cannot exceed global_max - global_min (the max and min of the whole array). And there always exists some subarray that attains that: any subarray that contains at least one global maximum element and at least one global minimum element. Therefore the best single-subarray value equals (global_max - global_min). Since repetition is allowed, the overall maximum total is k * (global_max - global_min).

## Refining the problem, round 2 thoughts
- Edge cases:
  - If n == 1 then max == min so value is 0; answer 0 regardless of k.
  - Large values: nums[i] up to 1e9, k up to 1e5, product up to 1e14 — safe in Python (big ints); in languages with 64-bit integers use 64-bit type.
- Complexity considerations:
  - We only need to compute min and max of the array once: O(n) time, O(1) extra space.
- Alternative solutions like enumerating subarrays or dynamic programming are unnecessary because repetition is allowed and the maximum per-subarray value is the global range.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maximumTotalSubarrayValue(self, nums: List[int], k: int) -> int:
        """
        Return k * (max(nums) - min(nums)).
        """
        if not nums:
            return 0
        return (max(nums) - min(nums)) * k
```
- Notes:
  - Approach: Find the global maximum and minimum of nums; the maximum value of any subarray is their difference. Because subarrays may be chosen multiple times (including choosing the same subarray k times), the optimal total is k * (global_max - global_min).
  - Time complexity: O(n) to compute max and min.
  - Space complexity: O(1) extra space (ignoring input storage).
  - Handles edge cases: empty list (guard) and single-element arrays (difference 0).