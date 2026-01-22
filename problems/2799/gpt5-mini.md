# [Problem 2799: Count Complete Subarrays in an Array](https://leetcode.com/problems/count-complete-subarrays-in-an-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to count subarrays that contain every distinct value that appears anywhere in the array. First thought: compute the total number of distinct values D in the whole array. Then find subarrays whose distinct count equals D.

Brute force: for every (i, j) check distinct count — that's O(n^2) subarrays and O(n) to compute distinct -> O(n^3) naive, or O(n^2) with incremental sets but still borderline. Given n ≤ 1000, an O(n^2) solution might pass, but we can do better.

Sliding-window / two-pointer approach: for a fixed left index l, find the smallest right index r such that the window [l..r] contains all D distinct values. Once that minimal r is found, any extension r' ≥ r will also contain all D, so we can add (n - r) (or careful off-by-one) subarrays starting at l. Move l forward and update counts; r never moves left, so total movements are linear — O(n) time overall for the two pointers (plus cost for map updates). That should be efficient and simple.

## Refining the problem, round 2 thoughts
- First compute D = number of distinct elements in the entire array (use a set).
- Use two pointers l, r (r will be the next index to include; we'll use the convention that current window is [l, r-1]).
- Maintain freq map and current distinct count curD for the window.
- For each l from 0..n-1: advance r while r < n and curD < D, updating freq and curD. If after advancing you have curD == D, then the minimal right endpoint is r-1, and the number of valid subarrays starting at l is n - (r-1) = n - r + 1. Add that to answer.
- Then move l forward by decrementing freq of nums[l] and update curD if frequency drops to zero.
- Because r never moves left, r increments at most n times and l increments n times, so O(n) time plus O(U) space for frequency (U <= 2000 given constraints, or <= n distinct). Edge cases: if D == 1, every subarray counts; algorithm still handles that.

Time complexity: O(n) with two-pointer movement (amortized), or more precisely O(n + U). Space: O(U) where U is number of distinct values (<= 2000).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def countCompleteSubarrays(self, nums: List[int]) -> int:
        n = len(nums)
        # total distinct in whole array
        total_distinct = len(set(nums))
        if total_distinct == 1:
            # every subarray is complete: n*(n+1)//2
            return n * (n + 1) // 2

        # frequency array (values up to 2000 per constraints)
        max_val = 2000
        freq = [0] * (max_val + 1)
        cur_distinct = 0
        ans = 0
        r = 0  # window is [l, r-1] initially empty

        for l in range(n):
            # expand r until window has all distinct values or r reaches end
            while r < n and cur_distinct < total_distinct:
                v = nums[r]
                if freq[v] == 0:
                    cur_distinct += 1
                freq[v] += 1
                r += 1

            if cur_distinct == total_distinct:
                # r-1 is minimal right index that completes the set for this l
                # number of valid subarrays starting at l is n - (r-1) = n - r + 1
                ans += n - r + 1
            else:
                # r reached end and we don't have all distinct anymore; no further l will succeed
                # but still need to slide l to keep consistent (loop will end soon)
                pass

            # move l forward: remove nums[l] from window
            v = nums[l]
            freq[v] -= 1
            if freq[v] == 0:
                cur_distinct -= 1

        return ans
```
- Notes:
  - We first compute total distinct D. Using two pointers we maintain a sliding window [l, r-1] and expand r until the window contains all D distinct values (if possible).
  - For each left l, once we find the minimal r such that [l..r-1] contains all distinct values, every extension to the right (r-1, r, ..., n-1) also contains all D distinct values, contributing n - (r-1) subarrays starting at l.
  - r never moves left, so each index is visited at most once by r and once by l: time O(n). Space is O(U) where U is number of distinct values (bounded by 2000 per constraints).
  - Edge case: if the total distinct is 1, we quickly return n*(n+1)//2 since every subarray qualifies. The general algorithm would also handle it but this is a small optimization.