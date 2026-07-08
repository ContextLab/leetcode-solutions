# [Problem 3756: Concatenate Non-Zero Digits and Multiply by Sum II](https://leetcode.com/problems/concatenate-non-zero-digits-and-multiply-by-sum-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need for each query on substring s[l..r] to remove zeros, concatenate the remaining digits into an integer x, compute sum of digits of x, and return x * sum (mod 1e9+7). Doing this naively per query (scan substring, build integer by repeated *10 and add) could be O(length) per query → worst-case O(m * q) which is too slow (m and q up to 1e5).

Observation: zeros are just ignored. If we collect all non-zero digits in order into an array A, then for a substring we only need a contiguous slice of A corresponding to non-zero digits with positions between l and r. So map original indices -> positions in A, and then queries reduce to taking A[i..j]. Concatenation of digits A[i..j] can be expressed with prefix concatenation values using powers of 10:
prefixVal[t] = concat(A[1..t]) (mod M). Then concat(A[i..j]) = prefixVal[j] - prefixVal[i-1] * 10^{j-i+1} (mod M). Also digit sum is prefixSum[j] - prefixSum[i-1]. So with precomputed arrays + binary search on positions we can answer each query in O(log N_nonzero) time.

## Refining the problem, round 2 thoughts
- Build arrays:
  - pos: positions in s of each non-zero digit (sorted by index).
  - digits: the corresponding digits (1..9).
  - prefVal: prefix concatenated values modulo MOD.
  - pow10: powers of 10 modulo MOD up to number of non-zero digits.
  - prefSum: prefix sums of digits (regular integers).
- For query [l,r], find i = first index in pos with pos[i] >= l (bisect_left), j = last index with pos[j] <= r (bisect_right - 1).
  - If i > j then no non-zero digits → answer 0.
  - Else compute length = j - i + 1, x_mod = (prefVal[j+1] - prefVal[i] * pow10[length]) % MOD (using 1-based pref arrays), sum_digits = prefSum[j+1] - prefSum[i].
  - Return (x_mod * sum_digits) % MOD.
- Complexity: preprocessing O(m) to build arrays and O(N_nonzero) to compute prefix arrays. Each query O(log N_nonzero). Total O(m + q log m). Space O(N_nonzero).
- Edge cases: substring contains only zeros → answer 0. Single non-zero digit works fine.

## Attempted solution(s)
```python
from typing import List
import bisect

class Solution:
    def concatenateNonZeroDigitsAndMultiplyBySumII(self, s: str, queries: List[List[int]]) -> List[int]:
        MOD = 10**9 + 7

        # Collect non-zero digits and their positions
        pos = []
        digits = []
        for idx, ch in enumerate(s):
            if ch != '0':
                pos.append(idx)
                digits.append(ord(ch) - ord('0'))

        n = len(digits)
        # Precompute powers of 10 modulo MOD
        pow10 = [1] * (n + 1)
        for i in range(1, n + 1):
            pow10[i] = (pow10[i-1] * 10) % MOD

        # prefVal[t] = concatenation of digits[0..t-1] modulo MOD (1-based semantics)
        prefVal = [0] * (n + 1)
        for t in range(1, n + 1):
            prefVal[t] = (prefVal[t-1] * 10 + digits[t-1]) % MOD

        # prefix sums of digits (for sum of digits)
        prefSum = [0] * (n + 1)
        for t in range(1, n + 1):
            prefSum[t] = prefSum[t-1] + digits[t-1]

        ans = []
        for l, r in queries:
            # find indices in digits array whose positions lie in [l, r]
            i = bisect.bisect_left(pos, l)        # first index with pos[i] >= l
            j = bisect.bisect_right(pos, r) - 1   # last index with pos[j] <= r
            if i > j:
                ans.append(0)
            else:
                L = i + 1  # convert to 1-based for pref arrays
                R = j + 1
                length = R - L + 1
                # concatenated value modulo MOD
                x_mod = (prefVal[R] - prefVal[L-1] * pow10[length]) % MOD
                sum_digits = prefSum[R] - prefSum[L-1]
                ans.append((x_mod * (sum_digits % MOD)) % MOD)
        return ans
```
- Notes on approach:
  - We reduce the problem to queries on the subsequence of non-zero digits.
  - Use prefix concatenation with powers of 10 to extract any sub-concatenation in O(1) after binary search to find boundaries.
  - Time complexity: O(m + n + q log n) where n is number of non-zero digits (n <= m). Preprocessing O(m), each query O(log n) for bisect.
  - Space complexity: O(n) for pos, digits, pow10, prefVal, prefSum.
  - Handles edge cases where there are no non-zero digits in the substring (returns 0). Modulo arithmetic is used for concatenated values and final multiplication.