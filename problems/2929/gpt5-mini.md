# [Problem 2929: Distribute Candies Among Children II](https://leetcode.com/problems/distribute-candies-among-children-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I see we need the number of nonnegative integer triples (a, b, c) with a + b + c = n and each <= limit. Without the upper bound this is a standard stars-and-bars count: C(n+2, 2). The upper bound suggests inclusion-exclusion: subtract solutions where a variable exceeds limit, add back where two exceed, etc. That should be straightforward because there are only 3 variables, so inclusion-exclusion has just 4 terms. Need to be careful with negative counts when the residual sum becomes negative — treat those as zero. Also watch integer sizes (but Python handles big ints).

## Refining the problem, round 2 thoughts
Refine to formula: let m = limit. For t >= 0 number of nonnegative solutions of x+y+z = t is C(t+2,2) else 0. Use inclusion-exclusion:

ans = C(n+2,2)
    - 3 * C(n-(m+1)+2, 2)
    + 3 * C(n-2*(m+1)+2, 2)
    - C(n-3*(m+1)+2, 2)

Each combinatorial term is zero if its inner sum < 0. Complexity is O(1) time and O(1) space. Edge cases: limit >= n -> no variable exceeds limit so answer is C(n+2,2) which the formula gives because subtracted terms become zero.

## Attempted solution(s)
```python
class Solution:
    def waysToDistribute(self, n: int, limit: int) -> int:
        # f(t) = number of nonnegative integer solutions to x+y+z = t
        # which is C(t+2, 2) for t >= 0, else 0
        def f(t: int) -> int:
            if t < 0:
                return 0
            x = t + 2
            return x * (x - 1) // 2

        m1 = limit + 1
        ans = (
            f(n)
            - 3 * f(n - m1)
            + 3 * f(n - 2 * m1)
            - f(n - 3 * m1)
        )
        return ans
```
- Notes: The solution uses inclusion-exclusion on the constraint "variable > limit". f(t) computes C(t+2,2) safely returning 0 for negative t. Time complexity O(1) and space O(1). All arithmetic is integer; for given constraints results fit in Python integers easily.