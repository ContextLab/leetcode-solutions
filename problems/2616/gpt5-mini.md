# [Problem 2616: Minimize the Maximum Difference of Pairs](https://leetcode.com/problems/minimize-the-maximum-difference-of-pairs/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I see we want p disjoint pairs so that the maximum difference among chosen pairs is minimized. This suggests we care about thresholds on allowed difference: for a given threshold x, can we form p pairs all with difference <= x? That is a yes/no predicate which is monotonic in x, so binary search on the answer comes to mind.

How to decide feasibility for a given x? If we sort nums, then small differences are between nearby elements. Greedily pairing adjacent elements whose difference <= x seems a good approach: scan left to right, whenever the pair of adjacent elements satisfies the bound, take it and skip both; otherwise skip the first and try pairing the next. This maximizes the number of pairs with difference <= x. If we can form >= p pairs this way, x is feasible.

Edge cases: p = 0 (answer 0), small arrays. Sorting is required. Complexity should be O(n log R) where R is value range (max-min).

## Refining the problem, round 2 thoughts
Refine binary search bounds: left = 0, right = max(nums) - min(nums). Use inclusive binary search to find minimal feasible x.

Prove greedy: after sorting, pairing non-adjacent elements can't increase number of pairs with differences <= x because exchanging pairs to adjacent ones cannot make differences worse — standard exchange argument. So the greedy adjacent pairing maximizes count.

Time complexity dominated by sorting O(n log n) plus binary search O(log R) iterations each O(n) scanning, so overall O(n log n + n log R) ~ O(n (log n + log R)). Space O(1) extra (besides sorted array).

Corner cases: if p == 0 return 0. If nums length is small but valid constraints handle that. Use while loop to count pairs.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minimizeMax(self, nums: List[int], p: int) -> int:
        if p == 0:
            return 0
        
        nums.sort()
        n = len(nums)
        
        def can_make_pairs(max_diff: int) -> bool:
            # Greedily form pairs by scanning sorted nums and pairing adjacent
            cnt = 0
            i = 0
            while i + 1 < n and cnt < p:
                if nums[i+1] - nums[i] <= max_diff:
                    cnt += 1
                    i += 2  # use both elements
                else:
                    i += 1  # try next element as potential left of a pair
            return cnt >= p
        
        left, right = 0, nums[-1] - nums[0]
        while left < right:
            mid = (left + right) // 2
            if can_make_pairs(mid):
                right = mid
            else:
                left = mid + 1
        return left
```
- Notes:
  - Approach: sort the array, binary search the minimal maximum allowed difference, and greedily check feasibility by pairing adjacent elements when their difference <= candidate.
  - Time complexity: O(n log n + n log R) where R = max(nums) - min(nums). Sorting O(n log n) plus binary search over range R with O(n) check each iteration.
  - Space complexity: O(1) extra (in-place sort aside).
  - Important detail: Greedy pairing adjacent elements after sorting is optimal to maximize number of valid pairs for a given threshold — this yields a correct feasibility check for binary search.