# [Problem 1671: Minimum Number of Removals to Make Mountain Array](https://leetcode.com/problems/minimum-number-of-removals-to-make-mountain-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I recognize this as a problem about forming a mountain — strictly increasing up to a peak and then strictly decreasing. A common way to reason about such problems is to compute the longest increasing subsequence (LIS) ending at each index and the longest decreasing subsequence (LDS) starting at each index. If I know those two values for every index i, then any valid mountain with peak i has length left[i] + right[i] - 1 (counting i once). The answer is n - max_mountain_length.

Brute-force DP (O(n^2)) for LIS/LDS would work for n up to 1000 but can be improved to O(n log n) using patience sorting / tails + binary search to get LIS lengths for each position. I should be careful about strictness (values equal are not allowed in strictly increasing/decreasing parts), so the LIS computation must enforce strict increasing behavior.

## Refining the problem, round 2 thoughts
- Compute left[i] = length of longest strictly increasing subsequence ending at i.
- Compute right[i] = length of longest strictly decreasing subsequence starting at i. To compute right efficiently, reverse the array and compute LIS there (strictly increasing), then map lengths back.
- Use patience algorithm (tails array + bisect_left) to compute LIS length ending at each index in O(n log n).
  - Using bisect_left on tails enforces strictly increasing subsequences (equal elements replace, not extend).
- A valid peak i must have left[i] > 1 and right[i] > 1 (there must be at least one element on each side). Compute max_len = max(left[i] + right[i] - 1) for valid peaks.
- Answer = n - max_len.
- Complexity: O(n log n) time, O(n) extra space. n ≤ 1000 so O(n^2) would pass, but O(n log n) is cleaner and efficient.

Edge cases:
- If no index has left[i] > 1 and right[i] > 1 it means no valid mountain, but the problem guarantees we can make a mountain array so there's at least one valid peak.
- Equal adjacent values are not allowed as strict increases/decreases, handled by bisect_left behavior.

## Attempted solution(s)
```python
from bisect import bisect_left
from typing import List

class Solution:
    def minimumMountainRemovals(self, nums: List[int]) -> int:
        n = len(nums)
        if n < 3:
            return 0  # not really required by constraints, but safe
        
        # Helper to compute LIS lengths ending at each index (strictly increasing)
        def lis_lengths(arr: List[int]) -> List[int]:
            tails = []        # tails[k] = smallest tail value of an increasing subsequence of length k+1
            lengths = [0] * len(arr)
            for i, x in enumerate(arr):
                pos = bisect_left(tails, x)  # position where x fits (strictly increasing)
                if pos == len(tails):
                    tails.append(x)
                else:
                    tails[pos] = x
                lengths[i] = pos + 1
            return lengths
        
        # left[i] = length of longest strictly increasing subsequence ending at i
        left = lis_lengths(nums)
        
        # right[i] = length of longest strictly decreasing subsequence starting at i
        # compute LIS on reversed array and map back
        rev_lengths = lis_lengths(nums[::-1])
        right = rev_lengths[::-1]
        
        # Find best mountain peak (must have increasing part and decreasing part > 1)
        max_mountain = 0
        for i in range(n):
            if left[i] > 1 and right[i] > 1:
                max_mountain = max(max_mountain, left[i] + right[i] - 1)
        
        return n - max_mountain
```

- Notes about the approach:
  - We compute LIS lengths from the left and LIS lengths from the reversed array to get longest decreasing subsequences from the right.
  - We require left[i] > 1 and right[i] > 1 because the peak cannot be at the ends and must have at least one element on both sides.
  - Time complexity: O(n log n) due to the patience-sort style LIS computation.
  - Space complexity: O(n) for storing lengths and temporary tails arrays.