# [Problem 3867: Sum of GCD of Formed Pairs](https://leetcode.com/problems/sum-of-gcd-of-formed-pairs/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need prefixGcd[i] = gcd(nums[i], max(nums[0..i])). The max as we move from left to right is non-decreasing, so we can maintain the current max and compute gcd(nums[i], cur_max) in O(1) per element (gcd cost is small). After building prefixGcd, we sort it and then form floor(n/2) pairs by matching smallest with largest, next-smallest with next-largest, etc., computing gcd for each pair and summing. Sorting dominates complexity: O(n log n). Edge case: if n is odd, middle element remains unused.

I briefly considered more exotic counting/frequency-based approaches to avoid sorting, but since values can be up to 1e9 and n is only up to 1e5, sorting is fine and simple.

## Refining the problem, round 2 thoughts
Concrete steps:
- One pass to build prefixGcd using a running max: cur_max = max(cur_max, nums[i]); prefixGcd[i] = gcd(nums[i], cur_max).
- Sort prefixGcd.
- Two-pointer pair formation: left = 0, right = n-1; while left < right: ans += gcd(prefixGcd[left], prefixGcd[right]); left += 1; right -= 1.
- Return ans.

Edge cases:
- n = 1 => no pairs => return 0.
- Values up to 1e9; Python's math.gcd handles that efficiently.
Time/space:
- Time: O(n log n) due to sort. gcd computations add O(n) cheap operations.
- Space: O(n) for prefixGcd.

This is straightforward and efficient for constraints.

## Attempted solution(s)
```python
from typing import List
from math import gcd

class Solution:
    def sumOfGcdOfFormedPairs(self, nums: List[int]) -> int:
        """
        Build prefixGcd[i] = gcd(nums[i], max(nums[:i+1])), sort it,
        pair smallest with largest, sum up gcds of each pair.
        """
        n = len(nums)
        if n <= 1:
            return 0

        prefix = []
        cur_max = 0
        for x in nums:
            if x > cur_max:
                cur_max = x
            prefix.append(gcd(x, cur_max))

        prefix.sort()
        i, j = 0, n - 1
        total = 0
        while i < j:
            total += gcd(prefix[i], prefix[j])
            i += 1
            j -= 1

        return total
```
- Notes:
  - Approach: one pass to compute prefix gcds with running maximum, then sort and two-pointer pairing.
  - Time complexity: O(n log n) (dominant sorting). Each gcd is O(log M) where M <= 1e9, so practically constant per call.
  - Space complexity: O(n) for the prefix list.
  - Handles n odd by stopping when left >= right; the middle element (if any) is ignored as required.