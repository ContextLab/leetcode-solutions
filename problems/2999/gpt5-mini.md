# [Problem 2999: Count the Number of Powerful Integers](https://leetcode.com/problems/count-the-number-of-powerful-integers/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to count integers x in [start, finish] such that:
- x ends with string s (i.e., decimal representation's suffix equals s),
- every decimal digit of x is <= limit.

Let m = len(s). Any such x can be seen as concatenation: prefix (possibly empty) + s. If prefix length p = 0 then x == s. If p >= 1 the prefix is a p-digit decimal number whose first digit cannot be 0 (otherwise the overall integer would have a leading zero), and every digit of the prefix must be in [0..limit] with the first in [1..limit].

Numeric value: x = prefix * 10^m + s_val. For fixed p, prefix ranges over p-digit numbers with digit constraints. We want prefixes such that x in [start, finish] => prefix in [ceil((start - s_val)/10^m), floor((finish - s_val)/10^m)] intersected with p-digit numbers.

Thus the subproblem: count p-digit integers in interval [lo..hi] whose digits each are <= limit and first digit >=1. This is a standard digit-DP counting <= N with digit constraints. We'll compute count(hi) - count(lo-1) for each applicable p. p ranges from 0 to max possible given finish's digits.

## Refining the problem, round 2 thoughts
Edge cases:
- p = 0: simply check if integer(s) lies in [start, finish].
- start - s_val could be negative; ceil division must be handled properly.
- lo and hi must also respect p-digit bounds: [10^{p-1}, 10^p - 1] (for p>=1).
- If lo > hi skip.
- The constraint s has digits <= limit already (given).
- finish up to 1e15 => up to 16 digits, so p is small and the digit-DP per p is cheap.

Complexity:
- For each p (<= ~16) we run a digit-DP of length p: O(p * (limit+1)) states/actions. Overall trivial.

We'll implement:
- ceil_div helper: ceil_div(a, b) = -((-a)//b) for integer safety.
- digit-DP function count_le(N, p, limit): number of p-digit numbers <= N with digits in allowed set and first digit >=1.
- For each p compute lo and hi, then accumulate count_le(hi) - count_le(lo-1).

## Attempted solution(s)
```python
from functools import lru_cache

class Solution:
    def powerfulIntegers(self, start: int, finish: int, limit: int, s: str) -> int:
        # Convert s to integer and setup
        s_val = int(s)
        m = len(s)
        pow10_m = 10 ** m

        # Helper: ceil division for integers (b > 0)
        def ceil_div(a, b):
            return -((-a) // b)

        # Digit-DP: count p-digit numbers <= N where:
        # - first digit in [1..limit]
        # - other digits in [0..limit]
        # Return 0 if N < 10^(p-1)
        def count_p_digit_le(N: int, p: int, limit: int) -> int:
            if p == 0:
                return 0
            lo_bound = 10 ** (p - 1)
            hi_bound = 10 ** p - 1
            if N < lo_bound:
                return 0
            if N >= hi_bound:
                # all p-digit numbers that respect digit constraints:
                # first digit choices: 1..limit -> limit choices
                # other (p-1) digits: 0..limit -> (limit+1)^(p-1)
                return limit * ((limit + 1) ** (p - 1))

            # build digit list of N with exactly p digits
            sN = str(N)
            if len(sN) != p:
                # N is between lo_bound and hi_bound but may have fewer digits due to leading zeros?
                # If len < p then N < 10^(p-1) already handled above
                sN = sN.zfill(p)
            digits = list(map(int, sN))

            @lru_cache(None)
            def dfs(pos: int, tight: bool) -> int:
                # pos from 0..p-1
                if pos == p:
                    return 1
                max_d = digits[pos] if tight else limit
                min_d = 1 if pos == 0 else 0
                if min_d > max_d:
                    return 0
                total = 0
                for d in range(min_d, max_d + 1):
                    if d > limit:
                        break
                    next_tight = tight and (d == digits[pos])
                    total += dfs(pos + 1, next_tight)
                return total

            return dfs(0, True)

        # main loop over possible prefix lengths p
        ans = 0
        max_digits = len(str(finish))
        max_p = max_digits - m
        if max_p < 0:
            # s is longer than any number up to finish -> only possible if start..finish includes s and s length fits
            max_p = -1

        # handle p = 0 separately (no prefix)
        if start <= s_val <= finish:
            # s's digits are guaranteed to be <= limit by constraints
            ans += 1

        # for p >= 1
        for p in range(1, max_p + 1):
            # prefix must satisfy:
            # prefix in [10^(p-1), 10^p - 1] and
            # prefix in [ceil((start - s_val)/10^m), floor((finish - s_val)/10^m)]
            lo_candidate = ceil_div(start - s_val, pow10_m)
            hi_candidate = (finish - s_val) // pow10_m

            lo = max(10 ** (p - 1), lo_candidate)
            hi = min(10 ** p - 1, hi_candidate)
            if lo > hi:
                continue

            cnt_hi = count_p_digit_le(hi, p, limit)
            cnt_lo_minus = count_p_digit_le(lo - 1, p, limit)
            ans += (cnt_hi - cnt_lo_minus)

        return ans
```
- Notes:
  - We convert each candidate x = prefix * 10^m + s_val and reduce counting to counting valid prefixes.
  - Counting valid prefixes in intervals is done via a small digit-DP that enforces per-digit upper bound limit and non-zero first digit.
  - ceil_div uses -((-a)//b) to safely compute ceil for possibly negative a.
  - Time complexity: For each p (<= ~16) we run a digit-DP O(p * limit) ~ small constant. Overall O(max_digits * max_digits * limit) worst-case, practically tiny.
  - Space complexity: recursion/memoization per DP uses O(p * states) also small.