# [Problem 2270: Number of Ways to Split Array](https://leetcode.com/problems/number-of-ways-to-split-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count indices i (0 <= i < n-1) where sum(nums[0..i]) >= sum(nums[i+1..n-1]). The naive approach is computing prefix sums and suffix sums for every split — that would work but storing suffix separately is unnecessary. If I compute the total sum once, and maintain a running prefix sum while iterating i from 0 to n-2, I can compute the suffix as total - prefix. Condition becomes prefix >= total - prefix, i.e., 2*prefix >= total. That’s constant check per i. Edge cases: negatives and zeros — the inequality works the same. Also watch out for integer overflow in languages without big ints; in Python it's fine. Time O(n), space O(1) (ignoring input).

## Refining the problem, round 2 thoughts
- Only indices up to n-2 are valid (there must be at least one element on the right).
- Precompute total = sum(nums).
- Iterate prefix = 0; for i in range(n-1): prefix += nums[i]; if 2*prefix >= total: count += 1.
- Complexity: single pass, O(n) time, O(1) extra space.
- Edge cases: n = 2 -> just check i = 0. Negative numbers don't change the logic. In other languages, use 64-bit integers to avoid overflow (prefix and total up to 1e5 * 1e5 = 1e10, fits in 64-bit).
- There is no need for binary search or extra arrays.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def waysToSplitArray(self, nums: List[int]) -> int:
        total = sum(nums)
        prefix = 0
        count = 0
        # iterate splits at i where 0 <= i < n-1
        for i in range(len(nums) - 1):
            prefix += nums[i]
            # condition prefix >= total - prefix  <=>  2*prefix >= total
            if 2 * prefix >= total:
                count += 1
        return count
```
- Notes:
  - Approach: compute total sum once, maintain running prefix sum, check 2*prefix >= total for each valid split index.
  - Time complexity: O(n) — one pass over the array.
  - Space complexity: O(1) extra space (only a few variables used).
  - Implementation detail: iterate only to len(nums)-2 inclusive (range(len(nums)-1)) because split must leave at least one element on the right.
  - In languages without arbitrary-precision integers, use 64-bit types (long/long long) to avoid overflow.