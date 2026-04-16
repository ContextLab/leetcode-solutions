# [Problem 3488: Closest Equal Element Queries](https://leetcode.com/problems/closest-equal-element-queries/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need, for each query index i, the minimum circular distance from i to any other index j where nums[j] == nums[i]. A circular array means distance between a and b is min(|a-b|, n - |a-b|). If the value at nums[i] occurs only once, answer is -1.

First idea: group indices by value. For a given value v, we have a sorted list of indices where v appears. For a query index i (which must be in that list), the nearest equal index in circular distance will be one of the immediate neighbors of i in that cyclic list (the next or previous occurrence), because any further occurrence on that list is farther either in linear order or across the wrap. So binary search for i's position in positions[v] and check its predecessor and successor (with wrap-around). If the positions list has length 1, return -1.

This gives an O(n) preprocessing to build maps and O(log k) per query for search (k occurrences for that value). Overall O(n + q log n) worst-case.

## Refining the problem, round 2 thoughts
Edge cases:
- Value appears exactly once => answer -1.
- Indices wrap around: for successor if i is last in the list, successor is first element (wrap), and predecessor similarly.
- bisect_left returns the index of i in the list; because the list contains i we can use that position to pick neighbors as pos-1 and pos+1 (mod length).
- Distance calculation: compute diff = abs(i - j) and return min(diff, n - diff).

Space: storing lists of indices per distinct value; worst-case O(n) total.

Time: building mapping O(n); each query O(1) to get list and O(1) to compute neighbor positions (no need to bisect if we can map index->position within its list). If we want to make per-query O(1), we can precompute for every index i its nearest neighbor distance by scanning each positions list and computing distances to adjacent occurrences (including wrap). That would produce answers for all indices in O(n) total and then answer queries in O(1). That is even better: for each list of indices L (len m), for each k in range(m): compare L[k] with L[(k-1)%m] and L[(k+1)%m], compute distances and store min for that index. Complexity O(n). This avoids binary search per query and is simpler.

I'll implement the precompute-per-index approach: for each value group, if size==1 set -1 for that sole index; else for each occurrence compute distances to its two neighbors in the cyclic group and set answer[index] = min(distance to prev, distance to next).

This yields O(n) time and O(n) space overall.

## Attempted solution(s)
```python
from typing import List
import collections

class Solution:
    def closestEqualDistance(self, nums: List[int], queries: List[int]) -> List[int]:
        n = len(nums)
        pos = collections.defaultdict(list)
        for i, v in enumerate(nums):
            pos[v].append(i)
        
        # Initialize all answers for indices to -1
        nearest = [-1] * n
        
        # For each value group, compute nearest equal distance for each occurrence
        for indices in pos.values():
            m = len(indices)
            if m == 1:
                # only one occurrence -> stays -1
                continue
            # For each occurrence, check its cyclic neighbors in the indices list
            for k in range(m):
                i = indices[k]
                prev_i = indices[(k - 1) % m]
                next_i = indices[(k + 1) % m]
                # compute circular distances
                diff_prev = abs(i - prev_i)
                dist_prev = min(diff_prev, n - diff_prev)
                diff_next = abs(i - next_i)
                dist_next = min(diff_next, n - diff_next)
                nearest[i] = min(dist_prev, dist_next)
        
        return [nearest[q] for q in queries]
```
- Notes:
  - Approach: group indices by value, then for each index compute distance to its previous and next occurrence (in cyclic order) and take the minimum. If a value appears only once, its answer remains -1.
  - Time complexity: O(n) to build groups + O(n) to compute neighbor distances across all groups = O(n) overall (n = len(nums)); answering queries is O(q) to gather precomputed values.
  - Space complexity: O(n) for the mapping and for the precomputed nearest array.
  - Implementation details: indices are appended in increasing order while iterating nums, so no extra sorting step is required. Wrap-around neighbors use modulo indexing. Distance is computed as min(|i-j|, n - |i-j|).