# [Problem 1758: Minimum Changes To Make Alternating Binary String](https://leetcode.com/problems/minimum-changes-to-make-alternating-binary-string/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I see a string of '0' and '1' and we want no two adjacent characters equal. An alternating string must be either "0101..." or "1010..." depending on the first character. So the minimum flips is how many characters differ from one of these two patterns — take the smaller of the two counts. A brute force could try flipping greedily, but it's equivalent and simpler to just compare with the two ideal patterns. Complexity should be O(n). Edge cases: length 1 (already alternating), all same characters (need about n/2 flips).

## Refining the problem, round 2 thoughts
- Two possible target patterns only: start with '0' or start with '1'.
- We can count mismatches for both targets in a single pass without building target strings to save memory.
- Return min(mismatches_for_target0, mismatches_for_target1).
- Time complexity O(n), space O(1).
- Handle small n trivially; algorithm covers all lengths.
- Implementation detail: use index parity (i % 2 or i & 1) to determine expected char.

## Attempted solution(s)
```python
class Solution:
    def minOperations(self, s: str) -> int:
        # count mismatches against pattern starting with '0' and pattern starting with '1'
        mismatches0 = 0  # pattern "0101..."
        mismatches1 = 0  # pattern "1010..."
        for i, ch in enumerate(s):
            if (i & 1) == 0:  # even index: expected '0' for pattern0, '1' for pattern1
                if ch != '0':
                    mismatches0 += 1
                if ch != '1':
                    mismatches1 += 1
            else:  # odd index: expected '1' for pattern0, '0' for pattern1
                if ch != '1':
                    mismatches0 += 1
                if ch != '0':
                    mismatches1 += 1
        return min(mismatches0, mismatches1)
```
- Approach: Count mismatches for both possible alternating patterns (start with '0' or start with '1') in one pass and return the smaller count.
- Time complexity: O(n), where n = len(s), because we inspect each character exactly once.
- Space complexity: O(1), only a couple of integer counters used.
- Implementation details: Using i & 1 for parity check is slightly faster than i % 2; we do not construct any auxiliary strings. This handles all edge cases, including length 1 or strings where all characters are identical.