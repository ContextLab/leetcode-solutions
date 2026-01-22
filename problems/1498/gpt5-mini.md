# [Problem 1498: Number of Subsequences That Satisfy the Given Sum Condition](https://leetcode.com/problems/number-of-subsequences-that-satisfy-the-given-sum-condition/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count subsequences (not necessarily contiguous) where min + max <= target. For subsequences, any elements between min and max can be chosen arbitrarily, so if I fix a minimum element value at some index i and a maximum element value at index j (with nums[i] <= nums[j]), then every subset of elements strictly between them can be chosen or not. Sorting the array will make it easy to reason about min and max: the smallest chosen element will come from the left and the largest from the right. A two-pointer approach comes to mind: sort nums, use left and right pointers; if nums[left] + nums[right] <= target, then any choice of the elements between left and right (each either included or not) gives 2^(right-left) valid subsequences where left is the min and right is the max (and also the case where left==right is counted as single-element subsequence since 2^0 = 1). If the sum is too large, decrement right. Precompute powers of two modulo 10^9+7 to get counts quickly.

## Refining the problem, round 2 thoughts
- Sorting costs O(n log n). Two-pointer scan is O(n) after sorting. Precomputing powers is O(n).
- Edge cases: handle when r < l (stop or continue); single-element subsequences are counted since min==max and that sum is 2*value which can be <= target.
- Need modulo 10^9+7. Precompute pow2[i] = 2^i % MOD for i in [0..n].
- Space: O(n) extra for pow2 (can be optimized to O(1) by updating powers on the fly if needed, but O(n) is fine for n up to 1e5).
- Time complexity O(n log n) and space O(n).
- Make sure to break out when r becomes < l to avoid negative indices.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def numSubseq(self, nums: List[int], target: int) -> int:
        MOD = 10**9 + 7
        nums.sort()
        n = len(nums)
        pow2 = [1] * (n + 1)
        for i in range(1, n + 1):
            pow2[i] = (pow2[i-1] * 2) % MOD

        ans = 0
        l, r = 0, n - 1
        while l <= r:
            if nums[l] + nums[r] <= target:
                # For current l and r, any subset of elements between them
                # can be chosen or not: 2^(r-l) options
                ans = (ans + pow2[r - l]) % MOD
                l += 1
            else:
                # sum too big, decrease r to try smaller max
                r -= 1

        return ans
```
- Notes:
  - Approach: sort + two pointers + precomputed powers of two.
  - Correctness: For fixed smallest element at index l and largest allowed at index r (with nums[l]+nums[r] <= target), every subset of the r-l elements between them (inclusive of picking none) leads to a valid subsequence where the chosen smallest is nums[l] and the chosen largest is at most nums[r]. Counting 2^(r-l) accounts for all subsequences that include nums[l] and whose maximum index is ≤ r.
  - Time complexity: O(n log n) due to sorting + O(n) two-pointer scan.
  - Space complexity: O(n) for pow2 (plus O(1) extra pointers).