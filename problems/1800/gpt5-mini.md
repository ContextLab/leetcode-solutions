# [Problem 1800: Maximum Ascending Subarray Sum](https://leetcode.com/problems/maximum-ascending-subarray-sum/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the maximum sum of a strictly increasing contiguous subarray. The input size is small (n <= 100), so an O(n) or even O(n^2) solution would be fine, but O(n) is straightforward. The array contains positive integers, so any increasing sequence sum grows as I extend it. A single pass tracking the current ascending run sum and the best seen so far should work. When the next number is greater than the previous, I extend the run; otherwise I start a new run at the current element. Edge cases: all decreasing (answer is the largest single element), single element array (answer is that element), equal adjacent elements break the strictly increasing condition.

## Refining the problem, round 2 thoughts
A two-pointer approach (start of current run and current index) or a simple running sum with a check against the previous element both accomplish the same thing. I'll use the running sum approach since it's concise: initialize curr_sum and max_sum to nums[0], iterate from index 1 to end; if nums[i] > nums[i-1] add to curr_sum, else reset curr_sum to nums[i]; update max_sum each step. Time complexity O(n), space O(1). Because nums values are positive, resetting to nums[i] is always safe — we don't need to carry any negative-subarray logic. Also ensure strictness: equal values should reset.

## Attempted solution(s)
```python
class Solution:
    def maxAscendingSum(self, nums: list[int]) -> int:
        if not nums:
            return 0  # not needed per constraints, but safe guard
        
        max_sum = curr_sum = nums[0]
        for i in range(1, len(nums)):
            if nums[i] > nums[i-1]:
                curr_sum += nums[i]
            else:
                curr_sum = nums[i]
            if curr_sum > max_sum:
                max_sum = curr_sum
        return max_sum
```
- Notes:
  - Approach: Single pass, keep a running sum for the current strictly-increasing contiguous segment; reset when the strict increase property fails; track the maximum running sum seen.
  - Time complexity: O(n), where n = len(nums), since we scan the array once.
  - Space complexity: O(1), only a couple of integer variables used.
  - Important detail: Use strict greater-than (nums[i] > nums[i-1]) because equal values break the strictly increasing requirement. Edge cases like all decreasing or single-element arrays are naturally handled by the initialization.