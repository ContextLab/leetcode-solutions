# [Problem 3130: Find All Possible Stable Binary Arrays II](https://leetcode.com/problems/find-all-possible-stable-binary-arrays-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The condition "each subarray with size > limit must contain both 0 and 1" is equivalent to forbidding any run of identical elements of length >= limit+1. So both 0 and 1 may have at most `limit` consecutive occurrences.

Thus a valid binary array is an alternating sequence of blocks (runs) of 0s and 1s, where:
- the number of 0s total equals `zero`,
- the number of 1s total equals `one`,
- each block size is at least 1 and at most `limit`,
- blocks alternate colors.

So the counting problem reduces to:
- choose how many blocks (positive segments) of 0, call k0, and how many blocks of 1, call k1,
- ensure |k0 - k1| <= 1 (so alternation is possible),
- count the number of ways to partition `zero` into k0 positive parts each <= limit,
- count the number of ways to partition `one` into k1 positive parts each <= limit,
- multiply those and multiply by the number of possible starting colors (1 if counts differ, 2 if equal).

Counting partitions with upper bounds is a standard stars-and-bars + inclusion-exclusion task. We can precompute binomial coefficients modulo 1e9+7 and sum inclusion-exclusion terms.

Max input sizes up to 1000 imply precomputing factorials up to ~2000 and an algorithm roughly O(n^2) is fine.

## Refining the problem, round 2 thoughts
- For splitting n into k positive parts each <= limit, convert xi >= 1 to yi = xi-1 >= 0 with sum N = n-k and yi <= limit-1 = U. Number of nonnegative solutions with yi <= U is:
  sum_{j=0..floor((n-k)/limit)} (-1)^j * C(k, j) * C(n - j*limit - 1, k - 1)
  (treat binomials with invalid parameters as 0).
- We iterate k0 from 1..zero, k1 from 1..one, but only pairs with |k0-k1|<=1. For each pair add comp(zero,k0)*comp(one,k1) * interleavings (1 or 2).
- Precompute factorials and inverse factorials for fast binomial computation modulo MOD.
- Time complexity: for each k (up to 1000) compute comp using a j-loop up to floor((n-k)/limit) which in worst-case (limit=1) is O(n). So worst-case ~O(n^2) ~ 1e6 operations, fine.
- Edge cases: zero, one >=1 by constraints; ensure binomial helper returns 0 for invalid inputs.

## Attempted solution(s)
```python
MOD = 10**9 + 7

class Solution:
    def countBinaryArrays(self, zero: int, one: int, limit: int) -> int:
        # Precompute factorials up to max_n
        maxN = zero + one + 5
        fac = [1] * (maxN)
        ifac = [1] * (maxN)
        for i in range(1, maxN):
            fac[i] = fac[i-1] * i % MOD
        # Fermat inverse for factorials
        ifac[-1] = pow(fac[-1], MOD-2, MOD)
        for i in range(maxN-2, -1, -1):
            ifac[i] = ifac[i+1] * (i+1) % MOD

        def nCr(n, r):
            if r < 0 or n < 0 or r > n:
                return 0
            return fac[n] * ifac[r] % MOD * ifac[n-r] % MOD

        # Count ways to split n into k positive integers each <= limit
        def ways_split_bounded(n, k):
            if k <= 0 or k > n:
                return 0
            # inclusion-exclusion: sum_{j=0..floor((n-k)/limit)} (-1)^j * C(k, j) * C(n - j*limit - 1, k-1)
            res = 0
            # j max such that n - j*limit >= k  => j <= (n - k)//limit
            jmax = (n - k) // limit
            for j in range(jmax + 1):
                sign = -1 if (j & 1) else 1
                term = nCr(k, j) * nCr(n - j*limit - 1, k - 1) % MOD
                if sign == 1:
                    res = (res + term) % MOD
                else:
                    res = (res - term) % MOD
            return res

        ans = 0
        # iterate possible numbers of zero-blocks k0 and one-blocks k1 with |k0-k1| <= 1
        # For efficiency, iterate k0 in 1..zero and compute corresponding k1 values
        # For each valid pair add contribution with 2 interleavings if k0 == k1 else 1
        for k0 in range(1, zero + 1):
            w0 = ways_split_bounded(zero, k0)
            if w0 == 0:
                continue
            # possible k1 values: k0-1, k0, k0+1 but must be in [1, one]
            for k1 in (k0-1, k0, k0+1):
                if k1 < 1 or k1 > one:
                    continue
                if abs(k0 - k1) > 1:
                    continue
                w1 = ways_split_bounded(one, k1)
                if w1 == 0:
                    continue
                inter = 2 if k0 == k1 else 1
                ans = (ans + w0 * w1 % MOD * inter) % MOD

        return ans % MOD
```
- Notes about approach:
  - We reduced the stability constraint to forbidding runs longer than `limit` for both values.
  - The counting decomposes into choosing numbers of blocks for 0s and 1s (k0, k1) that can be alternated and counting bounded compositions for each value separately, multiplying and accounting for starting color choices.
  - Use inclusion-exclusion on stars-and-bars to count compositions with an upper bound per part.

- Complexity:
  - Precomputation of factorials: O(zero + one).
  - For each k (up to zero) we compute bounded-composition sums that run up to O((n-k)/limit) terms; worst-case when limit=1 this is O(n). Overall worst-case O(n^2) with n ~ 1000 -> ~1e6 iterations of small constant work, which is efficient.
  - Space: O(zero + one) for factorial arrays.