# [Problem 2840: Check if Strings Can be Made Equal With Operations II](https://leetcode.com/problems/check-if-strings-can-be-made-equal-with-operations-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I notice the allowed swap requires indices i and j such that j - i is even, i.e., i and j have the same parity. That means characters at even indices can be freely permuted among even indices, and characters at odd indices can be freely permuted among odd indices. Swaps are allowed on either string any number of times, so effectively we can rearrange s1's evens and odds arbitrarily and likewise for s2. Therefore, to make s1 equal s2 we need the multiset of characters at even positions in s1 to match the multiset at even positions in s2, and similarly the multisets of odd-positioned characters must match. If either parity's multisets differ, it's impossible.

## Refining the problem, round 2 thoughts
This reduces to counting characters separately for even and odd indices for both strings and comparing counts. Edge cases: n = 1 simply requires s1 == s2. Complexity target: O(n) time, O(1) extra space (only 26-letter counters). Using collections.Counter is fine but we can also use fixed-size arrays of length 26 for efficiency. Both strings are same length per constraints. Return True iff both parity-counts match.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def checkStrings(self, s1: str, s2: str) -> bool:
        if len(s1) != len(s2):
            return False

        # Two counters for s1 (even, odd) and two for s2 (even, odd)
        # Use lists of size 26 for lowercase letters
        a_even = [0] * 26
        a_odd = [0] * 26
        b_even = [0] * 26
        b_odd = [0] * 26

        for i, (c1, c2) in enumerate(zip(s1, s2)):
            idx1 = ord(c1) - ord('a')
            idx2 = ord(c2) - ord('a')
            if (i & 1) == 0:  # even index
                a_even[idx1] += 1
                b_even[idx2] += 1
            else:             # odd index
                a_odd[idx1] += 1
                b_odd[idx2] += 1

        # Compare counts for even positions and odd positions
        return a_even == b_even and a_odd == b_odd
```
- Notes:
  - Approach: Separate characters by index parity and compare multisets for s1 and s2 on each parity.
  - Time complexity: O(n) where n = len(s1) (single pass to build counts, constant-time comparison of fixed-size lists).
  - Space complexity: O(1) extra space (four lists of size 26 regardless of n).
  - This is sufficient because within each parity class you can permute characters arbitrarily using the allowed swaps, so matching multisets is necessary and sufficient.