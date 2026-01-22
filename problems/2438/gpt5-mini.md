# [Problem 2438: Range Product Queries of Powers](https://leetcode.com/problems/range-product-queries-of-powers/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The phrase "minimum number of powers of 2 that sum to n" immediately suggests the binary representation of n: each set bit corresponds to a single power of two, and using each set bit's 2^k gives the minimal count. The array "powers" sorted non-decreasing is just the list of 2^k for each set bit k in increasing k order (i.e., 1,2,4,... for the set bits).

A query asking for the product of powers[left..right] becomes the product of some 2^k values. Multiplying 2^{k1} * 2^{k2} * ... = 2^{(k1+k2+...)}, so we only need the sum of the exponents in that index range. Thus build a prefix-sum of exponents (bit positions) and answer each query as pow(2, sum_exponents, MOD).

Because n <= 1e9, there are at most ~30 set bits, so building the list is trivial; queries can be up to 1e5 so answering must be O(1) per query after preprocessing.

## Refining the problem, round 2 thoughts
Implementation details:
- Extract indices k where (n >> k) & 1 == 1, in increasing order (k from 0 upward). That yields exponents list.
- Build prefix sum array pref where pref[i] = sum of exponents for first i entries (pref[0] = 0). Then exponent sum for [l,r] is pref[r+1] - pref[l].
- Answer = pow(2, exponent_sum, MOD).
Edge cases:
- n = 1 (powers = [1]) works: exponent 0, pow(2,0)=1.
- Single element queries or full-range queries handled correctly via prefix sums.
Complexity:
- Time O(B + Q) where B = number of bits (<= 30) and Q = number of queries (<= 1e5).
- Space O(B) extra.

Alternative approach: explicitly compute powers = [2^k % MOD] and prefix products mod MOD. That's fine too but using exponent sums is simpler and avoids repeated modular multiplications in preprocessing (though both are trivial here).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def rangeProductQueries(self, n: int, queries: List[List[int]]) -> List[int]:
        MOD = 10**9 + 7
        
        # collect exponents (k for which bit k of n is 1), in increasing order
        exponents = []
        k = 0
        temp = n
        while temp:
            if temp & 1:
                exponents.append(k)
            temp >>= 1
            k += 1
        
        # prefix sums of exponents
        pref = [0] * (len(exponents) + 1)
        for i, val in enumerate(exponents):
            pref[i+1] = pref[i] + val
        
        res = []
        for left, right in queries:
            exp_sum = pref[right+1] - pref[left]
            res.append(pow(2, exp_sum, MOD))
        
        return res
```
- Notes:
  - Approach: Use binary decomposition of n to get the minimal list of powers (each set bit yields 2^k). The product over a range equals 2^{sum of the exponents in that range}. Precompute prefix sums of exponents to answer each query in O(1).
  - Time complexity: O(B + Q), where B = number of bits set in n (≤ 30) and Q = number of queries.
  - Space complexity: O(B) for exponents and prefix sums (plus O(Q) for the output).
  - Implementation detail: we iterate through bits of n using bit shifts to build exponents in increasing order; pow with modulus gives the final answer efficiently.