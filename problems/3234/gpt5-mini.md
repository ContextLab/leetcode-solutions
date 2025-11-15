# [Problem 3234: Count the Number of Substrings With Dominant Ones](https://leetcode.com/problems/count-the-number-of-substrings-with-dominant-ones/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to count substrings where the number of ones o >= (number of zeros z)^2. If z is large the square grows quickly; since s.length <= 4e4, z cannot be very large in any valid substring because z^2 would exceed n. That suggests we can bound the number of zeros we need to consider per substring by ~sqrt(n) (about 200). So an approach that iterates over each starting index and tries all feasible zero counts up to that bound seems plausible.

We can use the positions of zeros to quickly locate the substring that contains exactly c zeros starting from index i: the c-th zero position gives the leftmost index where c zeros are included, and the next zero (if any) bounds the maximum end index before increasing zero count. For each such block we can compute the minimal end index required by the inequality and count how many end indices in that block satisfy it.

This yields O(n * sqrt(n)) time which should be fine for n up to 4e4.

## Refining the problem, round 2 thoughts
- Precompute the positions of zeros in s. Let pos be that list.
- For a given start index i and a given zero-count c >= 1:
  - The earliest r that includes c zeros is pos[posIdx + c - 1] where posIdx is the index in pos of the first zero >= i.
  - The largest r without including the (c+1)-th zero is pos[posIdx + c] - 1, or n-1 if none.
  - The inequality o >= c^2 where o = (r - i + 1) - c rearranges to r >= i - 1 + c + c^2.
  - So valid r are in [ max( earliest_r, required_r ), latest_r ].
- For c = 0 (no zeros) substrings must be all-ones; those are always valid. We can count all substrings starting at i that contain no zero simply as nextZero(i) - i.
- Iterate i from 0..n-1, maintain a pointer into pos so we can find posIdx quickly (amortized O(1) move as i increases). For each i, iterate c from 1..K where K ~ sqrt(n) (stop earlier if we run out of zeros).
- Complexity: O(n * sqrt(n)) time, O(n) extra space for zero positions.

Edge cases:
- All ones -> every substring valid. Our c=0 counting captures those.
- All zeros -> possible only small substrings might satisfy; algorithm handles since pos list is full but c^2 quickly becomes large and restricts r.
- Careful about indexing and bounds when posIdx + c - 1 or posIdx + c exceeds pos length.

## Attempted solution(s)
```python
import math
from typing import List

class Solution:
    def numberOfSubstrings(self, s: str) -> int:
        n = len(s)
        pos = [i for i, ch in enumerate(s) if ch == '0']
        m = len(pos)
        # Upper bound for zero count to check: if c^2 > n then impossible
        K = int(math.sqrt(n)) + 2

        ans = 0

        # First count substrings with 0 zeros (all-ones substrings).
        # For each start i, number of substrings starting at i with zero zeros:
        # nextZero(i) - i (where nextZero(i) is index of first zero >= i, or n)
        p = 0
        for i in range(n):
            while p < m and pos[p] < i:
                p += 1
            next_zero = pos[p] if p < m else n
            # substrings s[i..r] with r in [i, next_zero-1] are zero-zero substrings
            ans += (next_zero - i)

        # Now count substrings with c >= 1 zeros, for c up to K (practically <= sqrt(n))
        p = 0
        for i in range(n):
            # advance pointer to first zero index >= i
            while p < m and pos[p] < i:
                p += 1
            # try each zero count c
            for c in range(1, K + 1):
                j = p + c - 1  # index in pos of the c-th zero from start i
                if j >= m:
                    break  # not enough zeros remaining to have c zeros
                earliest_r = pos[j]  # minimal r that includes c zeros
                required_r = i - 1 + c + c * c  # from o >= c^2 => r >= ...
                lower = max(earliest_r, required_r)
                # upper bound: before the (c+1)-th zero, or end of string
                if p + c < m:
                    upper = pos[p + c] - 1
                else:
                    upper = n - 1
                if lower <= upper:
                    ans += (upper - lower + 1)

        return ans
```
- Notes about the solution:
  - We precompute zero positions to jump to the c-th zero quickly.
  - For c = 0 we add next_zero(i) - i for each start index i; this counts all substrings consisting only of ones starting at i.
  - For c >= 1 we compute the valid r-range intersection between (a) indices that include exactly c zeros and (b) indices satisfying the inequality. Add the length of that intersection when non-empty.
  - Time complexity: O(n * sqrt(n)) because for each of the n start indices we iterate c up to ~sqrt(n). With n <= 4e4 this is about <= 8e6 iterations, which is efficient.
  - Space complexity: O(n) for storing positions of zeros.
  - Careful bound handling ensures correctness at string endpoints and when zeros run out.