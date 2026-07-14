# [Problem 3336: Find the Number of Subsequences With Equal GCD](https://leetcode.com/problems/find-the-number-of-subsequences-with-equal-gcd/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count ordered pairs of non-empty disjoint subsequences (A, B) with equal GCD. Thinking: it's natural to group subsequences by their GCD value g. For fixed g, only elements divisible by g can participate; divide those elements by g and now we need pairs of disjoint non-empty subsequences whose gcd is 1 in the scaled array.

Counting arbitrary subsequences with gcd 1 can be done with multiplicative/inclusion-exclusion using the Möbius function: number of non-empty subsets with gcd = 1 = sum_{t} mu[t] * (2^{cnt_t} - 1) where cnt_t = count of elements divisible by t. But here we need ordered pairs of disjoint subsequences (A,B) with gcd(A)=gcd(B)=1. Think of each element having three choices: be in A, in B, or in neither (can't be both). Inclusion-exclusion / Möbius can be applied in two dimensions: use mu[s]*mu[t] and count assignments where all elements of A are divisible by s and all of B are divisible by t. For such a pair (s,t), the elements fall into three categories: divisible only by s, only by t, or by both (lcm). From those counts we can compute the number of assignments with both A and B non-empty and disjoint. Summing mu[s]*mu[t] times that value over s,t gives the number of ordered pairs with gcd(A)=gcd(B)=1 for that fixed g. Summing over g yields the answer.

## Refining the problem, round 2 thoughts
- Precompute occ[v] = number of nums equal to v (or just counts by value).
- Precompute div_count[x] = number of array elements divisible by x (for x up to max(nums)). This simplifies checking "divisible by d*s" etc.
- Precompute Möbius function mu up to max(nums) via sieve.
- For a fixed g (d in code), we only need to consider scaled divisors s,t up to floor(max/g). For each pair (s,t) with mu[s] and mu[t] non-zero:
  - Let l = lcm(s,t).
  - c = count of elements divisible by g*l (both s and t).
  - a = count divisible by g*s but not g*l.
  - b = count divisible by g*t but not g*l.
  - For those elements, number of disjoint assignments (A,B) with both non-empty:
    total_all = 2^{a} * 2^{b} * 3^{c} = 2^{a+b} * 3^{c}
    subtract assignments where A empty, where B empty, add back both empty:
    result = 2^{a+b} * 3^{c} - 2^{b+c} - 2^{a+c} + 1
  - Multiply this by mu[s]*mu[t] and accumulate.
- Sum over g. Use modulo 1e9+7. Skip g where total elements divisible by g < 2 (can't form two disjoint non-empty subsequences).
- Complexity: max value M <= 200. Sum_{d=1..M} (M/d)^2 ≈ O(M^2). With small constant; definitely feasible. Memory O(M + n).

## Attempted solution(s)
```python
from math import gcd

MOD = 10**9 + 7

class Solution:
    def countPairs(self, nums):
        # This method matches LeetCode function signature (nums -> int)
        n = len(nums)
        maxv = max(nums)
        # occ[value] = frequency of that exact value
        occ = [0] * (maxv + 1)
        for v in nums:
            occ[v] += 1

        # div_count[x] = number of elements divisible by x
        div_count = [0] * (maxv + 1)
        for x in range(1, maxv + 1):
            cnt = 0
            for m in range(x, maxv + 1, x):
                cnt += occ[m]
            div_count[x] = cnt

        # Möbius function mu up to maxv
        mu = [1] * (maxv + 1)
        is_prime = [True] * (maxv + 1)
        primes = []
        mu[0] = 0
        mu[1] = 1
        for i in range(2, maxv + 1):
            if is_prime[i]:
                primes.append(i)
                mu[i] = -1
            for p in primes:
                if i * p > maxv:
                    break
                is_prime[i * p] = False
                if i % p == 0:
                    mu[i * p] = 0
                    break
                else:
                    mu[i * p] = -mu[i]

        # Precompute powers of 2 and 3 up to n (max possible counts)
        pow2 = [1] * (n + 1)
        pow3 = [1] * (n + 1)
        for i in range(1, n + 1):
            pow2[i] = (pow2[i - 1] * 2) % MOD
            pow3[i] = (pow3[i - 1] * 3) % MOD

        ans = 0
        # iterate over possible gcd values g (called d below)
        for d in range(1, maxv + 1):
            total_div = div_count[d]
            if total_div < 2:
                continue  # need at least two distinct indices to form disjoint non-empty subsequences

            limit = maxv // d
            sum_d = 0
            # iterate divisors s, t in scaled domain
            for s in range(1, limit + 1):
                mus = mu[s]
                if mus == 0:
                    continue
                cnt_s = div_count[d * s]  # elements divisible by d*s
                if cnt_s == 0 and mus != 0:
                    # term may still be nonzero because of t loop, but optimization: zero cnt_s simplifies many terms
                    pass
                for t in range(1, limit + 1):
                    mut = mu[t]
                    if mut == 0:
                        continue
                    # l = lcm(s, t)
                    ggt = gcd(s, t)
                    l = s // ggt * t
                    if l > limit:
                        cnt_l = 0
                    else:
                        cnt_l = div_count[d * l]
                    cnt_t = div_count[d * t]
                    c = cnt_l
                    a = cnt_s - c
                    b = cnt_t - c
                    # compute term = 2^{a+b} * 3^{c} - 2^{b+c} - 2^{a+c} + 1
                    # all exponents are between 0 and n
                    term = (pow2[a + b] * pow3[c]) % MOD
                    term = (term - pow2[b + c]) % MOD
                    term = (term - pow2[a + c]) % MOD
                    term = (term + 1) % MOD
                    # multiply by mu[s] * mu[t]
                    coeff = mus * mut
                    if coeff == 1:
                        sum_d = (sum_d + term) % MOD
                    elif coeff == -1:
                        sum_d = (sum_d - term) % MOD
                    # coeff 0 already skipped by mu checks

            ans = (ans + sum_d) % MOD

        return ans if ans >= 0 else ans + MOD

# For LeetCode-style:
# instantiate Solution and call countPairs(nums)
```

- Notes about the solution approach:
  - We iterate over every possible gcd d. For each d we consider only elements divisible by d and scale them down (conceptually).
  - Use Möbius inversion in two dimensions: the indicator gcd(A) = 1 is represented by sum_s mu[s] 1_{A ⊆ D_s}. Combining for A and B gives mu[s]*mu[t] times count of assignments where A⊆D_s, B⊆D_t and they are disjoint and non-empty.
  - For a fixed pair (s,t) we split elements into: divisible only by s (count a), only by t (count b), and by both (count c). Then number of disjoint assignments with both non-empty is 2^{a+b}*3^{c} - 2^{b+c} - 2^{a+c} + 1. The reasoning: each of a items has 2 choices (A or neither), b items have 2 choices (B or neither), c items have 3 choices (A,B,neither). Subtract assignments with A empty, B empty, add back both empty.
  - Summing mu[s]*mu[t] * that count over s,t gives number of ordered pairs for scaled gcd=1. Summing across d gives final answer.

- Complexity:
  - Let M = max(nums) (<= 200). Precomputations (occ, div_count, mu) cost O(M log M) in practice (nested loops but small). The double-sum over (d, s, t) runs in time roughly sum_{d=1..M} (M/d)^2 = O(M^2) (≈ 66k iterations for M=200), each with O(1) arithmetic. So time ~ O(M^2 + n*M) with small constant. Memory O(M + n).
- Correctness:
  - The Möbius-based inclusion-exclusion and the 3-choice counting for disjoint assignment are standard and together correctly account for the gcd=1 requirement and the disjointness and non-empty constraints.
- Modulo: All arithmetic done mod 10^9+7, careful with negative contributions from mu.