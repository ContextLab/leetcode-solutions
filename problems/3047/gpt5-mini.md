# [Problem 3047: Find the Largest Area of Square Inside Two Rectangles](https://leetcode.com/problems/find-the-largest-area-of-square-inside-two-rectangles/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the largest square that can fit inside the intersecting region of at least two rectangles. If a square fits inside the intersection of three (or more) rectangles, it also fits inside the intersection of some pair among them (because the intersection of a pair is a superset of the intersection of the whole set). So it suffices to check intersections of all pairs.

For a pair of axis-aligned rectangles, the intersection is another axis-aligned rectangle (possibly empty). The maximum square that fits inside that intersection has side = min(width, height) of the intersection. So iterate pairs, compute overlap rectangle, get side, track max side. n ≤ 1000 so O(n^2) pairs (~1e6) is fine.

Watch out for degenerate overlaps (no overlap -> width or height ≤ 0). Coordinates up to 1e7 but differences safe in Python ints.

## Refining the problem, round 2 thoughts
- Confirm that checking all pairs is correct because any intersection of ≥2 rectangles contains the intersection of at least one pair that also contains the same square.
- Edge cases: no intersecting pairs -> return 0. Overlaps that touch on a line or point give width==0 or height==0 -> no positive-area square.
- Time complexity O(n^2), space O(1) (excluding input). For n = 1000 this is fine.
- No complicated geometry needed; simple min/max arithmetic.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def largestSquare(self, bottomLeft: List[List[int]], topRight: List[List[int]]) -> int:
        """
        Compute the largest square area that can fit inside the intersection of at least two rectangles.
        """
        n = len(bottomLeft)
        max_side = 0
        for i in range(n):
            ax1, ay1 = bottomLeft[i]
            ax2, ay2 = topRight[i]
            for j in range(i + 1, n):
                bx1, by1 = bottomLeft[j]
                bx2, by2 = topRight[j]
                # Intersection rectangle coordinates
                ix1 = max(ax1, bx1)
                iy1 = max(ay1, by1)
                ix2 = min(ax2, bx2)
                iy2 = min(ay2, by2)
                # Overlap dimensions
                dx = ix2 - ix1
                dy = iy2 - iy1
                if dx > 0 and dy > 0:
                    side = min(dx, dy)
                    if side > max_side:
                        max_side = side
        return max_side * max_side
```
- Approach: iterate all pairs of rectangles, compute their intersection rectangle via coordinate maxima/minima, derive overlap width and height, square side = min(width, height). Track max side and return area = side^2.
- Time complexity: O(n^2) for checking all pairs (n ≤ 1000 → ~1e6 pairs).
- Space complexity: O(1) extra (ignoring input).
- Implementation details: treat non-overlap or line/point-touch as dx ≤ 0 or dy ≤ 0 (no positive-area square). Coordinates are integers, so side and area are integers.