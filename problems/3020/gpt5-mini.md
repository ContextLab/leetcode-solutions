# [Problem 3020: Find the Maximum Number of Elements in Subset](https://leetcode.com/problems/find-the-maximum-number-of-elements-in-subset/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We are given positive integers and need to pick a subset that can be arranged in a palindromic pattern of powers of some base x, where exponents used are 1,2,4,...,k and k is a power of two. The pattern is
[x, x^2, x^4, ..., x^(k/2), x^k, x^(k/2), ..., x^4, x^2, x].
So for a chosen base x and maximum exponent k = 2^m:
- each intermediate value x^(2^i) for i = 0..m-1 must appear at least twice (symmetric positions),
- the central value x^(2^m) must appear at least once.
We want the maximum possible length 2*m+1 across all choices of x and m.

Immediate thoughts:
- Count frequencies of all numbers.
- For each candidate base x present, build the sequence v0 = x, v1 = x^2, v2 = x^4, ... while these values remain <= 1e9 and exist in the multiset.
- Let L be how many distinct values in that chain are present (v0..v_{L-1}). Let pair be the number of leading values among these that have freq >= 2 (contiguous from v0).
- A valid m must satisfy: m <= pair and m <= L-1 (because v_m must exist). So m_max = min(pair, L-1), giving length = 2*m_max + 1.
- Special-case x = 1: squaring 1 stays 1, and the pattern collapses to repeated 1s. We can use all ones: answer contribution = freq[1].

Because values grow quickly by squaring, chains are very short for bases > 1, so iterating over all distinct bases is efficient.

## Refining the problem, round 2 thoughts
- Handle x = 1 specially: answer can be freq[1] (we can choose any m because x^(2^i) == 1 for all i).
- For x > 1, each step v <- v * v grows fast; the chain length is O(log log maxVal) (tiny), so iterating every distinct x is fine.
- Use Counter to get frequencies.
- For each x:
  - compute successive v values while v <= maxVal and v in the counter; collect them into a list.
  - compute pair = number of consecutive entries from start with freq >= 2.
  - m_max = min(pair, L-1). length = 2*m_max + 1.
- Edge cases: base present only once -> length 1. Very large numbers may overflow if squared; check v > maxVal and stop. Use Python ints but still stop after exceeding maxVal.
- Complexity: O(n + D * chainLen) where D is number of distinct values and chainLen is very small (<= ~6 for typical bounds). So very efficient.

## Attempted solution(s)
```python
from collections import Counter
from typing import List

class Solution:
    def maxSubset(self, nums: List[int]) -> int:
        freq = Counter(nums)
        maxVal = max(nums)
        ans = 0

        # Special-case x == 1: all ones can be used
        if 1 in freq:
            ans = max(ans, freq[1])

        # Consider each distinct base > 1
        for x in freq:
            if x == 1:
                continue
            # build the chain of present values v0=x, v1=x^2, v2=x^4, ...
            chain = []
            v = x
            while v <= maxVal and v in freq:
                chain.append(v)
                # next v is v^2; break if it will exceed maxVal
                if v > maxVal // v:
                    break
                v = v * v

            if not chain:
                continue

            # count how many initial chain values have freq >= 2
            pair = 0
            for val in chain:
                if freq[val] >= 2:
                    pair += 1
                else:
                    break

            # m must be <= pair and also <= L-1 (since v_m must exist)
            L = len(chain)
            m_max = min(pair, L - 1)
            curr_len = 2 * m_max + 1
            ans = max(ans, curr_len)

        return ans
```
- Notes on approach: We iterate every distinct element as a possible base x. For x > 1 the sequence v, v^2, v^4, ... grows extremely fast so each chain is short; for x = 1 we handle separately (all ones can be used). For each chain we compute how many initial values have at least two occurrences (these form the symmetric pairs) and ensure the middle value exists (so m <= L-1). The maximum length from that base is 2*m_max + 1.
- Time complexity: O(n + D * chainLen). D is number of distinct values, chainLen is O(log log maxVal) (very small, typically <= 6), so practically O(n).
- Space complexity: O(D) for the frequency map and small extra for chain lists.