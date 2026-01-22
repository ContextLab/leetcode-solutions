# [Problem 3307: Find the K-th Character in String Game II](https://leetcode.com/problems/find-the-k-th-character-in-string-game-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I start from the definition: word initially "a". Each operation doubles the string length by appending either an identical copy (op 0) or a copy with every character advanced by 1 (op 1). Lengths grow exponentially (double each op), so we cannot build the string for large k (k up to 1e14). Typical trick: compute lengths after each operation and then trace k backwards from the final string to the original "a". When tracing back one operation:
- If k is in the first half, it corresponds to the same position in the prior string with no extra shift.
- If k is in the second half, it corresponds to position k - half in the prior string; and if that op was type 1, the character at that position was incremented by 1 (so we should add one to a shift counter).
By repeating backwards through operations, we reduce to the initial character 'a' plus the total number of increments (mod 26). Need to be careful with equality boundary (first half includes index == half) and capping lengths to avoid overflow while still correctly determining which half k falls into.

## Refining the problem, round 2 thoughts
Refinement details:
- Precompute lengths after each operation, capping at a safe INF > k (use 10**18) to avoid overflow but preserve comparisons against k.
- Iterate operations in reverse. For each op i, half = length before op. If k > half, we are in appended part: k -= half and if operations[i] == 1 then increment shift.
- Continue until all ops processed; starting char is 'a', apply shift modulo 26 to produce final char.
Edge cases:
- k exactly equals half: that is in first half (so use strict > to detect second half).
- operations length up to 100 ensures O(n) time is trivial.
Complexity:
- Time O(n) where n = len(operations) (<=100).
- Space O(n) for lengths array.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def findKthCharacter(self, k: int, operations: List[int]) -> str:
        # Precompute lengths after each operation, cap to a large INF (> max k)
        INF = 10**18
        n = len(operations)
        lengths = [1]  # lengths[i] = length after i operations? We'll keep lengths[i] = length after i ops done so far.
        for op in operations:
            lengths.append(min(lengths[-1] * 2, INF))
        
        # Work backwards to map k to position in original 'a', tracking total shifts
        shift = 0  # number of +1 shifts applied to the character
        # iterate operations from last to first; for op index i, the length before that op is lengths[i]
        for i in range(n - 1, -1, -1):
            half = lengths[i]  # length before operation i
            if k > half:
                # k is in appended half; map to original position
                k -= half
                # if operation was type 1, the appended half was shifted by +1
                if operations[i] == 1:
                    shift = (shift + 1) % 26
        
        # After reversing all ops, the character is original 'a' shifted by `shift`
        return chr((ord('a') - ord('a') + shift) % 26 + ord('a'))
```
- Approach: compute lengths (capped), walk operations backward, remap k to the corresponding index in the previous stage and accumulate shifts when k came from a type-1 appended half. Finally apply shift to initial 'a'.
- Time complexity: O(n) where n = len(operations) (<= 100).
- Space complexity: O(n) for lengths array.
- Implementation details: lengths are capped to INF (10**18) which is safely larger than max k (1e14) so comparisons k > half remain correct; equality k == half counts as first half. The shift is kept modulo 26 to get final character.