# [Problem 962: Maximum Width Ramp](https://leetcode.com/problems/maximum-width-ramp/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Brute force is obvious: check all pairs (i, j) with i < j and nums[i] <= nums[j], track max j-i — but that's O(n^2) and will time out for n up to 5e4. We need something near O(n log n) or O(n).

I recall a common pattern: keep candidate left indices that are "useful" — those with small values and earlier positions. If we keep indices of a strictly decreasing sequence of nums (as we scan left to right), each index in that stack is a potential left end because any later index with a value >= that left value can form a ramp. Then scan from the right to find farthest j that satisfies nums[j] >= nums[i], popping as we succeed and updating width. That gives O(n) time because each index is pushed and popped at most once.

Alternative: sort pairs (value, index) by value and then track min index seen so far while scanning ascending values — O(n log n). The monotonic stack + right-to-left scan is nicer and linear time & space.

Edge cases: totally decreasing array -> result 0; equal values repeated -> can get large width.

## Refining the problem, round 2 thoughts
Refine stack idea: build a stack of indices i such that nums[i] is strictly decreasing as indices increase. Implementation detail: iterate i from 0..n-1, push i if stack is empty or nums[i] < nums[stack[-1]] (strict to avoid useless larger/equal left indices since an earlier equal value is always better). Then iterate j from n-1 down to 0: while stack not empty and nums[j] >= nums[stack[-1]], compute width (j - stack[-1]) and pop that index (since we've found the farthest j for that i when scanning from rightmost first). Keep max width. Complexity: each index pushed/popped at most once -> O(n) time, O(n) space for stack.

Corner cases: if we use strict < when building stack, equal values keep the earlier index only, which is correct (earlier index yields larger or equal width). If we used <=, we'd keep later equal indices which are worse. Make sure to pop and update width in correct order scanning j from right to left; scanning from left wouldn't guarantee farthest j for each i.

Now produce code.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxWidthRamp(self, nums: List[int]) -> int:
        n = len(nums)
        stack = []
        # Build a stack of candidate left indices with strictly decreasing values
        for i in range(n):
            if not stack or nums[i] < nums[stack[-1]]:
                stack.append(i)
        
        max_width = 0
        # Scan from right to left to find farthest j for each candidate i
        for j in range(n - 1, -1, -1):
            # While current j can form a ramp with the top candidate i, update and pop
            while stack and nums[j] >= nums[stack[-1]]:
                i = stack.pop()
                max_width = max(max_width, j - i)
                # early exit: if stack empty or possible max width smaller than current j,
                # but we already pop until nums[j] < nums[stack[-1]] so it's fine
        return max_width
```
- Notes on approach:
  - We first collect indices i that could possibly start a maximum-width ramp: those where nums[i] is strictly smaller than all previous values seen (so indices form a strictly decreasing-by-value sequence). This guarantees we only keep the best left candidates.
  - Then scanning j from right-to-left ensures that when nums[j] >= nums[i], j is the farthest possible for that i among remaining j's, so we can safely compute j - i and pop i.
  - Time complexity: O(n) — each index is pushed at most once and popped at most once.
  - Space complexity: O(n) worst-case for the stack.