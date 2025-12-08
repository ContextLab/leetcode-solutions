# [Problem 1925: Count Square Sum Triples](https://leetcode.com/problems/count-square-sum-triples/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count integer triples (a, b, c) with 1 <= a, b, c <= n and a^2 + b^2 = c^2. The domain n is up to 250, which is small enough to allow an O(n^2) enumeration. One straightforward idea: for each c and each a (or for each pair a, b) check whether c^2 - a^2 is a perfect square (that's b^2). Using integer square root (math.isqrt) avoids floating-point issues. The problem counts ordered pairs, since examples include both (3,4,5) and (4,3,5).

## Refining the problem, round 2 thoughts
- We should ensure we count ordered (a,b) pairs. If we iterate a and b both from 1..n and check if a^2 + b^2 is a perfect square <= n^2, that directly counts ordered pairs.
- Slightly fewer checks if we iterate c from 1..n and a from 1..c-1 (since a,b < c when a^2 + b^2 = c^2 with positive integers), compute b^2 = c^2 - a^2 and check with isqrt. This still counts ordered pairs because when a takes the other value, we'll count the swapped pair too.
- Use math.isqrt to test perfect square safely.
- Complexity: O(n^2) time, O(1) extra space. For n <= 250 this is trivial to run.
- An alternative: generate Pythagorean triples using Euclid's formula and scale them, which can be more efficient for larger n, but unnecessary here.

## Attempted solution(s)
```python
import math
from typing import *

class Solution:
    def countTriples(self, n: int) -> int:
        count = 0
        # Iterate c and a, compute b via integer sqrt
        for c in range(1, n + 1):
            c2 = c * c
            # a and b must be positive and less than c for a^2 + b^2 = c^2
            for a in range(1, c):
                diff = c2 - a * a
                b = math.isqrt(diff)
                if b >= 1 and b < c and b * b == diff:
                    count += 1
        return count
```
- Notes:
  - Approach: iterate c from 1..n, for each a in 1..c-1 compute b = isqrt(c^2 - a^2) and check b^2 equals the difference and b < c. Each valid (a,b,c) found is counted; symmetry ensures (b,a,c) will be counted when a iterates to the other value, so ordered pairs are accounted for.
  - Time complexity: O(n^2) iterations; each iteration does O(1) work (integer arithmetic and isqrt) — overall O(n^2).
  - Space complexity: O(1) extra space.
  - math.isqrt avoids floating-point rounding errors and is efficient.
  - Given constraint n <= 250 this solution is more than fast enough.