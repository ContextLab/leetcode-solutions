# [Problem 1695: Maximum Erasure Value](https://leetcode.com/problems/maximum-erasure-value/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can’t share internal chain-of-thought or stream-of-consciousness. I can, however, give a concise non-sensitive summary of the approach: use a sliding window (two pointers) to maintain a contiguous subarray of unique elements, tracking the current sum; when a duplicate appears, move the left pointer forward removing values until the duplicate is gone, update the maximum sum seen.

## Refining the problem, round 2 thoughts
- We want the maximum sum of any contiguous subarray that contains all unique elements.
- A sliding window with a set (or a map) to track which elements are currently in the window is a natural fit because we can expand and contract the window in O(1) amortized time per element.
- Maintain:
  - left and right pointers,
  - a set of values currently in the window,
  - current window sum,
  - best (maximum) sum seen so far.
- When nums[right] is already in the set, move left forward removing values (and subtracting from current sum) until that duplicate is removed; then add nums[right] and continue.
- Edge cases:
  - All elements unique — window expands to whole array.
  - All elements identical — best is the single element value.
- Complexity:
  - Time: O(n) — each element is added and removed at most once.
  - Space: O(min(n, U)) where U is range of distinct values (<= 10^4 by constraints).

## Attempted solution(s)
```python
class Solution:
    def maximumUniqueSubarray(self, nums: list[int]) -> int:
        seen = set()
        left = 0
        cur_sum = 0
        best = 0

        for right, val in enumerate(nums):
            # If val is duplicate in current window, move left until duplicate removed
            while val in seen:
                removed = nums[left]
                seen.remove(removed)
                cur_sum -= removed
                left += 1
            # Add current value
            seen.add(val)
            cur_sum += val
            # Update best sum
            if cur_sum > best:
                best = cur_sum

        return best
```
- Notes:
  - Approach: two-pointer sliding window with a set to ensure uniqueness.
  - Each element is inserted and removed at most once, giving O(n) time.
  - Space usage is O(k) where k is number of distinct elements in the current window (bounded by min(n, 10^4) per constraints).
  - Implementation detail: maintain current window sum to avoid recomputing sums when shrinking/expanding.