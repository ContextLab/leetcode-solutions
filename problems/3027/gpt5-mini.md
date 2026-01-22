# [Problem 3027: Find the Number of Ways to Place People II](https://leetcode.com/problems/find-the-number-of-ways-to-place-people-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count ordered pairs (Alice, Bob) placed at given distinct points such that Alice is the upper-left corner and Bob is the lower-right corner of the (possibly degenerate) axis-aligned rectangle and no other point lies on or inside that rectangle.

Upper-left means Alice.x <= Bob.x and Alice.y >= Bob.y. The rectangle spans x in [Alice.x, Bob.x] and y in [Bob.y, Alice.y]. For a chosen pair (A, B) we must ensure there are exactly two points in that rectangle (A and B themselves).

Brute force: check all O(n^2) pairs and for each scan all n other points to see if any lie in the rectangle -> O(n^3), too slow for n up to 1000.

We can try sorting by x and use a data structure to count how many points between two x-positions have y between specific bounds. If we sort points by x, then for a fixed left index L and iterate right index R >= L, we can maintain counts of y-values of points with x indices in [L, R] using a Fenwick tree (BIT) over compressed y-coordinates. For pair (L,R) being valid we need y_L >= y_R and the count of points with y in [y_R, y_L] among x in [L, R] to be exactly 2 (A and B). That becomes: for each L, start with empty BIT, iterate R from L..n-1, add point R to BIT, and when y_L >= y_R query BIT.sum(range y_R..y_L) and check == 2.

One nuance: when multiple points have the same x coordinate, ordering among equal-x points matters so that when x_A == x_B and y_A >= y_B, A appears before B in the sorted order and will be considered as left L and right R. So sorting by x ascending and y descending handles that.

This yields an O(n^2 log n) solution (n up to 1000 is fine).

## Refining the problem, round 2 thoughts
- Coordinate compression of y-values is needed because original y coordinates can be large and sparse. Compression reduces BIT size to n.
- Sorting by x ascending, then by y descending ensures that for points with equal x, potential valid pairs (where y_A >= y_B) will have A earlier than B in the sorted order.
- For each L we rebuild a fresh BIT. For R from L..n-1 we add point R (so the BIT always represents points with x indices in [L, R]). When R == L the BIT count is 1 and won't pass the ==2 check, so we naturally avoid counting a point with itself.
- Complexity: For each L (n choices) we do up to n adds and up to n queries; add and query are O(log n), so O(n^2 log n) time and O(n) extra space for BIT and coordinate maps.
- Edge cases: points with equal x and y? Problem states all points distinct so no exact duplicate. Pairs with x_A <= x_B and y_A >= y_B include degenerate rectangles (lines or points) which are allowed. The inclusive check count==2 correctly forbids other points on the boundary.

## Attempted solution(s)
```python
from typing import List

class Fenwick:
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)
    def add(self, i: int, delta: int):
        # i is 0-based index for convenience; convert to 1-based for BIT
        i += 1
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i
    def sum(self, i: int) -> int:
        # prefix sum [0..i], i is 0-based
        i += 1
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s
    def range_sum(self, l: int, r: int) -> int:
        if r < l:
            return 0
        return self.sum(r) - (self.sum(l - 1) if l > 0 else 0)

class Solution:
    def numberOfWays(self, points: List[List[int]]) -> int:
        n = len(points)
        # compress y coordinates
        ys = sorted({y for _, y in points})
        y_to_idx = {y: i for i, y in enumerate(ys)}

        # sort by x ascending, y descending (so for equal x, higher y comes first)
        pts = sorted(points, key=lambda p: (p[0], -p[1]))

        # map to (x, y_idx, original y) for convenience
        pts_idx = [(p[0], y_to_idx[p[1]], p[1]) for p in pts]

        ans = 0
        # For each left index L, sweep R from L..n-1, maintaining counts of y in a Fenwick
        for L in range(n):
            bit = Fenwick(len(ys))
            xL, yL_idx, yL = pts_idx[L]
            for R in range(L, n):
                # add point R
                xR, yR_idx, yR = pts_idx[R]
                bit.add(yR_idx, 1)
                # require Alice.y >= Bob.y (yL >= yR) and xL <= xR is guaranteed by sort &
                # iteration
                if yL_idx >= yR_idx:
                    cnt = bit.range_sum(yR_idx, yL_idx)
                    if cnt == 2:
                        ans += 1
        return ans
```
- Notes on approach:
  - Sort by x asc, y desc to ensure for equal x values potential Alice (upper) appears before Bob (lower).
  - For fixed left index L we iterate right index R and maintain counts of y in the x-range [L, R] using a Fenwick tree on compressed y coordinates.
  - When y_L >= y_R, query how many points currently lie with y in [y_R, y_L]. If exactly 2, the only points in that rectangle are A and B, so we increment the answer.
- Complexity:
  - Time: O(n^2 log n) because for each L we perform O(n) updates and queries each costing O(log n).
  - Space: O(n) for coordinate compression and the Fenwick tree.

This solution is efficient enough for n up to 1000 and handles degenerate rectangles (lines/points) by using inclusive y-range queries.