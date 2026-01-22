# [Problem 2683: Neighboring Bitwise XOR](https://leetcode.com/problems/neighboring-bitwise-xor/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We are given derived[i] = original[i] XOR original[i+1] for i in [0..n-2], and derived[n-1] = original[n-1] XOR original[0]. We need to decide if there exists a binary original array (0/1 values) that produces the given derived.

First idea: try reconstructing original by picking original[0] = 0 or 1 and computing subsequent original values via original[i+1] = original[i] XOR derived[i]. After building up to original[n-1], we must check the circular constraint derived[n-1] == original[n-1] XOR original[0]. So we could try both initial guesses and see if one is consistent.

But maybe there's a simpler invariant: XOR all derived elements. Since XOR is associative and each original value appears exactly twice in the total XOR of all derived terms (original[0] appears in derived[0] and derived[n-1], original[1] appears in derived[0] and derived[1], etc.), the XOR of all derived entries equals XOR over all originals twice, i.e., 0. So a necessary condition is XOR_all(derived) == 0. Is it also sufficient? If XOR_all(derived) == 0, then reconstructing with any initial original[0] will produce original[n] == original[0], so the circular constraint holds. So the condition is both necessary and sufficient.

Edge case: n == 1. derived[0] must equal original[0] XOR original[0] == 0, so the same XOR-all == 0 condition applies.

So final answer: return True iff XOR of all derived elements is 0.

## Refining the problem, round 2 thoughts
- We can implement by computing a single xor accumulator across the array and checking if it's 0.
- Time complexity O(n) where n = len(derived), space O(1).
- No need to actually reconstruct original or try both starting values — the XOR invariant gives a direct answer.
- Confirmed for n=1 and general n.
- Implementation detail: derived entries are already 0/1, so simple integer xor works.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def doesValid(self, derived: List[int]) -> bool:
        """
        Return True if there exists a binary array `original` producing `derived`
        via neighboring XORs (with wrap-around), otherwise False.
        """
        xor_sum = 0
        for bit in derived:
            xor_sum ^= bit
        return xor_sum == 0
```
- Notes:
  - Approach: Use the invariant that XOR of all derived elements must be 0 (each original bit appears twice in the XOR of all derived entries).
  - Time complexity: O(n), where n = len(derived).
  - Space complexity: O(1) extra space.
  - Handles edge cases such as n = 1 (derived[0] must be 0).