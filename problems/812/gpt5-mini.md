# [Problem 812: Largest Triangle Area](https://leetcode.com/problems/largest-triangle-area/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the largest area from any triple of given points. The straightforward way is to check every triple of points, compute the triangle area, and keep the maximum. With up to 50 points, brute force C(50,3) ~ 19.6k triangles is trivial. For area calculation, use the cross product / shoelace formula to avoid any reliance on floating-point trigonometry: area = 0.5 * abs(cross((p2-p1),(p3-p1))). No degenerate or duplicate points per constraints, but some triples may be collinear yielding area 0. Could consider convex hull + rotating calipers for larger inputs, but unnecessary here.

## Refining the problem, round 2 thoughts
- Use integer arithmetic for the doubled area (abs of cross product) to avoid intermediate floating issues, then divide by 2 at the end.
- Edge cases: collinear triples (area 0); minimal n=3 (just one triangle).
- Complexity: brute force O(n^3) time, O(1) extra space. This is fine for n ≤ 50.
- Alternative: compute convex hull and only check hull points which can reduce complexity, but added implementation complexity is not needed for these constraints.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def largestTriangleArea(self, points: List[List[int]]) -> float:
        n = len(points)
        max_doubled_area = 0  # store 2 * area as integer via cross product
        for i in range(n):
            x1, y1 = points[i]
            for j in range(i + 1, n):
                x2, y2 = points[j]
                for k in range(j + 1, n):
                    x3, y3 = points[k]
                    # cross product of (p2 - p1) and (p3 - p1)
                    cross = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)
                    area2 = abs(cross)
                    if area2 > max_doubled_area:
                        max_doubled_area = area2
        return max_doubled_area / 2.0
```
- Notes:
  - Approach: brute-force all triples and compute area using cross product formula: area = 0.5 * |(x2-x1)*(y3-y1) - (x3-x1)*(y2-y1)|.
  - Time complexity: O(n^3) where n = len(points). With n ≤ 50, this is ≈ 19.6k triangle checks worst-case — efficient enough.
  - Space complexity: O(1) extra space (ignoring input storage).
  - Uses integer arithmetic for the doubled area to keep precision robust, then divides by 2.0 for the final float result.