# [Problem 1752: Check if Array Is Sorted and Rotated](https://leetcode.com/problems/check-if-array-is-sorted-and-rotated/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to decide if the given array could be the result of taking a non-decreasingly sorted array and rotating it some number of positions (including 0). A rotation keeps the relative order except for one "cut" where the tail wraps to the front. So if we scan the array left to right, we'd expect at most one place where a later element is smaller than the previous (a "drop"). If there's more than one drop, it can't come from a single cut rotation of a sorted array. Duplicates are allowed; equal neighbors are fine and do not create a drop. Also consider the wrap-around from last to first — that also can be the single allowed drop.

So the idea that comes immediately is to count how many indices i satisfy nums[i] > nums[i+1] (with i+1 taken modulo n). If count <= 1 then true, else false.

## Refining the problem, round 2 thoughts
- Edge cases:
  - n = 1: trivially true.
  - All elements equal: zero drops, true.
  - Already sorted (no rotation needed): zero drops, true.
  - Typical failing case: two or more drops (including wrap-around) -> false.
- Complexity:
  - Single pass over array -> O(n) time, O(1) extra space.
- Alternative approaches:
  - Find index of minimum element and verify array is sorted if started from that index — also O(n) but slightly more code. The drop-count method is simpler and concise.
- Implementation detail:
  - Use modulo indexing for the wrap check: compare nums[i] and nums[(i+1) % n].

## Attempted solution(s)
```python
from typing import List

class Solution:
    def check(self, nums: List[int]) -> bool:
        n = len(nums)
        if n <= 1:
            return True
        
        drops = 0
        for i in range(n):
            if nums[i] > nums[(i + 1) % n]:
                drops += 1
                if drops > 1:
                    return False
        return True
```
- Notes:
  - Approach: Count the number of "drops" where nums[i] > nums[i+1], treating the array as circular. A valid rotated sorted array can have at most one drop (the rotation cut). If there are zero drops the array is already sorted (rotation by 0).
  - Time complexity: O(n), where n = len(nums) because we scan once.
  - Space complexity: O(1) extra space (only counters and indices).