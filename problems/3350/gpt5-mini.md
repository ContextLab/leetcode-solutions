# [Problem 3350: Adjacent Increasing Subarrays Detection II](https://leetcode.com/problems/adjacent-increasing-subarrays-detection-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the largest k such that there exist two adjacent subarrays of length k that are each strictly increasing. A subarray of length k starting at i is strictly increasing iff each consecutive pair inside it increases, which is equivalent to the "longest strictly increasing run starting at i" being at least k.

So if I precompute, for each index i, the maximum length L_i of a strictly increasing subarray starting at i, then the condition for a given k is: exists i such that L_i >= k and L_{i+k} >= k (and i+k is a valid start, so i <= n-2k). That becomes a membership check over indices. We can then binary search on k (1..n//2) and check feasibility in O(n) per k using the precomputed L array. That yields O(n log n) total. Alternatively, could try a two-pointer or greedy scan to derive maximal k in one pass, but binary search is simple and safe.

Edge cases: k=1 is always possible for n>=2 because single-element subarray counts as strictly increasing. Need to be careful computing L at array end.

## Refining the problem, round 2 thoughts
Compute L (let's call it inc_start) by scanning from right to left:
- inc_start[n-1] = 1
- for i from n-2 down to 0:
    - if nums[i] < nums[i+1]: inc_start[i] = inc_start[i+1] + 1
    - else inc_start[i] = 1

Binary search k between 1 and n//2. For each k, check i from 0 to n-2k inclusive to see if inc_start[i] >= k and inc_start[i+k] >= k. If any index satisfies, k is feasible.

Time: O(n log n). Space: O(n) for inc_start. n up to 2e5 so this is fine.

Alternative: Could precompute a boolean array for each k? Not efficient. Or compute max feasible k by scanning increasing runs and using their lengths to decide how many adjacent blocks you can form, but that gets a bit trickier and binary search is clean.

Corner cases: equal elements break increasing runs. Single-element runs count as length 1. We must ensure indices when checking i+k exist (i+k <= n-k).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxK(self, nums: List[int]) -> int:
        n = len(nums)
        # inc_start[i] = length of longest strictly increasing subarray starting at i
        inc_start = [1] * n
        for i in range(n - 2, -1, -1):
            if nums[i] < nums[i + 1]:
                inc_start[i] = inc_start[i + 1] + 1
            else:
                inc_start[i] = 1

        def feasible(k: int) -> bool:
            # need i in [0, n-2k] such that inc_start[i] >= k and inc_start[i+k] >= k
            limit = n - 2 * k
            if limit < 0:
                return False
            for i in range(limit + 1):
                if inc_start[i] >= k and inc_start[i + k] >= k:
                    return True
            return False

        lo, hi = 1, n // 2
        ans = 0
        while lo <= hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1
        return ans
```
- Notes about the solution:
  - Approach: precompute longest increasing run starting at each index, then binary search the largest k; checking a k is an O(n) scan using the precomputed array.
  - Time complexity: O(n log n) due to binary search with an O(n) feasibility check per step.
  - Space complexity: O(n) for the inc_start array.
  - Implementation details: inc_start counts number of elements in the increasing run (so a single element gives 1). For checking adjacency, ensure i ranges up to n-2k inclusive so both subarrays fully fit. This handles corner cases like equal neighboring values (which reset runs).