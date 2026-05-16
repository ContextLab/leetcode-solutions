# [Problem 154: Find Minimum in Rotated Sorted Array II](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have a sorted array that has been rotated, and now it may contain duplicates. For the no-duplicates variant we can use a binary search comparing nums[mid] to nums[right] to decide which half contains the minimum. With duplicates, equality cases (nums[mid] == nums[right]) make that decision ambiguous because duplicates can hide the pivot. A naive approach is to scan linearly and return min(nums) which is O(n) but we can usually do better with a modified binary search.

Common trick: when nums[mid] > nums[right], the min is to the right of mid. When nums[mid] < nums[right], the min is at mid or to the left. When nums[mid] == nums[right], reduce the search space by shrinking right by 1 (right -= 1) — this is safe because nums[right] is equal to nums[mid], so dropping right cannot discard the unique minimum, but it can degrade to O(n) in worst case (e.g., all elements equal).

Plan: use while left < right, compare nums[mid] and nums[right], adjust left/right accordingly, and return nums[left] at the end.

## Refining the problem, round 2 thoughts
Edge cases:
- Single element array -> return that element.
- Array not rotated (still sorted ascending) -> algorithm should return first element.
- All elements equal -> any element is minimum; algorithm reduces right until left==right and returns that value.

Complexity:
- Time: Average O(log n), worst-case O(n) because of the nums[mid] == nums[right] case where we only decrement right by 1.
- Space: O(1) extra.

Alternative: linear scan O(n) always correct but not optimal for many cases. The modified binary search is the standard accepted approach.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def findMin(self, nums: List[int]) -> int:
        """
        Find minimum in rotated sorted array that may contain duplicates.
        Uses modified binary search. Worst-case O(n) when duplicates force linear steps.
        """
        if not nums:
            raise ValueError("nums must contain at least one element")
        
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (left + right) // 2
            if nums[mid] > nums[right]:
                # min must be in (mid, right]
                left = mid + 1
            elif nums[mid] < nums[right]:
                # min is in [left, mid]
                right = mid
            else:
                # nums[mid] == nums[right], cannot determine side, safely shrink right
                right -= 1
        return nums[left]
```
- Notes:
  - Approach: modified binary search handling duplicates by decrementing right when nums[mid] == nums[right].
  - Correctness: When nums[mid] > nums[right], the rotation pivot is right of mid. When nums[mid] < nums[right], pivot is at or left of mid. When equal, removing nums[right] is safe because it's not the unique minimum if a smaller value exists on the left; if all values equal, shrinking still yields correct result.
  - Time complexity: Average O(log n), worst-case O(n).
  - Space complexity: O(1).