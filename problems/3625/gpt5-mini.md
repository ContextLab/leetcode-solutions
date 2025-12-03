# [Problem 3625: Count Number of Trapezoids II](https://leetcode.com/problems/count-number-of-trapezoids-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count convex quadrilaterals with at least one pair of parallel sides among given points. A trapezoid requires two opposite sides to be parallel. If I fix an orientation (slope), then consider all lines with that slope that contain points: choosing two distinct lines and picking two points from each line (two on line A and two on line B) gives a quadrilateral whose the two chosen sides (joining points on the same line) are parallel. So for each slope, if for each parallel line i there are k_i points, the number of ways to pick two points on two different parallel lines is sum_{i<j} C(k_i,2) * C(k_j,2). Summing over slopes counts all quadrilaterals that have a pair of parallel sides in that orientation.

But parallelograms have two pairs of parallel sides, so they will be counted twice (once for each orientation). So subtract parallelograms once. Parallelograms can be counted by the standard midpoint trick: diagonals of a parallelogram share the same midpoint — count unordered pairs of point-pairs (i,j) that share the same midpoint: for each midpoint, C(cnt,2) parallelograms.

Implementation detail: we don't need k_i explicitly. If we iterate over all unordered pairs of points (i,j) and group them by the normalized slope and the line offset (perpendicular dot), then for a fixed (slope, offset) the number of such pairs equals C(k_i,2). So we can accumulate counts per (slope, offset) directly. Complexity is O(n^2) pairs which is OK for n <= 500.

## Refining the problem, round 2 thoughts
- Represent slope as a normalized direction vector (dx/g, dy/g) with a consistent sign convention (dx>0 or dx==0 and dy>0) to group parallel directions.
- For a given normalized direction vector v = (dxn, dyn), a consistent perpendicular vector is p = (-dyn, dxn). For a point (x,y) the value offset = p.x * x + p.y * y uniquely identifies which parallel line (with that direction) the point lies on. When building pairs (i,j) we can use offset computed from one endpoint; offset is the same for both endpoints on that line.
- When iterating pairs, increment slope_map[slope][offset] by 1 (this count equals C(k_i,2) for that line).
- For each slope, compute S = sum c_i and sum_sq = sum c_i^2 and number of trapezoids for that slope is (S^2 - sum_sq)//2 (which equals sum_{i<j} c_i * c_j).
- Compute parallelograms by mapping midpoints (xi+xj, yi+yj) (doubled coordinates to stay integers) to counts and summing C(cnt,2).
- Final answer = total_trapezoids_by_slope_sum - parallelograms.

Edge cases:
- Vertical/horizontal/slopes of any sign handled by normalization.
- All points distinct is guaranteed.
- All computations are integer; use gcd for normalization.

Time complexity: O(n^2) to enumerate pairs and build maps, and O(#distinct_slope * #lines_per_slope) roughly bounded by O(n^2) still. Space complexity: O(n^2) in worst-case for maps.

## Attempted solution(s)
```python
from collections import defaultdict
from math import gcd
from typing import List

class Solution:
    def countTrapezoids(self, points: List[List[int]]) -> int:
        n = len(points)
        slope_map = defaultdict(lambda: defaultdict(int))  # slope -> (offset -> count_of_pairs_on_that_line)
        mid_map = defaultdict(int)  # midpoint (2x,2y) -> count_of_pairs_that_have_this_midpoint

        for i in range(n):
            xi, yi = points[i]
            for j in range(i+1, n):
                xj, yj = points[j]
                dx = xj - xi
                dy = yj - yi
                g = gcd(dx, dy)
                dxn = dx // g
                dyn = dy // g
                # normalize sign so direction is unique
                if dxn < 0 or (dxn == 0 and dyn < 0):
                    dxn = -dxn
                    dyn = -dyn
                slope = (dxn, dyn)
                # perpendicular vector to the direction (dxn, dyn)
                perp_x, perp_y = -dyn, dxn
                offset = perp_x * xi + perp_y * yi  # integer identifier for the parallel line
                slope_map[slope][offset] += 1

                # midpoint key (double coordinates to stay integral)
                mid_key = (xi + xj, yi + yj)
                mid_map[mid_key] += 1

        total_by_slope = 0
        for slope, offmap in slope_map.items():
            # offmap[offset] is the number of unordered pairs of points on that particular line,
            # which equals C(k,2) where k is number of points on the line.
            vals = list(offmap.values())
            S = sum(vals)
            sum_sq = sum(v * v for v in vals)
            total_by_slope += (S * S - sum_sq) // 2  # sum_{i<j} c_i * c_j

        # parallelograms counted by midpoint collisions: for each midpoint value with cnt pairs,
        # number of parallelograms is C(cnt,2)
        parallelograms = sum(cnt * (cnt - 1) // 2 for cnt in mid_map.values())

        return total_by_slope - parallelograms
```
- Notes:
  - We iterate over all unordered pairs of points (i<j). For each pair we:
    - add 1 to the count of pairs on the particular line identified by (slope, offset). That count equals C(k,2) for that line (k = #points on the line).
    - record the midpoint (xi + xj, yi + yj) to count diagonal-pair collisions (parallelograms).
  - For each slope, if the lines with that slope have pair-counts c_i = C(k_i,2), the number of trapezoids whose parallel sides have that slope is sum_{i<j} c_i * c_j = (S^2 - sum c_i^2) // 2.
  - Parallelograms are counted twice across slopes (once per pair of parallel sides), so subtract the parallelogram count once.
  - Time complexity: O(n^2) to process all pairs; space complexity O(n^2) worst-case for maps. This fits constraints (n <= 500).