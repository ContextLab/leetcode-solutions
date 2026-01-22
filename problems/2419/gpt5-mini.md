# [Problem 2419: Longest Subarray With Maximum Bitwise AND](https://leetcode.com/problems/longest-subarray-with-maximum-bitwise-and/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
At first glance this looks like a bitwise problem where we might need to consider ANDs over many subarrays or try some two-pointer / segment technique. One could try to compute ANDs progressively or maintain candidate ANDs for windows. But there's a simpler observation: the AND of a subarray is always less than or equal to every element in that subarray. So the maximum possible AND over all subarrays cannot exceed the maximum element in the array. A single-element subarray achieves the value of that element, so the global maximum achievable AND is simply max(nums). That simplifies the problem massively: we only need to find the longest contiguous subarray whose AND equals that maximum value.

Now: for a subarray's AND to equal max_val, every element in the subarray must contribute all the bits of max_val. Since no element can be greater than max_val, any element that has all bits of max_val must be equal to max_val. Thus the condition reduces to contiguous runs of elements equal to max(nums).

## Refining the problem, round 2 thoughts
So algorithm is straightforward:
- Find m = max(nums).
- Scan the array counting consecutive elements equal to m; track the maximum run length.
Edge cases:
- Single element array.
- All elements equal (answer = n).
- No adjacent equal maxima (answer = 1 if max appears).
Time complexity O(n) and O(1) extra space.

This avoids any heavy bitwise window logic and is optimal.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def longestSubarray(self, nums: List[int]) -> int:
        # Find the maximum value in the array
        m = max(nums)
        # Track current run length of values equal to m and best (maximum) run length
        cur = 0
        best = 0
        for x in nums:
            if x == m:
                cur += 1
                if cur > best:
                    best = cur
            else:
                cur = 0
        return best
```
- Notes:
  - Approach: compute the global maximum m, then return the length of the longest contiguous sequence of elements equal to m.
  - Time complexity: O(n) to scan the array twice at most (one for max, one for counting) — actually combined into one if desired but current form is two passes: O(n).
  - Space complexity: O(1) extra space.
  - Correctness justification: the AND of any subarray is ≤ each element in it, so the maximal possible AND is max(nums). For a subarray to have AND equal to max(nums), every element in that subarray must have all bits of max(nums); given elements ≤ max(nums), they must be equal to max(nums). Hence contiguous runs of max(nums) are exactly the valid subarrays.