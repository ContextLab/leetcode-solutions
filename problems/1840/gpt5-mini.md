# [Problem 1840: Maximum Building Height](https://leetcode.com/problems/maximum-building-height/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We must place n buildings in a line with non-negative integer heights, h1 = 0, adjacent difference ≤ 1, and some buildings have upper bounds. We want the maximum possible height among all buildings.

First thought: treat the given restrictions as fixed caps. Because adjacent difference ≤ 1, heights between two restricted positions (i, hi) and (j, hj) are tightly constrained: when you move from i to j you can only change height by at most distance d = j-i. So each restriction also limits neighbors (propagating). A standard approach is to add the implicit restriction (1,0). Also it's helpful to consider the last position n — its unconstrained cap is n-1 (starting from 0 with +1 each step). If n isn't in restrictions we can add (n, n-1) so the chain is closed. Then propagate caps left-to-right and right-to-left to enforce that no restriction can be violated through adjacency. After that, between any two consecutive restricted positions we know their capped heights and can compute the maximal achievable peak between them analytically: the peak is where increasing from left and decreasing to right meet, formula involving (h1 + h2 + d)//2.

## Refining the problem, round 2 thoughts
Refinements / edge cases:
- Problem guarantees building 1 is not in restrictions so we must add (1,0).
- If restrictions already include n, do not override it; otherwise add (n, n-1).
- After sorting restrictions by id and doing two passes (left→right and right→left) adjusting heights via h[i] = min(h[i], h[i-1] + dist) and similarly backwards, the set of caps becomes consistent with adjacency constraints.
- The maximum between two restricted points (id1, h1) and (id2, h2) with distance d = id2 - id1 is floor((h1 + h2 + d)/2). This can be derived by letting heights increase by 1 from left and decrease by 1 from right until they meet.
- Complexity: sorting O(m log m) where m = len(restrictions) + 2, passes and scan linear in m. Space O(m).

Now implement cleanly in Python as LeetCode expects: class Solution with method maxBuilding(self, n, restrictions).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxBuilding(self, n: int, restrictions: List[List[int]]) -> int:
        # Build list of (id, maxHeight) including (1,0)
        pts = [(1, 0)]
        # Add given restrictions
        for rid, rh in restrictions:
            pts.append((rid, rh))
        # If n not present, add (n, n-1) as natural upper bound
        ids = {rid for rid, _ in pts}
        if n not in ids:
            pts.append((n, n - 1))
        # Sort by id
        pts.sort(key=lambda x: x[0])
        # Convert to mutable list of [id, h]
        pts = [[rid, rh] for rid, rh in pts]
        m = len(pts)
        # Left-to-right pass: enforce h[i] <= h[i-1] + dist
        for i in range(1, m):
            dist = pts[i][0] - pts[i-1][0]
            pts[i][1] = min(pts[i][1], pts[i-1][1] + dist)
        # Right-to-left pass: enforce h[i-1] <= h[i] + dist
        for i in range(m-2, -1, -1):
            dist = pts[i+1][0] - pts[i][0]
            pts[i][1] = min(pts[i][1], pts[i+1][1] + dist)
        # Compute maximum achievable height between consecutive restricted points
        ans = 0
        for i in range(1, m):
            id1, h1 = pts[i-1]
            id2, h2 = pts[i]
            d = id2 - id1
            # Maximum peak between them
            peak = (h1 + h2 + d) // 2
            if peak > ans:
                ans = peak
        return ans
```
- Notes:
  - We add (1,0) and ensure (n, n-1) is present so endpoints are covered. Sorting and two passes propagate adjacency constraints.
  - The maximum inside a segment [id1, id2] is floor((h1 + h2 + d)/2).
  - Time complexity: O(m log m) due to sorting, where m = len(restrictions) + up to 2; space complexity: O(m).