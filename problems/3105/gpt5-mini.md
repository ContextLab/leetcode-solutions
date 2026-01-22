# [Problem 3105: Longest Strictly Increasing or Strictly Decreasing Subarray](https://leetcode.com/problems/longest-strictly-increasing-or-strictly-decreasing-subarray/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the length of the longest contiguous subarray that is strictly increasing or strictly decreasing. A brute-force approach would check every subarray (O(n^2)) and test monotonicity, but given n ≤ 50 that's fine for correctness — however a linear scan is simpler and optimal.

Observation: while scanning once, we can maintain the length of the current strictly increasing run and the current strictly decreasing run. At each adjacent pair nums[i-1], nums[i]:
- if nums[i] > nums[i-1] then extend the increasing run and reset the decreasing run to 1,
- if nums[i] < nums[i-1] then extend the decreasing run and reset the increasing run to 1,
- if nums[i] == nums[i-1] then both runs reset to 1 (equal breaks strict monotonicity).
Keep the maximum length encountered.

Edge cases: array length 1 should return 1; equal adjacent values break runs.

## Refining the problem, round 2 thoughts
- Time complexity: O(n) single pass, which is optimal.
- Space complexity: O(1) extra space (just counters).
- Alternatives: DP arrays storing longest inc/dec ending at i (but that is equivalent to the two counters).
- Confirm handling of equal elements: must reset both counters to 1 because strict inequality is required.
- Small n boundary conditions: initialize counters to 1, iterate from i = 1 to n-1.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def longestSubarray(self, nums: List[int]) -> int:
        if not nums:
            return 0
        n = len(nums)
        # Both lengths are at least 1 (single element)
        inc_len = 1
        dec_len = 1
        best = 1
        for i in range(1, n):
            if nums[i] > nums[i-1]:
                inc_len += 1
                dec_len = 1
            elif nums[i] < nums[i-1]:
                dec_len += 1
                inc_len = 1
            else:  # nums[i] == nums[i-1]
                inc_len = 1
                dec_len = 1
            if inc_len > best:
                best = inc_len
            if dec_len > best:
                best = dec_len
        return best
```
- Notes about the solution approach:
  - We scan once, updating two counters: inc_len and dec_len represent the lengths of the current strictly increasing and strictly decreasing subarrays that end at the current index.
  - When the current pair continues one monotonic direction, extend that counter and reset the other to 1.
  - Equal adjacent values reset both counters because "strict" excludes equality.
- Complexity:
  - Time: O(n), one pass through the array.
  - Space: O(1), only a few integer counters used.