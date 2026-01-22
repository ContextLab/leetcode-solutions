# [Problem 1072: Flip Columns For Maximum Number of Equal Rows](https://leetcode.com/problems/flip-columns-for-maximum-number-of-equal-rows/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Flipping a column toggles that bit in every row. If we pick a set of columns to flip (a mask), each row is XORed with the same mask. Two rows can be made identical by the same column flips iff they are either already equal or exact bitwise complements of each other — because XORing by some mask can transform a row into another iff row_a XOR mask = row_b, so mask = row_a XOR row_b. For that mask to be the same for multiple rows to map to the same target pattern, their pairwise XORs must be equal; equivalently, rows that are complements of each other share a simple relationship.

A convenient normalization: for any row, XOR it with its first bit (i.e., if first bit is 1, flip all bits; if 0, leave as-is). This makes the first bit 0 for all normalized rows; rows that are equal or complements will normalize to the same pattern. So we can count normalized patterns and take the max frequency.

## Refining the problem, round 2 thoughts
- Implementation: for each row produce a tuple (or string) of bits normalized by XORing with row[0]: normalized = tuple(x ^ row[0] for x in row). Count frequencies with a dict/Counter.
- Edge cases: small matrices (1x1), all identical rows, all complementary rows — handled naturally.
- Complexity: we visit every element once, O(m * n) time, and store up to m keys each of length n, so O(m * n) space.
- Alternative: could encode rows as integers/bitmasks (if n <= 300 might need big ints or multiple ints), but tuple is simple and fast enough in Python for constraints.

## Attempted solution(s)
```python
from collections import Counter
from typing import List

class Solution:
    def maxEqualRowsAfterFlips(self, matrix: List[List[int]]) -> int:
        """
        Normalize each row by XORing every entry with the row's first entry.
        This maps rows and their complements to the same key. Count frequencies
        of normalized rows and return the maximum count.
        """
        freq = Counter()
        for row in matrix:
            first = row[0]
            key = tuple(x ^ first for x in row)
            freq[key] += 1
        return max(freq.values()) if freq else 0
```
- Notes:
  - Approach: Normalize each row by XOR with its first bit so that a row and its complement share the same normalized pattern. The answer is the maximum frequency of any normalized pattern.
  - Time complexity: O(m * n) where m is number of rows and n is number of columns (each element processed once).
  - Space complexity: O(m * n) in the worst case to store normalized keys (m keys each of length n).
  - This is simple, clear, and fits the constraints (m, n <= 300).