# [Problem 3405: Count the Number of Arrays with K Matching Adjacent Elements](https://leetcode.com/problems/count-the-number-of-arrays-with-k-matching-adjacent-elements/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I want to count arrays of length n with values in [1..m] where exactly k adjacent pairs are equal. Adjacent equal pairs + adjacent unequal pairs partition the n-1 adjacencies. If we let t be the number of adjacencies where arr[i] != arr[i-1], then t = (n-1) - k. So we can think in terms of transitions (changes) instead of equalities.

If there are t transitions, then the array splits into s = t+1 contiguous segments of identical values. For any fixed choice of which of the (n-1) adjacent positions are transitions (choose t positions among n-1), we must assign a color/value to each of the s segments so that adjacent segments have different colors: first segment has m choices, each subsequent segment has (m-1) choices. So for a fixed set of transition positions there are m * (m-1)^t colorings. Multiply by C(n-1, t) choices of transition placements. That gives C(n-1, t) * m * (m-1)^t where t = n-1-k.

Noting C(n-1, t) = C(n-1, k) (symmetry), a final simplified formula is:
answer = C(n-1, k) * m * (m-1)^(n-1-k) (mod 1e9+7).

This yields an O(n) preprocessing solution (factorials + inverse factorials) with O(1) final computation.

## Refining the problem, round 2 thoughts
Edge cases:
- If k > n-1, impossible -> return 0.
- If m == 1, then all elements must equal; only possible when k == n-1 (all adjacent equal). The formula handles this: (m-1)^(...) becomes 0^something; careful but formula with m=1 and n-1-k > 0 gives 0 which is correct; when n-1-k == 0 (i.e., k = n-1), (m-1)^0 = 1 and C(n-1,k)=1 so answer = 1*m = 1 as expected.
Implementation details:
- Precompute factorials up to n-1 (or n) and modular inverses using Fermat's little theorem (mod is prime 1e9+7).
- Use pow for modular exponentiation.
Time/space:
- Precompute factorials and inverse factorials in O(n) time and O(n) space.
- Final calculation is O(1).
- Overall O(n) time, O(n) space. n <= 1e5 fits easily.

## Attempted solution(s)
```python
class Solution:
    def numOfArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7
        # If k impossible
        if k > n - 1:
            return 0

        # We need C(n-1, k) * m * (m-1)^(n-1-k) % MOD
        # Precompute factorials up to n-1
        maxN = n  # compute up to n to be safe
        fac = [1] * (maxN + 1)
        for i in range(1, maxN + 1):
            fac[i] = fac[i-1] * i % MOD

        inv_fac = [1] * (maxN + 1)
        inv_fac[maxN] = pow(fac[maxN], MOD - 2, MOD)
        for i in range(maxN, 0, -1):
            inv_fac[i-1] = inv_fac[i] * i % MOD

        def comb(a: int, b: int) -> int:
            if b < 0 or b > a:
                return 0
            return fac[a] * inv_fac[b] % MOD * inv_fac[a-b] % MOD

        ways_choose = comb(n-1, k)
        pow_term = pow(m-1, (n-1)-k, MOD)
        ans = ways_choose * (m % MOD) % MOD * pow_term % MOD
        return ans
```
- Approach: count choices of transition positions (C(n-1, t) with t = n-1-k) and multiply by color assignments per segment m*(m-1)^t. Use modular combinations via factorials and inverse factorials.
- Time complexity: O(n) to precompute factorials and inverse factorials, O(1) to compute the result.
- Space complexity: O(n) for factorial arrays.
- Handles edge cases like k > n-1 and m = 1 correctly.