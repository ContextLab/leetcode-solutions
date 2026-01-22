# [Problem 3152: Special Array II](https://leetcode.com/problems/special-array-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
[We need to check for each query whether every adjacent pair in the subarray has different parity. That means no two consecutive numbers in the subarray can both be even or both be odd. For many queries, recomputing pairwise parity checks per query would be too slow if done naively. Precomputation sounds appropriate: for each adjacent pair in the whole array we can mark whether that pair is "bad" (same parity). Then a subarray is special iff the number of bad adjacent pairs inside the subarray is zero. That suggests building a prefix-sum array over the "bad" flags so each query reduces to a constant-time range sum check. Also remember subarrays of length 1 are vacuously special because they have no adjacent pair to violate the condition.]

## Refining the problem, round 2 thoughts
[Define bad[i] = 1 if nums[i] and nums[i+1] have the same parity, else 0, for i in [0..n-2]. Then prefix pref where pref[0]=0 and pref[k+1]=pref[k]+bad[k]. For a query [l,r], the pairs inside the subarray correspond to indices l..r-1 in bad; their sum is pref[r]-pref[l]. The subarray is special iff pref[r]-pref[l] == 0. Time complexity: O(n + q). Space: O(n) for the prefix (or O(n-1) for bad). Edge cases: single-element subarrays (l==r) should return True since no pairs exist; the above formula returns 0 so it's handled automatically.]

## Attempted solution(s)
```python
from typing import List

class Solution:
    def isSpecialArray(self, nums: List[int], queries: List[List[int]]) -> List[bool]:
        """
        Return a list of booleans where each boolean indicates whether nums[l..r] is special:
        every adjacent pair in the subarray has different parity.
        """
        n = len(nums)
        if n == 0:
            return [True] * len(queries)  # defensive, though constraints say n >= 1

        # bad[i] = 1 if nums[i] and nums[i+1] have same parity, else 0, for i in [0..n-2]
        # Build prefix sum pref where pref[k] = sum of bad[0..k-1], pref has length n
        pref = [0] * n  # pref[0] = 0, pref[1] = bad[0], ...
        for i in range(n - 1):
            same_parity = (nums[i] & 1) == (nums[i+1] & 1)
            pref[i+1] = pref[i] + (1 if same_parity else 0)

        ans: List[bool] = []
        for l, r in queries:
            # number of bad adjacent pairs in nums[l..r] is pref[r] - pref[l]
            bad_count = pref[r] - pref[l]
            ans.append(bad_count == 0)
        return ans
```
- Notes on approach:
  - We precompute whether each adjacent pair in nums has the same parity (bad pairs) and accumulate them in a prefix-sum array.
  - For query [l, r], the relevant adjacent pairs are indices l..r-1, whose count of bad pairs equals pref[r] - pref[l]. If that count is zero, the subarray is special.
- Complexity:
  - Time: O(n + q), where n = len(nums) and q = len(queries). Building the prefix takes O(n), each query is answered in O(1).
  - Space: O(n) extra for the prefix array (can be O(n-1) logically).