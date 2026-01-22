# [Problem 3381: Maximum Subarray Sum With Length Divisible by K](https://leetcode.com/problems/maximum-subarray-sum-with-length-divisible-by-k/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Sorry — I can’t share stream-of-consciousness reasoning. I can, however, give a concise summary of the key idea:

- Use prefix sums. A subarray from l to r-1 has length r-l. That length is divisible by k exactly when r % k == l % k. So among prefix-sum indices with the same index mod k, the best subarray ending at r is P[r] - (minimum prefix P[l] previously seen with l % k == r % k). Maintain the minimum prefix sum seen per modulo class and compute the best difference.

## Refining the problem, round 2 thoughts
- Maintain prefix sum P as we iterate through indices i = 1..n (prefix index 0 for empty prefix).
- Keep an array min_prefix of size k where min_prefix[m] is the minimum prefix sum seen so far among prefix indices whose index % k == m.
- Initialize min_prefix[0] = 0 (prefix index 0) and other entries to +inf.
- For each index i (1-based for prefix), compute P, m = i % k. If min_prefix[m] is finite, candidate = P - min_prefix[m] updates answer. Then update min_prefix[m] = min(min_prefix[m], P).
- Ensure candidate is computed before updating min_prefix[m] with P to avoid using the same prefix index (would make subarray length 0).
- Time O(n), space O(k). Works with negative numbers and large values.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxSubarraySumDivByK(self, nums: List[int], k: int) -> int:
        # prefix sum
        prefix = 0
        # min_prefix[m] = minimum prefix sum seen so far at indices with index % k == m
        INF = 10**30
        min_prefix = [INF] * k
        min_prefix[0] = 0  # prefix index 0 has sum 0 and 0 % k == 0

        ans = -INF
        # iterate using 1-based prefix index: after processing nums[0..i-1], prefix is P[i]
        for i, x in enumerate(nums, start=1):
            prefix += x
            m = i % k
            # if there's an earlier prefix with same mod, we can form a valid non-empty subarray
            if min_prefix[m] != INF:
                ans = max(ans, prefix - min_prefix[m])
            # update minimum prefix for this modulo class
            if prefix < min_prefix[m]:
                min_prefix[m] = prefix

        return ans
```
- Approach: Use prefix sums and group prefix indices by index % k. For each prefix P[r], the best subarray ending at r with length divisible by k is P[r] - min_prefix[r % k].
- Time complexity: O(n) where n = len(nums) — single pass.
- Space complexity: O(k) for min_prefix array.
- Implementation details: Use 1-based prefix index so prefix at step i corresponds to sum of nums[:i]. Initialize min_prefix[0] = 0 to allow subarrays starting at index 0. Compute candidate before updating min_prefix to ensure non-empty subarrays.