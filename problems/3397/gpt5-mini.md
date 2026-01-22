# [Problem 3397: Maximum Number of Distinct Elements After Operations](https://leetcode.com/problems/maximum-number-of-distinct-elements-after-operations/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
[I see each element can be shifted by any integer in [-k, k] once. That means each element defines an integer interval [num-k, num+k] of possible final values. To maximize the number of distinct final values, it's natural to try to assign to as many different integers as possible, i.e., pick a distinct integer inside the interval for as many elements as we can.

This becomes an interval-to-point assignment (matching) problem: each element (interval) wants a unique integer point inside it. A greedy common strategy for maximizing number of satisfied intervals is to sort intervals by their right endpoint and always pick the smallest available integer >= interval.left. If that integer is <= interval.right we can assign it; otherwise we cannot satisfy this interval with a new distinct value.

Because intervals' coordinates can be up to 1e9 (and possibly negative when subtracting k), we cannot maintain a giant boolean array. But we only need to assign at most n distinct integers, so we can lazily track assigned integers. To efficiently find the smallest unused integer >= L we can use a map-based disjoint-set (union-find) trick: when we assign integer x we "occupy" it and set its parent to the next candidate (x+1), so future finds skip used integers quickly. This is a standard trick for assigning unique integers greedily.]

## Refining the problem, round 2 thoughts
[Refinements:
- Represent each element as an interval [num-k, num+k]; include duplicates separately (each occurrence is a separate interval).
- Sort intervals by right endpoint (tie-breaker left).
- For each interval, find smallest unused integer >= left; if it's <= right, assign and mark that integer used by unioning it with next integer.
- Use a hashmap-based DSU to keep memory proportional to number of assigned integers (<= n) and avoid iterating over huge ranges.
- If k == 0, the intervals are singletons and the algorithm still works; but we can early-return len(set(nums)).

Complexities:
- Building intervals: O(n).
- Sorting: O(n log n).
- Each find/assign uses amortized near-constant time with path compression; overall O(n α(n)) for DSU operations.
- Memory: O(n) for parent map + O(n) for intervals.]

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxDistinct(self, nums: List[int], k: int) -> int:
        # Special-case: if k == 0 we cannot change values, answer is distinct count
        if k == 0:
            return len(set(nums))
        
        intervals = []
        for v in nums:
            intervals.append((v - k, v + k))
        # sort by right endpoint then left endpoint
        intervals.sort(key=lambda x: (x[1], x[0]))
        
        parent = {}  # map occupied point -> next candidate (used for DSU)
        
        def find(x: int) -> int:
            # iterative find with path compression
            # if x not in parent => x is free; return x
            path = []
            while x in parent:
                path.append(x)
                x = parent[x]
            for node in path:
                parent[node] = x
            return x
        
        assigned = 0
        for L, R in intervals:
            x = find(L)
            if x <= R:
                assigned += 1
                # mark x as used: next free candidate is find(x+1)
                parent[x] = find(x + 1)
        return assigned
```
- Notes about approach:
  - We convert the problem to interval assignment: each element is an interval [num-k, num+k].
  - Sort by right endpoint and greedily assign the smallest available integer >= left for each interval.
  - Use a hashmap-based union-find (parent dict) so that once an integer x is assigned we set parent[x] = find(x+1); subsequent find calls skip used integers efficiently. Only assigned integers are stored in parent, so memory is O(assigned) ≤ O(n).
  - Time complexity: O(n log n) due to sorting, plus near O(n) for DSU operations (amortized O(n α(n))). Overall O(n log n).
  - Space complexity: O(n) for intervals and parent map.