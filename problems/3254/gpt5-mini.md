# [Problem 3254: Find the Power of K-Size Subarrays I](https://leetcode.com/problems/find-the-power-of-k-size-subarrays-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the "power" of every k-length subarray: it's the maximum element if the elements are consecutive and sorted ascending, otherwise -1. Sorted ascending and consecutive means the window must look like x, x+1, x+2, ..., x+k-1. That implies every adjacent difference must equal 1. So for k>=2 we can just check the k-1 adjacent differences inside each window. If all are 1, the max is the last element of the window (since sorted ascending), otherwise -1. For k==1 every single element trivially satisfies this and the power is the element itself.

A naive approach would check each window in O(k), resulting in O(n*k) time. But we can do better: precompute boolean indicators for adjacent differences equal to 1, then use a sliding-window sum (or prefix sums) over that boolean array to check in O(1) per window whether all k-1 differences are 1. That yields O(n) time.

## Refining the problem, round 2 thoughts
- Edge case: k == 1 → return the elements themselves.
- For k >= 2:
  - Create diffs array of length n-1: diffs[i] = 1 if nums[i+1] - nums[i] == 1 else 0.
  - For each window starting at i, check sum(diffs[i..i+k-2]) == k-1. Use a running sum to update in O(1) per window.
  - If true, window is x..x+k-1 and the max is nums[i+k-1], otherwise -1.
- Complexity: O(n) time, O(n) extra space (diffs + output). With n <= 500 this is trivial memory-wise but approach scales nicely.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def power(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        # k == 1: every single element is trivially consecutive+sorted
        if k == 1:
            return nums[:]  # each element is its own power

        # build boolean diffs: 1 if next - current == 1, else 0
        diffs = [1 if nums[i+1] - nums[i] == 1 else 0 for i in range(n-1)]

        res = []
        # initial window sum of length k-1 in diffs
        need = k - 1
        cur = sum(diffs[:need])  # safe because k <= n -> need <= n-1

        for i in range(0, n - k + 1):
            if i > 0:
                # slide: remove diffs[i-1], add diffs[i+need-1]
                cur += diffs[i + need - 1] - diffs[i - 1]
            # if all k-1 diffs are 1, window is consecutive ascending
            if cur == need:
                res.append(nums[i + k - 1])  # max element in ascending window
            else:
                res.append(-1)
        return res
```
- Approach: Convert adjacent checks into a boolean array and use a sliding-window sum to test whether all adjacent differences in each k-window equal 1. If yes, the window is consecutive ascending and the power is the window's last (maximum) element; otherwise -1.
- Time complexity: O(n) — building diffs and scanning windows once.
- Space complexity: O(n) extra (diffs array and output array). If desired, diffs could be computed on the fly for O(1) extra but current solution is clear and efficient.