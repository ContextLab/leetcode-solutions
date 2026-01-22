# [Problem 2411: Smallest Subarrays With Maximum Bitwise OR](https://leetcode.com/problems/smallest-subarrays-with-maximum-bitwise-or/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need, for each start index i, the shortest subarray starting at i whose OR equals the maximum OR achievable for any subarray starting at i (i..k for k>=i). The maximal OR from i is simply the OR of all elements from i to end. To get the minimal length that attains that OR we must extend i to include every bit that appears at or after i at least once. So for each bit (0..30), if it appears somewhere at or after i, we must include up to the earliest occurrence of that bit (the nearest index >= i where that bit is set). The minimal required end index is the maximum among those nearest occurrences of each required bit. So scanning from right to left and maintaining, for each bit, the next index where it's set seems natural.

## Refining the problem, round 2 thoughts
- We'll keep an array next_pos[0..30] initialized to INF (use n). When processing i from n-1 down to 0, update next_pos for bits set in nums[i] to i.
- After updating, compute max_pos = i (always at least current index). For every bit with next_pos[b] < INF, set max_pos = max(max_pos, next_pos[b]). Then answer[i] = max_pos - i + 1.
- Edge cases: all zeros -> no bits ever set; with the above, next_pos stays INF but max_pos starts at i so answer becomes 1, which is correct (any single zero yields the maximum 0).
- Complexity: for each i we examine 31 bits -> O(31*n) = O(n). Space O(31) extra.

This is simple, efficient, and straightforward to implement.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def smallestSubarrays(self, nums: List[int]) -> List[int]:
        n = len(nums)
        # Use n as INF (indices are in [0, n-1])
        INF = n
        # next_pos[b] = next index >= current i where bit b is set
        next_pos = [INF] * 31
        ans = [1] * n

        # process from right to left
        for i in range(n - 1, -1, -1):
            x = nums[i]
            # update next positions for bits set in nums[i]
            bit = 0
            while x:
                if x & 1:
                    next_pos[bit] = i
                bit += 1
                x >>= 1
            # for bits not covered by the while loop (higher bits), they remain as is

            # compute furthest required position among bits present anywhere >= i
            max_pos = i
            for b in range(31):
                if next_pos[b] < INF:
                    if next_pos[b] > max_pos:
                        max_pos = next_pos[b]
            ans[i] = max_pos - i + 1

        return ans
```
- Approach notes: We scan from right to left, tracking the nearest index >= i for every bit. The minimum subarray starting at i that achieves the maximal OR must include every bit that appears at or after i, so we take the farthest such index as the end.
- Time complexity: O(31 * n) = O(n) where n = len(nums).
- Space complexity: O(31) = O(1) extra space (besides the output).