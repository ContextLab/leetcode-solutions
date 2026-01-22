# [Problem 3264: Final Array State After K Multiplication Operations I](https://leetcode.com/problems/final-array-state-after-k-multiplication-operations-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to perform k operations where each operation picks the minimum value in nums (if multiple, pick the first occurrence) and replaces it with value * multiplier. The constraints are small (n <= 100, k <= 10), so a direct simulation is fine. The main detail is to ensure tie-breaking uses the first occurrence of the minimum. A naive approach scanning the array to find the first minimum index and updating it in-place for each of k iterations is straightforward and efficient enough.

## Refining the problem, round 2 thoughts
Edge cases:
- multiplier == 1: values won't change; we still must pick the first minimum each time (no effect).
- All values equal: we will repeatedly pick index 0 (the first occurrence) and update it k times.
- Small n and k mean we don't need complex data structures like heaps; repeated linear scans are fine.

Time complexity: O(k * n) which with n <= 100 and k <= 10 is trivial. Space complexity: O(1) extra (in-place updates).

I'll implement a simple loop that for each operation:
1. Find index of the first minimum value (single pass).
2. Multiply nums[index] by multiplier.

This guarantees correct tie-breaking and is easy to read.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def finalArray(self, nums: List[int], k: int, multiplier: int) -> List[int]:
        # Perform k operations
        for _ in range(k):
            # find index of first minimum
            min_idx = 0
            for i in range(1, len(nums)):
                if nums[i] < nums[min_idx]:
                    min_idx = i
            # multiply the found minimum
            nums[min_idx] *= multiplier
        return nums

# Example usage:
# sol = Solution()
# print(sol.finalArray([2,1,3,5,6], 5, 2))  # [8,4,6,5,6]
# print(sol.finalArray([1,2], 3, 4))       # [16,8]
```

- Notes:
  - Approach: Direct simulation by repeatedly finding the first minimum and updating it.
  - Time complexity: O(k * n) where n = len(nums), k operations and each scan is O(n).
  - Space complexity: O(1) extra space (in-place updates).
  - This is simple, easy to reason about, and optimal given constraints. For larger constraints one might consider a priority queue that stores (value, index) and supports updates, but for the given limits the linear scan is preferable for clarity.