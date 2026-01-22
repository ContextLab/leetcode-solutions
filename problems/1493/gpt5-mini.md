# [Problem 1493: Longest Subarray of 1's After Deleting One Element](https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the longest subarray of 1s after deleting exactly one element. Deleting one element is like allowing one zero inside a subarray of the original array and then removing it. That suggests a sliding-window approach where we maintain a window that contains at most one zero. The number of 1s for a window that has at most one zero is window_length - 1 (we remove that zero). If the window contains no zeros (all ones), we still must delete one element, so the result is window_length - 1 in that case too. Edge cases: all ones (answer = n-1), all zeros (answer = 0). Two pointers with a zero count works nicely and is O(n) time, O(1) space.

## Refining the problem, round 2 thoughts
- We'll use left and right pointers. Expand right; if nums[right] == 0 increment zero_count. While zero_count > 1, move left forward decreasing zero_count when we skip a zero.
- For each valid window (zero_count <= 1) compute candidate = window_length - 1 and update max.
- When array is all ones, the sliding window will often have zero_count == 0; candidate will be window_length - 1 yielding n-1 as required.
- When array has zeros, windows containing one zero yield the count of ones if we remove that zero.
- Complexity: one pass O(n), constant extra space.

## Attempted solution(s)
```python
class Solution:
    def longestSubarray(self, nums: list[int]) -> int:
        n = len(nums)
        left = 0
        zero_count = 0
        max_len = 0

        for right in range(n):
            if nums[right] == 0:
                zero_count += 1

            # Shrink window until we have at most one zero
            while zero_count > 1:
                if nums[left] == 0:
                    zero_count -= 1
                left += 1

            # For a window with at most one zero, after deleting one element
            # the number of 1's is window_length - 1 (we delete that zero or
            # delete any element if no zero exists)
            current_ones_after_deletion = right - left + 1 - 1
            if current_ones_after_deletion > max_len:
                max_len = current_ones_after_deletion

        return max_len
```
- Approach: sliding window with two pointers maintaining at most one zero in the window. For each window, the number of 1's after deleting exactly one element equals window_length - 1.
- Time complexity: O(n) — each pointer moves at most n steps.
- Space complexity: O(1) — only a few integer variables used.
- Important details:
  - The formula window_length - 1 handles both the case when the window contains one zero (we delete that zero) and when the window contains no zero (we are forced to delete one '1', so length reduces by one).
  - Works correctly for edge cases:
    - All ones: returns n-1.
    - All zeros: returns 0.