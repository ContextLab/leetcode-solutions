# [Problem 2654: Minimum Number of Operations to Make All Array Elements Equal to 1](https://leetcode.com/problems/minimum-number-of-operations-to-make-all-array-elements-equal-to-1/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
If any element is already 1, we can use it to make neighbors 1 by taking gcd(1, x) = 1, so we can "spread" the 1 across the array. Each non-1 element needs one operation to become 1 when there's at least one 1, so I think answer = n - (# of ones) in that case.

If there are no ones, we need to create a 1 first. Creating a 1 requires finding a contiguous subarray whose gcd is 1; reducing that subarray to a single 1 takes some operations. For a subarray of length L whose gcd is 1, I recall it takes L-1 operations to produce a 1 inside it (by repeatedly taking gcd of adjacent elements). Once we have a single 1, we then need to spread it to the remaining n-1 elements, which costs n-1 operations. So total would be (L-1) + (n-1) = n + L - 2. If no subarray has gcd 1, it's impossible.

So algorithm: count ones -> if any, return n - count_ones. Otherwise, find minimal L such that gcd of subarray = 1 (O(n^2) with gcd updates). If none -> -1. Else return n + L - 2.

## Refining the problem, round 2 thoughts
- Edge cases:
  - Already contains multiple 1s -> formula n - count_ones still holds.
  - Entire array gcd > 1 -> impossible.
  - n up to 50, so O(n^2 logA) (gcd updates) is fine.
- Implementation detail: while scanning subarrays, if running gcd becomes 1 we can break the inner loop for that start index because extending only increases length.
- Complexity: We'll compute gcd pairwise cumulatively to avoid recomputing from scratch; use math.gcd.
- No tricky memory requirements.

## Attempted solution(s)
```python
from math import gcd
from typing import List

class Solution:
    def minOperations(self, nums: List[int]) -> int:
        n = len(nums)
        # Count existing ones
        ones = sum(1 for x in nums if x == 1)
        if ones > 0:
            return n - ones
        
        # Find minimal subarray length with gcd == 1
        min_len = float('inf')
        for i in range(n):
            g = nums[i]
            if g == 1:
                min_len = 1
                break
            for j in range(i + 1, n):
                g = gcd(g, nums[j])
                if g == 1:
                    min_len = min(min_len, j - i + 1)
                    break  # no need to extend this start further
        
        if min_len == float('inf'):
            return -1
        
        # To create the first 1 takes (min_len - 1) operations,
        # then spreading that 1 to the remaining n-1 elements takes (n - 1) operations.
        return (min_len - 1) + (n - 1)
```
- Notes on approach:
  - If there is at least one 1 in nums, we need exactly one operation per non-1 to convert it to 1 using adjacent gcd with a 1, so answer = n - count_ones.
  - If no 1 exists, find the shortest contiguous segment whose gcd is 1 (length L). It takes L-1 operations to reduce that segment to a single 1, then n-1 operations to propagate that 1 to all elements. Total = n + L - 2.
- Time complexity: O(n^2 * logA) where n = len(nums) (<=50) and logA is cost of gcd on values up to 1e6. Practically O(n^2).
- Space complexity: O(1) extra space.