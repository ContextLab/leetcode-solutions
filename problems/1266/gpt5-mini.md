# [Problem 1266: Minimum Time Visiting All Points](https://leetcode.com/problems/minimum-time-visiting-all-points/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the minimum time to move through the given points in order. Movement options: in 1 second, move one unit vertically, one unit horizontally, or both (a diagonal move that effectively moves (±1, ±1) in one second). So when going from point A to B, if both x and y must change, a diagonal move can decrease both differences by 1 in a single second. Intuitively, you can keep moving diagonally until one axis difference is exhausted, then move straight for the remainder. That suggests the time between two points is the larger of the absolute differences in x and y (Chebyshev distance), i.e., max(|dx|, |dy|). Sum that for each consecutive pair.

## Refining the problem, round 2 thoughts
Edge cases: if there's only one point, time is 0. The input size is small (n ≤ 100), so an O(n) solution is trivial and optimal. Alternative (but unnecessary) approaches: simulate each second step-by-step, or compute Manhattan distance—those are either slower or incorrect. The correct formula is max(|dx|, |dy|). Time complexity O(n), space O(1).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minTimeToVisitAllPoints(self, points: List[List[int]]) -> int:
        total_time = 0
        for i in range(1, len(points)):
            x1, y1 = points[i-1]
            x2, y2 = points[i]
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            total_time += max(dx, dy)
        return total_time
```
- Notes:
  - Approach: For each consecutive pair of points, the minimum time equals the Chebyshev distance max(|dx|, |dy|) because diagonal moves can reduce both coordinates simultaneously. Sum these times for the full path.
  - Time complexity: O(n), where n = number of points (we process each consecutive pair once).
  - Space complexity: O(1) extra space (only a few variables used).