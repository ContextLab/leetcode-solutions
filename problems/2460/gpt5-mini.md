# [Problem 2460: Apply Operations to an Array](https://leetcode.com/problems/apply-operations-to-an-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to simulate n-1 operations where for each i, if nums[i] == nums[i+1] then nums[i] *= 2 and nums[i+1] = 0. After all operations, move all zeros to the end while preserving the order of non-zero elements.

First thought: do a single left-to-right pass to perform the described operations (they are sequential), then do another pass to shift non-zero values to the front (or build a new array). This is straightforward and O(n). There might be an in-place way to compress zeros to the end with two pointers to save space.

Also note: merging doesn't cascade backward because we only compare i and i+1 in increasing i; after an operation sets nums[i+1] to 0, it won't immediately merge with the next one unless a later i handles it.

## Refining the problem, round 2 thoughts
Refinement:
- First pass: for i in [0..n-2], if nums[i] == nums[i+1] then double nums[i] and set nums[i+1]=0.
- Second pass: shift all non-zero elements left preserving order. This can be done by building a new list or by an in-place two-pointer approach (write pointer).
- Edge cases: arrays that contain zeros initially, arrays where multiple equal values appear consecutively (e.g., [2,2,2]). Because operations are sequential, only adjacent pairs at the moment of their index are considered.
- Complexity: two O(n) passes -> O(n) time. Space can be O(1) extra if shifting in-place, or O(n) if creating a new array.

I'll implement an in-place solution with two passes to avoid extra space allocation (aside from constant overhead).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def applyOperations(self, nums: List[int]) -> List[int]:
        n = len(nums)
        # First pass: perform the sequential operations
        for i in range(n - 1):
            if nums[i] == nums[i + 1]:
                nums[i] *= 2
                nums[i + 1] = 0

        # Second pass: shift non-zero elements to the front in-place
        write = 0
        for read in range(n):
            if nums[read] != 0:
                nums[write] = nums[read]
                # If we moved an element forward, zero out the old spot
                if write != read:
                    nums[read] = 0
                write += 1

        return nums
```
- Notes about the solution:
  - Approach: Two passes. First pass applies the operations exactly as described (sequentially). Second pass compacts non-zero values to the front in-place using a write pointer, filling the remainder implicitly with zeros by zeroing positions we moved from.
  - Time complexity: O(n) — each element is touched a constant number of times.
  - Space complexity: O(1) extra space (in-place).
  - This matches the sequential nature of operations and preserves the relative order of non-zero elements when shifting zeros to the end.