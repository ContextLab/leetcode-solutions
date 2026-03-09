# [Problem 3129: Find All Possible Stable Binary Arrays I](https://leetcode.com/problems/find-all-possible-stable-binary-arrays-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The condition that every subarray of size > limit must contain both 0 and 1 means that no run (consecutive identical elements) may have length > limit. So we just need to count binary strings of length n = zero + one with exactly `zero` zeros and `one` ones, and with every run length between 1 and `limit` inclusive.

We can think of the string as alternating blocks of zeros and ones. Let a = number of zero-blocks, b = number of one-blocks. Each block length is at least 1 and at most `limit`. The zeros must sum to `zero`, the ones to `one`. So the number of ways is the number of compositions of `zero` into `a` parts each in [1, limit], times the number of compositions of `one` into `b` parts in [1, limit]. Which (a,b) pairs are possible? For alternating blocks, |a-b| <= 1. Also if a == b there are two possible starting bits (start with 0 or start with 1), otherwise the larger count's bit must be the starting bit. So we can iterate all a,b with 1 <= a <= zero, 1 <= b <= one, |a-b| <= 1, compute the two composition counts and add up (times 2 if a==b else times 1).

Counting compositions with upper bound (each part between 1 and limit) can be done with stars-and-bars + inclusion-exclusion:
number of positive integer solutions x1+...+k = N with 1 <= xi <= L equals
sum_{j=0}^{k} (-1)^j * C(k, j) * C(N - j*L - 1, k-1)
where C(n,k)=0 if n<k or n<0.

We can precompute factorials/inv factorials for combinations modulo 1e9+7. Memoize composition counts for (N,k) to avoid recomputation.

Constraints are small (<=200), so this approach is efficient.

## Refining the problem, round 2 thoughts
- Edge cases: k > N (cannot split N into more than N positive parts) -> zero ways. Also k==0 only if N==0, but inputs guarantee zero,one >=1 so k>=1 here.
- Inclusion-exclusion needs careful bounds; we can cap j by floor((N-k)/L) or simply check the comb arguments.
- Complexity: iterating a in [1..zero] and b in [1..one] but only pairs with |a-b|<=1 -> about O(min(zero,one)*2) pairs, each requiring two composition counts (but we'll memoize so each (N,k) computed once). Composition computation itself loops j up to ~ (N-k)/L which is <= N. So overall complexity roughly O((zero+one) * N) with small constants; safe for ≤200.
- Implementation details: precompute factorials up to zero+one (<=400) for combinations, modular inverse via pow.

## Attempted solution(s)
```python
MOD = 10**9 + 7

class Solution:
    def countStableArrays(self, zero: int, one: int, limit: int) -> int:
        # Precompute factorials up to maxN
        maxN = zero + one + 5
        fact = [1] * (maxN)
        invfact = [1] * (maxN)
        for i in range(1, maxN):
            fact[i] = fact[i-1] * i % MOD
        invfact[-1] = pow(fact[-1], MOD-2, MOD)
        for i in range(maxN-2, -1, -1):
            invfact[i] = invfact[i+1] * (i+1) % MOD

        def comb(n, k):
            if n < 0 or k < 0 or k > n:
                return 0
            return fact[n] * invfact[k] % MOD * invfact[n-k] % MOD

        # number of ways to write N as sum of k positive integers each <= L
        from functools import lru_cache
        @lru_cache(None)
        def compositions_bounded(N, k, L):
            if k == 0:
                return 1 if N == 0 else 0
            if k > N:
                return 0
            # transform to nonnegative: yi = xi - 1, sum yi = N - k, each yi <= L-1
            S = N - k
            U = L - 1
            # inclusion-exclusion:
            res = 0
            # j up to min(k, floor(S/(U+1))) where U+1 = L
            maxj = S // L
            for j in range(0, min(k, maxj) + 1):
                sign = -1 if (j % 2 == 1) else 1
                term = comb(k, j) * comb(N - j*L - 1, k-1) % MOD
                if sign == 1:
                    res = (res + term) % MOD
                else:
                    res = (res - term) % MOD
            return res % MOD

        ans = 0
        # iterate number of zero-blocks a and one-blocks b
        for a in range(1, zero+1):
            for b in (a-1, a, a+1):
                if b < 1 or b > one:
                    continue
                if abs(a-b) > 1:
                    continue
                ways0 = compositions_bounded(zero, a, limit)
                if ways0 == 0:
                    continue
                ways1 = compositions_bounded(one, b, limit)
                if ways1 == 0:
                    continue
                multiplicity = 2 if a == b else 1
                ans = (ans + ways0 * ways1 % MOD * multiplicity) % MOD

        return ans

# For LeetCode function name compatibility:
def countStableArrays(zero: int, one: int, limit: int) -> int:
    return Solution().countStableArrays(zero, one, limit)
```

- Notes about the approach:
  - We model the array as alternating blocks of zeros and ones. Let a be the count of zero-blocks and b the count of one-blocks. Each block length is in [1, limit]. The counts of blocks satisfy |a-b| <= 1. When a == b we have two possible starting bits; otherwise exactly one starting bit is possible.
  - For each (a,b) pair we multiply the number of bounded compositions of `zero` into `a` parts and `one` into `b` parts, and add to the result (times 2 if a == b).
  - The bounded composition count uses inclusion-exclusion on transformed nonnegative solutions.
- Complexity:
  - Time: roughly O((zero+one) * N_max) where N_max <= 400 in practice; more concretely, nested loops over a (<=zero) and b (near a), and for each distinct (N,k) we do inclusion-exclusion up to O(N/L) terms. This is easily within limits for zero,one <= 200.
  - Space: O(N_max) for factorials and O(number of cached (N,k)) for memoization (<= O(zero+one)^2 worst case but practically small).