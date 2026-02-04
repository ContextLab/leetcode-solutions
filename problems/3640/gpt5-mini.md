# [Problem 3640: Trionic Array II](https://leetcode.com/problems/trionic-array-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need a contiguous subarray nums[l..r] that can be partitioned into three contiguous parts:
- nums[l..p] strictly increasing,
- nums[p..q] strictly decreasing,
- nums[q..r] strictly increasing,
with l < p < q < r. We want the maximum sum of such a subarray.

This is essentially a "up-down-up" pattern (rise, fall, rise) inside a contiguous slice. Each of the three pieces is itself a contiguous monotone segment. A natural approach is to precompute info about maximal increasing segments ending at each index (left) and starting at each index (right), together with their sums. Then consider every possible middle strictly-decreasing segment [p..q] and combine the best left-increasing ending at p and right-increasing starting at q. The subarray sum can be expressed via prefix sums; algebra shows we can rearrange it so for a fixed q we only need the maximum value of a function of p among p in the same decreasing run with p < q. That allows a linear sweep across maximal decreasing runs maintaining the best p-value so far. Complexity should be O(n).

## Refining the problem, round 2 thoughts
Important details and constraints:
- Each increasing piece must contain at least two indices (because l < p and q < r), so left-increasing length at p must be >= 2 and right-increasing length at q must be >= 2.
- The middle decreasing piece must have p < q (length >= 2).
- We can decompose sum(nums[l..r]) as left_sum[p] + sum(nums[p..q]) + right_sum[q] - nums[p] - nums[q] because left_sum and right_sum include p and q respectively while the middle includes both; subtracting once each prevents double counting.
- Using prefix sums pre[k] (sum up to index k-1), sum(nums[p..q]) = pre[q+1] - pre[p]. So the total becomes:
  left_sum[p] - pre[p+1]  +  (pre[q+1] + right_sum[q] - nums[q]).
  For a fixed q, the second term is known; we only need the maximum value of left_sum[p] - pre[p+1] among valid p in the same decreasing run with p < q and left_len[p] >= 2.
- So iterate the array, find maximal strictly-decreasing runs; for each run, sweep q from start+1..end, updating best p-value with p = q-1 as we go; if right_len[q] >= 2 and best exists, compute candidate sum and update answer.

Time O(n), space O(n) for arrays and prefix sums. Handle large sums using Python ints. The problem guarantees at least one valid trionic subarray exists.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        n = len(nums)
        # prefix sums: pre[i] = sum of nums[0..i-1]
        pre = [0] * (n + 1)
        for i in range(n):
            pre[i+1] = pre[i] + nums[i]

        # left_len[i]: length of longest strictly increasing contiguous subarray ending at i
        # left_sum[i]: sum of that subarray
        left_len = [1] * n
        left_sum = [0] * n
        for i in range(n):
            if i > 0 and nums[i-1] < nums[i]:
                left_len[i] = left_len[i-1] + 1
                left_sum[i] = left_sum[i-1] + nums[i]
            else:
                left_len[i] = 1
                left_sum[i] = nums[i]

        # right_len[i]: length of longest strictly increasing contiguous subarray starting at i
        # right_sum[i]: sum of that subarray
        right_len = [1] * n
        right_sum = [0] * n
        for i in range(n-1, -1, -1):
            if i < n-1 and nums[i] < nums[i+1]:
                right_len[i] = right_len[i+1] + 1
                right_sum[i] = right_sum[i+1] + nums[i]
            else:
                right_len[i] = 1
                right_sum[i] = nums[i]

        ans = -10**30  # sufficiently small
        i = 0
        # iterate over maximal strictly decreasing runs
        while i < n - 1:
            if nums[i] <= nums[i+1]:
                i += 1
                continue
            # start of decreasing run
            s = i
            j = i
            while j + 1 < n and nums[j] > nums[j+1]:
                j += 1
            e = j  # run is s..e (inclusive), length >= 2
            # sweep q from s+1..e, maintaining best value of (left_sum[p] - pre[p+1]) among p in [s..q-1] with left_len[p] >= 2
            best = None  # store max value or None
            for q in range(s+1, e+1):
                p = q - 1
                if left_len[p] >= 2:
                    val = left_sum[p] - pre[p+1]
                    if best is None or val > best:
                        best = val
                # candidate only valid if there exists a valid p (best not None) and right_len[q] >= 2 (q<r)
                if best is not None and right_len[q] >= 2:
                    candidate = best + pre[q+1] + right_sum[q] - nums[q]
                    if candidate > ans:
                        ans = candidate
            i = e + 1

        return ans
```
- Notes about the approach:
  - Precompute prefix sums, left-increasing sums/lengths, and right-increasing sums/lengths in O(n).
  - Scan the array to find maximal strictly-decreasing runs. For each run, sweep the end index q in increasing order; for each q, maintain the best value of left_sum[p] - pre[p+1] among valid p < q. This produces candidate trionic sums in O(1) per index, so overall O(n).
  - We required left_len[p] >= 2 and right_len[q] >= 2 to satisfy l < p and q < r constraints (each increasing segment must have at least two indices).
- Complexity:
  - Time: O(n)
  - Space: O(n) (prefix sums and auxiliary arrays)
- Implementation details:
  - Uses Python integers for sums (safe for large values).
  - Assumes at least one trionic subarray exists (per problem statement), so ans will be set accordingly. If not guaranteed, you'd need to handle ans initial value and absence of valid candidate.