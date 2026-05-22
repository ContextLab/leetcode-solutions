# [Problem 33: Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I'm thinking this is the classic rotated sorted array search. The array was sorted and then rotated; values are distinct. The requirement is O(log n) so a linear scan is out. Two common approaches come to mind:
- Find the rotation pivot (index of smallest element) with binary search, then do a normal binary search on the appropriate half.
- Or perform a single modified binary search that at each step determines which half (left or right of mid) is sorted and decides where the target can lie.

The second approach avoids two-phase search and is simpler to implement. Need to be careful about boundary conditions and comparisons (<= vs <) because values are distinct.

## Refining the problem, round 2 thoughts
Refine: Use a while loop with low and high. Compute mid. If nums[mid] == target return mid. Otherwise check whether left half [low..mid] is sorted by comparing nums[low] <= nums[mid]. If left sorted, see if target in [nums[low], nums[mid]) — if yes move high = mid - 1, else low = mid + 1. If left not sorted, right half must be sorted; check if target in (nums[mid], nums[high]] and move low/high accordingly.

Edge cases:
- Single element array.
- No rotation (already sorted) — the checks still work.
- Rotation at any index.
- Distinct values guarantee eliminates equalities causing ambiguity.

Time complexity: O(log n). Space: O(1).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        low, high = 0, len(nums) - 1
        
        while low <= high:
            mid = (low + high) // 2
            if nums[mid] == target:
                return mid
            
            # If left half [low..mid] is sorted
            if nums[low] <= nums[mid]:
                # Check if target is in left half
                if nums[low] <= target < nums[mid]:
                    high = mid - 1
                else:
                    low = mid + 1
            else:
                # Right half [mid..high] must be sorted
                if nums[mid] < target <= nums[high]:
                    low = mid + 1
                else:
                    high = mid - 1
        
        return -1
```
- Approach: Single-pass modified binary search. At each step determine which half is sorted and decide where the target can be, discarding the other half. This guarantees logarithmic time.
- Time complexity: O(log n) — each iteration halves the search range.
- Space complexity: O(1) — only a few pointers/variables used.
- Implementation details: Using nums[low] <= nums[mid] to detect a sorted left half; distinct values ensure no ambiguity. The comparisons for membership in a half use inclusive/exclusive bounds consistent with equality checks already handled.