# [Problem 3356: Zero Array Transformation II](https://leetcode.com/problems/zero-array-transformation-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We can choose for each index, independently across queries, how much to decrement (up to val for each query that covers that index). So after processing the first k queries, the total amount we can possibly decrement index j by equals the sum of val_i over those queries among the first k whose ranges include j. To make nums a zero array we need, for every index j, that this total available decrement >= nums[j]. Thus the feasibility of a given k reduces to checking whether the coverage-sum per index (using the first k queries) is >= nums element-wise.

This suggests checking k by computing coverage per index. Since queries are range adds, we can use a difference array to apply the first k queries in O(k + n) time and then prefix-sum to get per-index coverage. We want the minimum k, so binary search on k in [0, m] (m = number of queries) is natural — each feasibility check is monotonic (if k works, any larger k also works), so binary search is valid.

## Refining the problem, round 2 thoughts
- Include k = 0 in search: if nums are already all zeros, answer is 0.
- For a candidate k, apply queries 0..k-1. Use diff array of length n+1, add val at l, subtract at r+1 (if r+1 < n).
- After prefix-summing the diff into coverage array, check coverage[j] >= nums[j] for all j; if any index fails, k is infeasible.
- Binary search left=0, right=m; while left<right compute mid=(left+right)//2; if feasible(mid) set right=mid else left=mid+1. After loop test left; if feasible return left else -1.
- Time complexity: each feasibility check is O(n + k) but we can bound per check as O(n + m) worst-case. Binary search does O(log m) checks -> total O((n+m) log m). Space O(n) for diff/coverage.
- Constraints (n,m up to 1e5) make this approach fine.
- Edge cases: large n, k=0, queries with r = n-1, val small (<=5) doesn't affect approach.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minK(self, nums: List[int], queries: List[List[int]]) -> int:
        """
        Return the minimum non-negative k such that after processing the first k queries
        (queries[0..k-1]) we can make nums all zeros by choosing per-index decrements
        up to the val of queries covering that index. If impossible, return -1.
        """
        n = len(nums)
        m = len(queries)

        # Helper: check if first k queries suffice (k in [0, m])
        def feasible(k: int) -> bool:
            # difference array
            diff = [0] * (n + 1)
            for i in range(k):
                l, r, v = queries[i]
                diff[l] += v
                if r + 1 < n:
                    diff[r + 1] -= v
            # accumulate and compare
            cur = 0
            for i in range(n):
                cur += diff[i]
                if cur < nums[i]:
                    return False
            return True

        # Binary search for minimal k
        left, right = 0, m
        while left < right:
            mid = (left + right) // 2
            if feasible(mid):
                right = mid
            else:
                left = mid + 1

        if left <= m and feasible(left):
            return left
        return -1
```
- Notes:
  - Approach: binary search on k + difference array to apply range additions (sum of val for queries covering each index). For a candidate k, we check whether coverage[j] >= nums[j] for all j.
  - Time complexity: O((n + m) log m) in the worst case (each feasibility check processes up to k queries and n indices; binary search does O(log m) checks). With m ~ n this is O(n log n).
  - Space complexity: O(n) for the difference array.
  - Implementation details: k=0 is handled (no queries applied); queries indices are assumed 0-based as in the problem. The function returns -1 when even all m queries cannot reduce every element to zero.