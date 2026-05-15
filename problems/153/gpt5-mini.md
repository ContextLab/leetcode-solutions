# [Problem 153: Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have a sorted array that was rotated. The minimum is the rotation pivot (the smallest element). With unique elements we can find the pivot using binary search in O(log n). A naive scan is O(n) but we need logarithmic time. Observations: if the array is not rotated (nums[0] <= nums[-1]) the first element is the minimum. Otherwise, the minimum lies where the order breaks. Using binary search we can compare mid to an endpoint (commonly nums[right]) to decide which half contains the minimum. If nums[mid] > nums[right], the minimum is to the right of mid; otherwise the minimum is at mid or to its left.

## Refining the problem, round 2 thoughts
Use l, r pointers. Maintain invariant that the minimum is in [l, r]. While l < r compute mid = (l + r) // 2. If nums[mid] > nums[r], set l = mid + 1 (min in right half). Else set r = mid (mid could be minimum). Loop ends when l == r and that index is the minimum. Edge cases: n == 1, array not rotated (first element minimum), fully rotated (rotation by n yields original array but still handled by the check). All elements unique so no equal-case ambiguities. Time O(log n), space O(1).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def findMin(self, nums: List[int]) -> int:
        """
        Binary search for the minimum in a rotated sorted array with unique elements.
        Invariant: the minimum is always within [l, r].
        """
        l, r = 0, len(nums) - 1
        # If array not rotated (or rotated n times), the first element is the minimum.
        if nums[l] <= nums[r]:
            return nums[l]
        
        while l < r:
            mid = (l + r) // 2
            # If mid element is greater than rightmost, min is to the right of mid.
            if nums[mid] > nums[r]:
                l = mid + 1
            else:
                # nums[mid] <= nums[r]: min is at mid or to the left of mid.
                r = mid
        return nums[l]
```
- Notes:
  - Approach: binary search comparing nums[mid] with nums[r], maintaining that the minimum lies in [l, r].
  - Time complexity: O(log n).
  - Space complexity: O(1).
  - Handles edge cases: single-element arrays, arrays that are not rotated (returns nums[0]), and arrays rotated any number of times.