# [Problem 693: Binary Number with Alternating Bits](https://leetcode.com/problems/binary-number-with-alternating-bits/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
If I need to check whether the bits alternate, the straightforward idea is to look at the binary representation and ensure every bit differs from the previous one. Converting to a string of '0'/'1' and scanning is simple and easy to reason about, but there's also a neat bitwise pattern: if bits alternate (e.g., 101010 or 0101), then n XOR (n >> 1) becomes a sequence of 1s (e.g., 11111). A number that's a consecutive sequence of 1s has the property x & (x + 1) == 0 (because x + 1 flips all of those low 1s to 0s and adds a carry). So compute x = n ^ (n >> 1) and test x & (x + 1) == 0. That avoids converting to strings and runs in O(1) time.

## Refining the problem, round 2 thoughts
Edge cases: n = 1 should return True (binary "1" trivially alternating). The bitwise trick works for any positive integer (Python integer arithmetic handles sizes). Alternative approach: iterate bits with last_bit variable, shift n right and compare adjacent bits — O(number of bits) time which is still O(1) for fixed 32-bit inputs but conceptually O(log n). The bitwise XOR + power-of-two-minus-one test is compact and constant-time in practice. Space is O(1) either way.

## Attempted solution(s)
```python
class Solution:
    def hasAlternatingBits(self, n: int) -> bool:
        """
        Check if n has alternating bits using bitwise trick:
        If bits alternate, x = n ^ (n >> 1) is a sequence of 1s.
        A sequence of 1s has the property x & (x + 1) == 0.
        """
        x = n ^ (n >> 1)
        return (x & (x + 1)) == 0
```
- Notes:
  - Approach: compute x = n ^ (n >> 1). If n's bits alternate, x equals binary 111... (a run of 1s). Check that x is of the form 2^k - 1 by testing x & (x + 1) == 0.
  - Time complexity: O(1) — a constant number of bitwise operations (practically proportional to the word size, e.g., 32 or 64).
  - Space complexity: O(1).