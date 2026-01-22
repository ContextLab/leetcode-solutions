# [Problem 1749: Maximum Absolute Sum of Any Subarray](https://leetcode.com/problems/maximum-absolute-sum-of-any-subarray/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the maximum absolute sum of any contiguous subarray. Absolute value suggests we care about both very large positive sums and very large negative sums (whose absolute value is large). My first thought: this is like Kadane's algorithm for maximum subarray sum, but we also need the "most negative" subarray (minimum subarray sum). If we can get the maximum subarray sum and the minimum subarray sum, the answer is max(max_sum, -min_sum). There's also the possibility of the empty subarray (sum 0), so results should be at least 0. Using two passes of Kadane (or a single pass maintaining both max and min) should work in O(n) time and O(1) space.

## Refining the problem, round 2 thoughts
Refinements / edge cases:
- All positive numbers: maximum absolute sum is the sum of a subarray with large positive sum (Kadane finds it).
- All negative numbers: minimum subarray sum will be negative and its absolute value could be the answer; empty subarray (0) is an option but won't beat a negative sum's absolute value if it has larger magnitude.
- Single element arrays, mixed signs — Kadane handles them.
- Because empty subarray is allowed, initial values for max and min can start at 0 so we implicitly consider the empty subarray. That also keeps max_so_far >= 0 and min_so_far <= 0.
- Complexity target: O(n) time, O(1) space. Alternative approach: prefix sums with tracking min and max prefix to get largest difference — equivalent but no advantage over Kadane variant.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxAbsoluteSum(self, nums: List[int]) -> int:
        """
        Maintain Kadane-like variables for maximum subarray sum and minimum subarray sum
        in a single pass. Because an empty subarray is allowed, initialize running values
        and best values at 0.
        """
        max_ending = 0   # best ending-at-current for positive sums
        min_ending = 0   # best ending-at-current for negative sums
        max_so_far = 0   # best positive subarray sum seen
        min_so_far = 0   # most negative subarray sum seen (<= 0)

        for x in nums:
            # update running maximum subarray ending here
            max_ending = max(max_ending + x, x)
            if max_ending > max_so_far:
                max_so_far = max_ending

            # update running minimum subarray ending here
            min_ending = min(min_ending + x, x)
            if min_ending < min_so_far:
                min_so_far = min_ending

        # the answer is the larger of max positive sum and absolute of most negative sum
        return max(max_so_far, -min_so_far)
```
- Notes:
  - Approach: single-pass Kadane for both maximum and minimum contiguous subarray sums.
  - Time complexity: O(n), where n = len(nums).
  - Space complexity: O(1), only a handful of variables used.
  - Implementation detail: initializing to 0 handles the "possibly empty" subarray case (ensuring results are at least 0). The final answer is max(max_so_far, -min_so_far).