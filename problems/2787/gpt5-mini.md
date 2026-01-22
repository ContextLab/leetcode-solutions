# [Problem 2787: Ways to Express an Integer as Sum of Powers](https://leetcode.com/problems/ways-to-express-an-integer-as-sum-of-powers/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem asks how many ways to write n as a sum of distinct x-th powers of positive integers. This feels like a subset-sum / knapsack counting problem where each candidate is i^x (i >= 1) and each candidate can be used at most once. Because numbers must be unique, this is exactly the 0/1 subset-sum counting variant.

Constraints: n <= 300, x <= 5. For x up to 5, the largest base i we might consider is floor(n^(1/x)), which is small (for n=300 and x=1, up to 300 items; for larger x, far fewer items). So dynamic programming over sums up to n is fine.

A standard DP approach: compute all powers p_i = i^x <= n, then use DP (1D) where dp[s] = number of ways to form sum s using processed powers. To ensure each power is used at most once, iterate sums backwards (s from n down to p) when processing a new power p. Initialize dp[0] = 1. Return dp[n] % MOD.

Recursion with memoization is also possible (choose/not choose each power), but iterative DP is straightforward, efficient, and easy to implement.

## Refining the problem, round 2 thoughts
Edge cases:
- x = 1: candidates 1..n; answer counts partitions into distinct integers.
- n small (e.g., n=1) should work, dp size n+1.
- Must return answer modulo 1e9+7.

Complexity:
- Let m = number of bases with i^x <= n (m = floor(n^(1/x))). Time complexity O(m * n) since for each candidate we loop sums up to n. Space O(n) for 1D DP.
- With given constraints this is trivial (n <= 300).

Implementation details:
- Precompute powers as integers.
- Use modulo at each addition.
- Use backward iteration to enforce uniqueness (0/1 knapsack pattern).

## Attempted solution(s)
```python
class Solution:
    def numberOfWays(self, n: int, x: int) -> int:
        MOD = 10**9 + 7

        # Generate all distinct x-th powers <= n
        powers = []
        base = 1
        while True:
            val = base ** x
            if val > n:
                break
            powers.append(val)
            base += 1

        # dp[s] = number of ways to form sum s using processed powers
        dp = [0] * (n + 1)
        dp[0] = 1

        # For each power, update dp in reverse to ensure each used at most once
        for p in powers:
            for s in range(n, p - 1, -1):
                dp[s] = (dp[s] + dp[s - p]) % MOD

        return dp[n]
```
- Notes:
  - Approach: 0/1 knapsack counting (subset-sum counting) where items are i^x for i >= 1 and i^x <= n. Use 1D DP iterating sums backward to avoid reusing items.
  - Time complexity: O(m * n) where m = floor(n^(1/x)) (worst-case m = n when x = 1), so worst-case O(n^2) but with n <= 300 this is fine.
  - Space complexity: O(n) for the dp array.
  - Use modulo 10^9+7 for all additions to avoid overflow and meet problem requirements.