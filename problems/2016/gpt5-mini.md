# [Problem 2016: Maximum Difference Between Increasing Elements](https://leetcode.com/problems/maximum-difference-between-increasing-elements/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the maximum nums[j] - nums[i] with i < j and nums[i] < nums[j]. The brute force is obvious: check all pairs (i, j) with i < j and track the max positive difference — that's O(n^2). But I can do better: as I scan from left to right I can remember the smallest value seen so far (a candidate i). For each new element nums[j] I can compute nums[j] - min_so_far and update the answer if it's larger and positive. Also update min_so_far when I see a new smaller value. That yields O(n) time and O(1) extra space. Edge cases: strictly non-increasing array should return -1; identical values never satisfy nums[i] < nums[j].

## Refining the problem, round 2 thoughts
- Confirm iteration order: since i < j, scanning left-to-right is natural.
- Maintain min_so_far initialized to nums[0]. For j from 1..n-1:
  - if nums[j] > min_so_far: candidate diff = nums[j] - min_so_far, update max_diff
  - if nums[j] < min_so_far: update min_so_far
- If no valid increasing pair found, return -1 (we can keep max_diff initialized to -1).
- Complexity: O(n) time, O(1) space. n <= 1000 so O(n^2) would also pass but O(n) is cleaner and optimal.
- Watch out for large values up to 1e9: subtraction fits in Python int without issue.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maximumDifference(self, nums: List[int]) -> int:
        # Initialize the smallest value seen so far and the answer
        min_so_far = nums[0]
        max_diff = -1

        # Iterate through the array starting from index 1
        for x in nums[1:]:
            if x > min_so_far:
                # valid increasing pair found, update max_diff
                diff = x - min_so_far
                if diff > max_diff:
                    max_diff = diff
            elif x < min_so_far:
                # update the smallest value seen so far
                min_so_far = x

        return max_diff
```
- Notes:
  - Approach: Single pass, track minimum value seen so far and compute differences on the fly.
  - Time complexity: O(n), where n = len(nums) — one scan through the array.
  - Space complexity: O(1) extra space (only a couple of variables).
  - Correctly returns -1 when no increasing pair exists (max_diff stays -1).