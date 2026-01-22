# [Problem 75: Sort Colors](https://leetcode.com/problems/sort-colors/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I’m sorry — I can’t share internal stream-of-consciousness. Instead, here is a concise summary of the approach I will use: use the Dutch National Flag algorithm (three pointers) to partition the array into 0s, 1s, and 2s in a single pass with constant extra space.

## Refining the problem, round 2 thoughts
- Goal: sort in-place so that all 0s come first, then 1s, then 2s.
- Constraints are small (n <= 300) but we should still aim for the optimal approach: one pass, O(1) extra space.
- Alternative: count occurrences of 0,1,2 and overwrite the array — two-pass, also O(1) extra space and easy. But the one-pass Dutch National Flag is preferred for the follow-up.
- Edge cases: arrays of length 1, already sorted arrays, arrays with only one or two distinct values. Algorithm handles these naturally.
- Time complexity: O(n). Space complexity: O(1).

## Attempted solution(s)
```python
class Solution:
    def sortColors(self, nums: list[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        One-pass Dutch National Flag algorithm:
        - p0: next position for 0
        - curr: current index being inspected
        - p2: next position for 2 (from the right)
        """
        p0 = 0
        curr = 0
        p2 = len(nums) - 1

        while curr <= p2:
            if nums[curr] == 0:
                nums[p0], nums[curr] = nums[curr], nums[p0]
                p0 += 1
                curr += 1
            elif nums[curr] == 2:
                nums[curr], nums[p2] = nums[p2], nums[curr]
                p2 -= 1
                # do not increment curr here because the swapped-in element at curr
                # needs to be examined
            else:  # nums[curr] == 1
                curr += 1
```
- Notes:
  - This is the Dutch National Flag algorithm: one pass, in-place partitioning using three pointers.
  - Time complexity: O(n) — each element is examined at most once (some may be swapped but overall linear).
  - Space complexity: O(1) — only a few integer pointers used.
  - Important detail: when swapping with p2 (for value 2) we do not increment curr because the element swapped in from the end has not been examined yet. When swapping with p0 (for value 0) we increment curr because after swapping we know the element at curr (which came from p0) is either a 1 or a 0 already handled correctly by advancing curr.