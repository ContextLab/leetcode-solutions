# [Problem 3392: Count Subarrays of Length Three With a Condition](https://leetcode.com/problems/count-subarrays-of-length-three-with-a-condition/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to check every subarray of length 3 and test whether "sum of the first and third numbers equals exactly half of the second number." Because all numbers are integers, comparing halves directly might introduce floats if the middle is odd. A safer integer check is to multiply both sides by 2: 2 * (first + third) == second. The number of subarrays of length 3 in an array of length n is n-2, so a single pass with a sliding window of size 3 is enough. Time should be O(n), space O(1). Watch out for negatives — the arithmetic still holds. Constraints guarantee n >= 3 so no special handling for too-short arrays is necessary (but it's trivial to handle).

## Refining the problem, round 2 thoughts
Refinement: iterate i from 0 to len(nums)-3 and check condition on nums[i], nums[i+1], nums[i+2]. Use the integer transformed condition to avoid floating-point comparisons:
  nums[i+1] == 2 * (nums[i] + nums[i+2])
Edge cases: middle element odd — the transformed check naturally fails when no integer half exists. Negative values and zero are fine. Complexity: single scan, O(n) time, O(1) extra space. This is the simplest and most direct solution; no need for prefix sums or extra data structures.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def countGood(self, nums: List[int]) -> int:
        """
        Count subarrays of length 3 where first + third == middle / 2.
        Use integer comparison: middle == 2 * (first + third)
        """
        n = len(nums)
        count = 0
        for i in range(n - 2):
            if nums[i + 1] == 2 * (nums[i] + nums[i + 2]):
                count += 1
        return count
```
- Notes:
  - Approach: sliding window of size 3, check integer-transformed condition to avoid floating-point issues.
  - Time complexity: O(n), where n = len(nums) — we check each length-3 window once.
  - Space complexity: O(1) extra space (only a counter and loop index).