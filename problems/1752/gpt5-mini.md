# [Problem 1752: Check if Array Is Sorted and Rotated](https://leetcode.com/problems/check-if-array-is-sorted-and-rotated/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to decide if nums could be a rotated version of a non-decreasing (sorted) array. Rotation preserves the relative order except that there's a single wrap from the end back to the start. So in the rotated array we expect at most one place where a value is greater than the next value (a "drop" or inversion). If there are two or more drops, it can't come from a single rotation of a sorted non-decreasing array. Duplicates are allowed, so equal adjacent elements are fine (not drops). Edge cases: tiny arrays (length 1 or 2), all-equal arrays — these should be allowed.

## Refining the problem, round 2 thoughts
So the algorithm: scan the array and count positions i where nums[i] > nums[(i+1) % n]. If the count is <= 1 return True, else False. This handles rotation implicitly with modulo for the wrap-around. Complexity is O(n) time and O(1) extra space. Confirm edge cases:
- n == 1: zero drops -> True
- all equal elements: zero drops -> True
- strictly increasing but not rotated (rotation by 0): zero drops -> True
- [3,1,2] has one drop at 3>1 -> True (original [1,2,3])
- [2,1,3,4] has drop at 2>1 and maybe others -> count>1 -> False

Alternative would be to try to find rotation pivot and then check both segments are sorted; but counting drops is simpler and optimal.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def check(self, nums: List[int]) -> bool:
        n = len(nums)
        drops = 0
        for i in range(n):
            if nums[i] > nums[(i + 1) % n]:
                drops += 1
                if drops > 1:
                    return False
        return True
```
- Notes:
  - Approach: count the number of times an element is greater than the next (with wrap-around). A sorted non-decreasing array rotated some amount can have at most one such drop.
  - Time complexity: O(n), where n = len(nums), since we scan the array once.
  - Space complexity: O(1) extra space.