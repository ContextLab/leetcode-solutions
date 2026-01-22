# [Problem 2163: Minimum Difference in Sums After Removal of Elements](https://leetcode.com/problems/minimum-difference-in-sums-after-removal-of-elements/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have an array of length 3n and must remove exactly n elements (any subsequence). After removal, the remaining 2n elements are split into first n and second n (in original order), and we want to minimize (sum_first - sum_second).

This is tricky because removing arbitrary elements mixes indices. A known observation: consider the overlap region indices n..2n-1 — elements here can end up in either the first part or the second part. The first part must be formed from elements among indices 0..2n-1 (it picks n elements from that prefix), and the second part must be formed from elements among indices n..3n-1 (it picks n elements from that suffix). So for any split between positions i and i+1 (where i runs between n-1 and 2n-1), the best we can do for the first part using items from 0..i is to take the maximum possible sum of n elements there; and for the second part using items from i+1..3n-1 is to take the minimum possible sum of n elements there. Then the difference for that split is left_max_sum(i) - right_min_sum(i+1). We can iterate i and take the minimum difference.

This suggests computing:
- left[i] = maximum sum of n elements chosen from nums[0..i] for i in [n-1, 2n-1]
- right[i] = minimum sum of n elements chosen from nums[i..3n-1] for i in [n, 2n]

We can compute left with a min-heap of size n (keep n largest prefixes) and right with a max-heap of size n (keep n smallest suffixes). Then sweep to find min(left[i] - right[i+1]).

## Refining the problem, round 2 thoughts
Edge cases: n = 1 small arrays should work. Heaps must be carefully maintained and indices aligned. Time complexity should be O(n log n) and space O(n). We'll store left and right arrays (size 3n or at least for needed ranges).

Implementation details:
- For left: initialize heap with first n elements, sum = sum(first n). left[n-1] = sum. For i from n to 2n-1, push nums[i], pop the smallest, adjust sum, set left[i] = sum.
- For right: initialize heap with last n elements (indices 2n..3n-1), sum = sum(last n). right[2n] = sum. Iterate i from 2n-1 down to n, push nums[i] (as negative for max-heap), pop largest (i.e., pop smallest negative), adjust sum, set right[i] = sum.
- Then answer = min(left[i] - right[i+1]) for i from n-1 to 2n-1.

Complexities: O(n log n) time (heap ops) and O(n) extra space for two arrays and heaps.

## Attempted solution(s)
```python
import heapq
from typing import List

class Solution:
    def minimumDifference(self, nums: List[int]) -> int:
        m = len(nums)
        n = m // 3
        
        # left[i]: max sum of n elements chosen from nums[0..i]
        left = [0] * m
        min_heap = nums[:n]
        heapq.heapify(min_heap)
        s = sum(min_heap)
        left[n-1] = s
        # extend left for i = n .. 2n-1
        for i in range(n, 2*n):
            heapq.heappush(min_heap, nums[i])
            smallest = heapq.heappop(min_heap)
            s += nums[i] - smallest
            left[i] = s
        
        # right[i]: min sum of n elements chosen from nums[i..m-1]
        right = [0] * m
        # max-heap via negatives for maintaining n smallest
        max_heap = [-x for x in nums[2*n:3*n]]
        heapq.heapify(max_heap)
        t = sum(nums[2*n:3*n])
        right[2*n] = t
        for i in range(2*n - 1, n - 1, -1):
            heapq.heappush(max_heap, -nums[i])
            largest = -heapq.heappop(max_heap)
            t += nums[i] - largest
            right[i] = t
        
        # compute minimum difference left[i] - right[i+1] for i in [n-1, 2n-1]
        ans = float('inf')
        for i in range(n-1, 2*n):
            ans = min(ans, left[i] - right[i+1])
        return ans
```
- Approach: Use two sweeps with heaps:
  - Left sweep (left array): keep n largest sums from prefix using a min-heap sized n — ensures left[i] is the maximum possible sum of n elements from nums[0..i].
  - Right sweep (right array): keep n smallest sums from suffix using a max-heap (negatives) sized n — ensures right[i] is the minimum possible sum of n elements from nums[i..end].
  - Combine by checking splits between i and i+1 for i in [n-1, 2n-1] and take min(left[i] - right[i+1]).

- Time complexity: O(n log n) due to heap operations across O(n) pushes/pops.
- Space complexity: O(n) extra (heaps + left/right arrays).