# [Problem 2762: Continuous Subarrays](https://leetcode.com/problems/continuous-subarrays/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to count subarrays where every pair of elements has absolute difference at most 2. That means for any subarray the maximum and minimum values differ by at most 2 (range <= 2). A naive approach would check every subarray and compute min/max, which is O(n^2) or O(n^2 log n) and too slow for n up to 1e5.

A common pattern for "count subarrays with a constraint on the range" is to use a sliding-window (two pointers) and maintain the current window's min and max efficiently. Monotonic deques (one for maxima and one for minima) can provide O(1) amortized updates to get current max and min, allowing an O(n) total solution. For each right index, we'd find the smallest left such that range <= 2, and add the number of valid subarrays ending at right (right - left + 1).

## Refining the problem, round 2 thoughts
- Maintain two deques storing indices in decreasing order for max and increasing order for min.
- Expand right pointer; insert new element updating both deques.
- While current max - min > 2, move left pointer up, and pop indices from deques if they fall out of the window.
- For each right, all subarrays starting at any index between left and right and ending at right are valid; add (right-left+1) to the answer.
- Edge cases: single-element arrays, all equal elements, strictly increasing/decreasing. Values may be up to 1e9 but only comparisons matter.
- Complexity: each index enters and exits each deque at most once => O(n) time, O(n) space.

## Attempted solution(s)
```python
from collections import deque
from typing import List

class Solution:
    def continuousSubarrays(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0

        maxd = deque()  # indices of candidates for maximum, decreasing by value
        mind = deque()  # indices of candidates for minimum, increasing by value
        left = 0
        res = 0

        for right, val in enumerate(nums):
            # maintain max deque (decreasing)
            while maxd and nums[maxd[-1]] < val:
                maxd.pop()
            maxd.append(right)

            # maintain min deque (increasing)
            while mind and nums[mind[-1]] > val:
                mind.pop()
            mind.append(right)

            # shrink window until range <= 2
            while nums[maxd[0]] - nums[mind[0]] > 2:
                # if the left index is at the front of either deque, pop it
                if maxd and maxd[0] == left:
                    maxd.popleft()
                if mind and mind[0] == left:
                    mind.popleft()
                left += 1

            # all subarrays ending at right with start in [left, right] are valid
            res += (right - left + 1)

        return res
```
- Approach: sliding window with two monotonic deques tracking current window's max and min. For each right index, we shrink left until max-min <= 2, then add count of valid subarrays ending at right.
- Time complexity: O(n) amortized, each element is pushed/popped at most once from each deque.
- Space complexity: O(n) worst-case for the deques (typically much smaller).
- Implementation details: store indices in deques so we can compare and remove elements that go out of the window by checking index == left. The result fits in Python int (up to ~n*(n+1)/2).