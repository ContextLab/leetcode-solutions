# [Problem 3025: Find the Number of Ways to Place People I](https://leetcode.com/problems/find-the-number-of-ways-to-place-people-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count ordered pairs (A, B) such that A is on the "upper left" side of B and there are no other points inside or on the border of the axis-aligned rectangle spanned by A and B. My first thought is to translate "upper left" precisely into coordinate comparisons. Looking at examples suggests "upper left" means A.x <= B.x and A.y >= B.y (inclusive allowed on one coordinate so a horizontal/vertical line is allowed). For each candidate pair (A,B) satisfying that relation, check all other points to see if any lie inside or on the boundary of the rectangle [A.x..B.x] x [B.y..A.y]. If any do, the pair is invalid. With n up to 50, an O(n^3) approach (check all pairs and all other points) is perfectly fine.

## Refining the problem, round 2 thoughts
We must be careful about inclusive bounds: the rectangle includes borders, so any third point with coordinates x between A.x and B.x inclusive and y between B.y and A.y inclusive invalidates the pair. We should allow equal x or y for A and B (line cases) as valid pairs as long as no other point lies on that line segment (i.e., on the rectangle border). Distinct points guarantee A != B. Complexity: there are O(n^2) candidate ordered pairs, each validated by checking up to O(n) points => O(n^3) time. Space is O(1) besides input. Edge cases: all points collinear or many points preventing most pairs; the algorithm handles them.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def numberOfWays(self, points: List[List[int]]) -> int:
        n = len(points)
        ans = 0
        for i in range(n):
            xi, yi = points[i]
            for j in range(n):
                if i == j:
                    continue
                xj, yj = points[j]
                # Check "upper left": xi <= xj and yi >= yj (inclusive allowed)
                if xi <= xj and yi >= yj:
                    empty = True
                    # Check for any other point inside or on border of rectangle
                    xlo, xhi = xi, xj
                    ylo, yhi = yj, yi
                    for k in range(n):
                        if k == i or k == j:
                            continue
                        xk, yk = points[k]
                        if xlo <= xk <= xhi and ylo <= yk <= yhi:
                            empty = False
                            break
                    if empty:
                        ans += 1
        return ans
```
- Approach: brute-force all ordered pairs (A,B) that satisfy the "upper left" relation (xi <= xj and yi >= yj). For each such pair, verify there is no third point in the inclusive axis-aligned rectangle between them. If none, increment the count.
- Time complexity: O(n^3) where n = number of points (n ≤ 50 so this is fine). For each of O(n^2) pairs we scan up to O(n) other points.
- Space complexity: O(1) extra space (ignoring input and output).