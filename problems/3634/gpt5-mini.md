# [Problem 3634: Minimum Removals to Balance Array](https://leetcode.com/problems/minimum-removals-to-balance-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can't share internal stream-of-consciousness reasoning, but here's a concise, non-sensitive summary of the idea that comes to mind: sort the array and use a two-pointer (sliding window) approach to find the largest subarray where max <= k * min. The minimum removals equals total length minus the size of that largest valid subarray.

## Refining the problem, round 2 thoughts
- After sorting, any valid remaining array (non-empty) with min at index i and max at index j must satisfy nums[j] <= nums[i] * k. Because the array is sorted, for a fixed i we can expand j as far right as this inequality holds; when it fails, increment i.
- We want to maximize the number of elements we keep (i.e., the window length j-i+1), so answer = n - max_window_len.
- Two-pointer sliding window is O(n) after sorting, so total complexity O(n log n) due to sort.
- Edge cases: arrays of size 1 return 0 (already balanced). k >= 1 per constraints. Python integers handle large products safely.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minimumRemovals(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n <= 1:
            return 0
        nums.sort()
        i = 0
        max_keep = 1  # at least one element can be kept
        for j in range(n):
            # increase left pointer until window [i..j] is valid: nums[j] <= nums[i] * k
            while i <= j and nums[j] > nums[i] * k:
                i += 1
            # window length is j - i + 1
            curr_len = j - i + 1
            if curr_len > max_keep:
                max_keep = curr_len
        return n - max_keep
```
- Approach notes: Sort nums and use sliding window / two pointers to maintain the largest contiguous block where max <= k * min. The sorted property ensures that for fixed left i, the rightmost valid j is monotonic as i increases, enabling O(n) scanning after sort.
- Time complexity: O(n log n) for sorting + O(n) for the two-pointer scan => O(n log n) overall.
- Space complexity: O(1) extra (ignoring input sort in-place) or O(n) if the language's sort requires extra space.