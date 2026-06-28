# [Problem 1846: Maximum Element After Decreasing and Rearranging](https://leetcode.com/problems/maximum-element-after-decreasing-and-rearranging/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Sorry — I can’t share stream-of-consciousness internal monologue. Instead, here is a concise summary of the approach:

- Because we may rearrange arbitrarily and only decrease values, we can sort the array and then greedily make each element as large as possible while respecting the constraints: first element must be 1, and each next element can be at most previous + 1 (and cannot increase above its original value).
- So sort arr, set the first to 1, and for each following element take min(original_value, previous + 1). The maximum seen after this process is the answer.

## Refining the problem, round 2 thoughts
- Edge cases: array of length 1 (answer is 1 after ensuring first element is 1), many duplicates, very large values — sorting handles order and decreases handle large values.
- Time complexity: sorting dominates at O(n log n). Single pass after sort is O(n). Space complexity: O(1) extra if sorting in place (or O(n) depending on sorting implementation).
- This greedy is optimal because after sorting the smallest available numbers will be placed earliest, allowing later positions to potentially grow up to previous+1; decreasing larger numbers to at most prev+1 is always feasible.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maximumElementAfterDecreasingAndRearranging(self, arr: List[int]) -> int:
        # Sort the array to place smaller values first
        arr.sort()
        prev = 0
        max_val = 0
        for x in arr:
            # Each element can be decreased and must be at most prev + 1
            cur = min(x, prev + 1)
            # Ensure the first element is at least 1 (x >= 1 by constraints, so this holds)
            if cur < 1:
                cur = 1
            prev = cur
            if cur > max_val:
                max_val = cur
        return max_val
```
- Notes:
  - Approach: sort + greedy pass capping each element at prev + 1 (with first element becoming 1).
  - Time complexity: O(n log n) due to sorting, where n = len(arr).
  - Space complexity: O(1) extra space (in-place sort), or O(n) if the language's sort implementation requires extra space.