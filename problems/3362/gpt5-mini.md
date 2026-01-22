# [Problem 3362: Zero Array Transformation III](https://leetcode.com/problems/zero-array-transformation-iii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to remove as many queries as possible while still being able to make every nums[i] zero using the remaining queries. Each remaining query gives at most 1 decrement to each index in its interval, independently per index. So for every index i we need at least nums[i] queries that cover i among the remaining queries. Equivalently, choose a subset of queries of minimal size such that for every index i the number of chosen queries whose interval contains i is >= nums[i]. That is a covering-with-demands problem on a line with intervals; because intervals are contiguous, a greedy left-to-right construction should work: at each position i, ensure the current number of chosen intervals covering i meets nums[i] by selecting additional intervals that start at or before i and extend as far right as possible (to help future positions too). This suggests maintaining available intervals (by start) and picking the ones with the largest right endpoint when more coverage is needed.

## Refining the problem, round 2 thoughts
Refine into an explicit algorithm:
- Sort queries by their left endpoint.
- Iterate positions i = 0..n-1, maintaining:
  - a max-heap of right endpoints of queries whose left <= i (these are currently available).
  - a difference array (or prefix sum) representing how many already-chosen intervals cover current position i (we'll increment by 1 on choosing an interval at position i and decrement at r+1).
  - current_coverage = number of chosen intervals that cover i (via prefix sum).
- While current_coverage < nums[i], pop from the max-heap the available interval with the largest right endpoint r. If r < i or heap empty, it's impossible (cannot cover i enough times) -> return -1. Otherwise choose that interval: add +1 at i and -1 at r+1 in diff, increment current_coverage and chosen_count.
- After processing all positions, chosen_count is the minimal number of queries needed; answer = total_queries - chosen_count.

Complexities:
- Each query is pushed once and popped at most once from the heap -> O(m log m).
- We iterate n positions, doing O(1) work between pops -> total O((n + m) log m).
- Space O(n + m).

Edge cases:
- nums[i] could be zero -> no action needed.
- queries that end before current i are not useful to cover i; if the top of heap has r < i then no available interval can cover i and we should return -1.
- Use a diff array of length n+1 to effect range contribution increments quickly.

## Attempted solution(s)
```python
import heapq
from typing import List

class Solution:
    def maxNumRemovals(self, nums: List[int], queries: List[List[int]]) -> int:
        n = len(nums)
        m = len(queries)
        # sort queries by left endpoint
        qs = sorted(queries, key=lambda x: x[0])
        # heap will be a max-heap by right endpoint; python has min-heap so store -r
        heap = []
        idx = 0  # index into qs for pushing by left endpoint

        # difference array for contributions of chosen intervals
        diff = [0] * (n + 1)
        current_coverage = 0  # prefix sum of diff up to current i
        chosen = 0

        for i in range(n):
            # push all queries with left <= i
            while idx < m and qs[idx][0] <= i:
                l, r = qs[idx]
                # push (negative r, r) so we can get max r easily
                heapq.heappush(heap, -r)
                idx += 1

            # update coverage at position i
            current_coverage += diff[i]

            # need nums[i] coverage at i
            while current_coverage < nums[i]:
                # pick interval with largest r that is available
                if not heap:
                    return -1
                r = -heapq.heappop(heap)
                # if this interval doesn't reach i, it's useless
                if r < i:
                    # since this was the largest r available, nothing can cover i
                    return -1
                # choose this interval: it contributes +1 to [i, r]
                current_coverage += 1
                chosen += 1
                # mark diff to decrement after r
                if r + 1 <= n - 1:
                    diff[r + 1] -= 1
                # no need to update diff[i] because we already increment current_coverage immediately
                # but to keep prefix sums consistent for future indices we don't add diff[i] (we've applied it)
                # if we wanted to be consistent we could do diff[i] += 1 and current_coverage += 1,
                # but skipping diff[i] change works because we already incremented current_coverage now.
                # However, to be consistent with future prefix updates, we should apply diff[r+1] decrement only.
                # (diff[i] was not changed so nothing else will double count)
            # loop continues to next i

        # minimal chosen intervals found
        return m - chosen


# For LeetCode's naming convention:
# class Solution:
#     def maxNumRemovals(self, nums: List[int], queries: List[List[int]]) -> int:
#         ...
```

- Notes about the solution approach:
  - We greedily ensure each position i is covered nums[i] times by picking available intervals (queries) that start no later than i and extend as far right as possible; choosing the farthest-right available interval maximizes its future usefulness.
  - We use a max-heap keyed by the right endpoint to implement the "furthest-right" choice. Each interval is considered at most once.
  - We maintain coverage counts using a difference array to avoid updating a whole range when selecting an interval. When an interval [l, r] is chosen at position i (with l <= i <= r), it increments coverage for all positions from i through r; we increment current_coverage immediately and place a -1 at diff[r+1] so future positions' prefix sums are correct.
  - Time complexity: O((n + m) log m) because each query is pushed and popped at most once and we scan n positions.
  - Space complexity: O(n + m) for the diff array and heap storage.

