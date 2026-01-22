# [Problem 3423: Maximum Difference Between Adjacent Elements in a Circular Array](https://leetcode.com/problems/maximum-difference-between-adjacent-elements-in-a-circular-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Sorry — I can’t share my internal stream-of-consciousness. I can, however, give a concise summary of the approach: iterate through the array once, compute absolute differences between each element and the next (using modulo to handle the circular adjacency between the last and first), and track the maximum difference.

## Refining the problem, round 2 thoughts
Concise refinement and considerations:
- We need the maximum absolute difference between adjacent elements in a circular array, so treat index i and (i+1)%n as adjacent for all i.
- Edge cases: n >= 2 as per constraints, elements can be negative — use abs().
- Time complexity target: O(n) by a single pass. Space complexity: O(1) extra space.
- Alternative approaches (not needed here): sorting or other transforms are unnecessary — direct adjacency check is optimal.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxDifference(self, nums: List[int]) -> int:
        n = len(nums)
        if n < 2:
            return 0  # Given constraints guarantee n >= 2, but keep safe fallback.
        
        max_diff = 0
        for i in range(n):
            j = (i + 1) % n
            diff = abs(nums[i] - nums[j])
            if diff > max_diff:
                max_diff = diff
        return max_diff
```
- Notes:
  - Approach: single pass through the array computing abs(nums[i] - nums[(i+1)%n]) and tracking the maximum.
  - Time complexity: O(n), where n = len(nums).
  - Space complexity: O(1) extra space.
  - The modulo handles the circular adjacency between the last and first elements. The constraints guarantee n >= 2 so every element has an adjacent neighbor.