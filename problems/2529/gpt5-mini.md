# [Problem 2529: Maximum Count of Positive Integer and Negative Integer](https://leetcode.com/problems/maximum-count-of-positive-integer-and-negative-integer/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The array is sorted non-decreasingly, so negatives (if any) are on the left, zeros (if any) in the middle, positives (if any) on the right. We need the larger of the counts of negatives and positives. A straightforward idea is to count negatives and positives directly by scanning, but since the array is sorted we can do better with binary search (or Python's bisect) to find boundaries (first non-negative or first positive). That yields O(log n) time as requested by the follow-up.

## Refining the problem, round 2 thoughts
- Count of negatives = index of first element >= 0 (i.e., bisect_left(nums, 0)).
- Count of positives = total length - index of last zero - 1, equivalently len(nums) - bisect_right(nums, 0) which gives the first index > 0.
- Edge cases: all negatives (positives = 0), all positives (negatives = 0), only zeros (both 0). Using bisect handles these naturally.
- Alternative: single linear pass O(n) is simplest and fine given n ≤ 2000, but using bisect meets the O(log n) follow-up and is still simple to implement.
- Time: O(log n) with bisect, Space: O(1).

## Attempted solution(s)
```python
from typing import List
import bisect

class Solution:
    def maximumCount(self, nums: List[int]) -> int:
        # Number of negative integers: first index where value >= 0
        neg_count = bisect.bisect_left(nums, 0)
        # Number of positive integers: elements strictly greater than 0
        pos_count = len(nums) - bisect.bisect_right(nums, 0)
        return max(neg_count, pos_count)
```
- Notes:
  - We use bisect_left(nums, 0) to get the count of elements < 0 (negatives).
  - We use bisect_right(nums, 0) to find the first index > 0; subtracting from len(nums) gives count of positives.
  - Time complexity: O(log n) due to binary searches.
  - Space complexity: O(1).