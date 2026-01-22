# [Problem 3539: Find Sum of Array Product of Magical Sequences](https://leetcode.com/problems/find-sum-of-array-product-of-magical-sequences/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the sum of products over all ordered sequences seq of length m where seq[i] in [0..n-1] (n = len(nums)) and the binary representation of sum_j 2^{seq[j]} has exactly k set bits. A sequence is equivalent to a count vector c_j = how many times index j appears; the sequence product equals prod_j nums[j]^{c_j}, and the number of ordered sequences with these counts is the multinomial m! / prod_j c_j!. So each count vector c contributes:
  m! * prod_j (nums[j]^{c_j} / c_j!).

Condition on the binary representation is on the integer total_sum = sum_j c_j * 2^j. The number of set bits of that integer depends on the bits formed by adding c_j copies of 2^j — carries matter. That suggests a DP iterating bit positions j (i.e., indices of nums) while tracking carries and the number of 1 bits seen so far. Also we must ensure sum c_j = m. We can accumulate prod(nums[j]^{c_j} / c_j!) multiplicatively and multiply by m! at the end.

Constraints: m ≤ 30, n ≤ 50. c_j ∈ [0..m]. Carry after each bit is bounded by m. A DP with dimensions (position up to n) × (used up to m) × (carry up to m) × (ones up to k) is feasible.

## Refining the problem, round 2 thoughts
Set up dp[pos][used][carry][ones] = sum of products (without the global m! factor) for choices over positions < pos. Transition at pos j: choose c in [0..m-used], multiply current value by nums[j]^c / c!, compute new carry = (carry + c) >> 1 and whether current bit contributes (carry + c) & 1 to ones. Cap ones to k (we only care up to k). After finishing all positions, leftover carry may contain multiple set bits; the final valid states are those with used == m and ones + popcount(carry) == k. Sum their values and multiply by m! modulo MOD.

Implementation details:
- Precompute factorials and inverse factorials up to m to get 1/c_j! mod MOD and final multiply by fact[m].
- Precompute pow_nums[j][c] = nums[j]^c % MOD for c=0..m.
- dp arrays can be 3D per position: dp[used][carry][ones]; roll to next position to save memory.
- Time complexity: roughly O(n * (m+1)^2 * (k+1) * avg_c) ~ O(n * m^3) worst-case; with m ≤ 30 and n ≤ 50 this is fine.
- Space complexity: O(m^2 * k).

Edge cases: k may be up to m, handle that; n may be > m so most c_j will be zero for high positions (DP handles that); watch modulo operations.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def findSum(self, m: int, k: int, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        # Precompute factorials and inv factorials up to m
        fact = [1] * (m + 1)
        for i in range(1, m + 1):
            fact[i] = fact[i-1] * i % MOD
        invfact = [1] * (m + 1)
        invfact[m] = pow(fact[m], MOD - 2, MOD)
        for i in range(m, 0, -1):
            invfact[i-1] = invfact[i] * i % MOD

        # Precompute powers nums[j]^c for c=0..m
        pow_nums = [[1] * (m + 1) for _ in range(n)]
        for j in range(n):
            for c in range(1, m + 1):
                pow_nums[j][c] = pow_nums[j][c-1] * (nums[j] % MOD) % MOD

        # dp[used][carry][ones] -> value (without multiplying by m!)
        # Initialize dp for pos = 0
        # Dimensions: used in [0..m], carry in [0..m], ones in [0..k]
        dp = [[[0] * (k + 1) for _ in range(m + 1)] for _ in range(m + 1)]
        dp[0][0][0] = 1

        for pos in range(n):
            nxt = [[[0] * (k + 1) for _ in range(m + 1)] for _ in range(m + 1)]
            pows = pow_nums[pos]
            for used in range(0, m + 1):
                max_c = m - used
                for carry in range(0, m + 1):
                    row = dp[used][carry]
                    # quick skip if entire row zeros
                    if all(v == 0 for v in row):
                        continue
                    for ones in range(0, k + 1):
                        cur = row[ones]
                        if cur == 0:
                            continue
                        # choose c occurrences of index pos
                        # multiply by nums[pos]^c * invfact[c]
                        for c in range(0, max_c + 1):
                            new_used = used + c
                            s = carry + c
                            bit = s & 1
                            new_ones = ones + bit
                            if new_ones > k:
                                continue
                            new_carry = s >> 1
                            add = cur * pows[c] % MOD * invfact[c] % MOD
                            nxt[new_used][new_carry][new_ones] = (nxt[new_used][new_carry][new_ones] + add) % MOD
            dp = nxt

        # Sum final states where used == m and ones + popcount(carry) == k
        ans = 0
        final_row = dp[m]
        for carry in range(0, m + 1):
            # popcount of carry
            pc = carry.bit_count()
            for ones in range(0, k + 1):
                if ones + pc == k:
                    ans = (ans + final_row[carry][ones]) % MOD

        # multiply by m! for multinomial factor
        ans = ans * fact[m] % MOD
        return ans
```
- Notes about the approach:
  - We factor sequences into counts c_j; account for ordered sequences via the multinomial factor m! / prod c_j!. We accumulate prod(nums[j]^{c_j} / c_j!) in DP and multiply by m! at the end.
  - DP iterates positions (the exponents / bit positions), tracks how many items used so far, the carry into the next bit, and how many ones (set bits) we've produced so far from lower bits. After processing all positions, leftover carry's popcount contributes remaining set bits.
  - Time complexity: roughly O(n * (m+1)^2 * (k+1) * avg_c) which is about O(n * m^3) in the worst case. With m ≤ 30 and n ≤ 50 this fits comfortably. Space complexity: O(m^2 * k).
  - Implementation details: precompute factorials and inverse factorials for dividing by c_j! mod MOD and precompute nums[j]^c for speeds. We cap ones at k to prune states.