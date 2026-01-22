# [Problem 3349: Adjacent Increasing Subarrays Detection I](https://leetcode.com/problems/adjacent-increasing-subarrays-detection-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to detect whether there exist two adjacent subarrays of length k that are both strictly increasing. "Adjacent" means the second starts exactly k indices after the first. A straightforward way is: for every possible start i (0 <= i <= n - 2k), check if nums[i..i+k-1] and nums[i+k..i+2k-1] are each strictly increasing. Checking each subarray directly costs O(k) per start, giving O(nk) worst-case — but we can do better.

Observation: A subarray of length k is strictly increasing iff it has k-1 consecutive adjacent pairs where nums[j] < nums[j+1]. So if we precompute for each index how many consecutive increasing adjacent-pairs start there (or equivalently, the length of the run of strictly increasing adjacent pairs), we can test each starting position in O(1).

That suggests computing an array len_inc where len_inc[i] is the number of consecutive indices t >= i such that nums[t] < nums[t+1] (i.e., how many increasing adjacent pairs beginning at i). Then a subarray starting at i is strictly increasing iff len_inc[i] >= k-1. Finally check for any i if len_inc[i] >= k-1 and len_inc[i+k] >= k-1.

## Refining the problem, round 2 thoughts
- Edge cases: constraints guarantee 2*k <= n, so there is at least one possible pair of adjacent subarrays to check. Also n up to 100 is small, but the O(n) solution is simple and optimal.
- Implementation detail: len_inc has defined values only up to n-2 (last index has no next pair), so treat len_inc[n-1] = 0.
- Alternative simpler solution: sliding window that checks strictly-increasing property with a running count of adjacent increasing pairs in each window; but the len_inc backwards DP is simpler and robust.
- Time complexity: O(n) to compute len_inc and O(n) to scan starts => O(n) total. Space: O(n) for len_inc (could be optimized to O(1) with a sliding approach but not necessary given constraints).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def findSubarrays(self, nums: List[int], k: int) -> bool:
        n = len(nums)
        # len_inc[i] = number of consecutive increasing adjacent pairs starting at i
        # valid indices for pairs are 0..n-2. For convenience create length n array.
        if n < 2 * k:
            return False  # by constraints this shouldn't happen, but safe guard

        len_inc = [0] * n
        # compute from right to left
        for i in range(n - 2, -1, -1):
            if nums[i] < nums[i + 1]:
                len_inc[i] = 1 + len_inc[i + 1]
            else:
                len_inc[i] = 0

        needed = k - 1
        # check starts i from 0 to n - 2k (inclusive)
        end = n - 2 * k
        for i in range(end + 1):
            if len_inc[i] >= needed and len_inc[i + k] >= needed:
                return True
        return False
```
- Notes about the solution:
  - Approach: Precompute len_inc (consecutive increasing adjacent pairs starting at each index). A subarray of length k is strictly increasing iff len_inc[start] >= k-1. Check for any start i whether both start and start+k satisfy this.
  - Time complexity: O(n).
  - Space complexity: O(n) for len_inc (n up to 100, trivial). Could be reduced to O(1) with a sliding-window counting adjacent increasing pairs, but this is simple and clear.