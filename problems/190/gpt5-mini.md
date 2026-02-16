# [Problem 190: Reverse Bits](https://leetcode.com/problems/reverse-bits/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to reverse the bits of a 32-bit integer. The simplest idea is to build the reversed integer bit by bit: repeatedly take the least-significant bit of n and append it to the result (shifting result left each time). Loop exactly 32 times because the input is a 32-bit number (leading zeros matter). In languages with signed shifts I'd need to be careful about using an unsigned right shift; in Python n is non-negative here so >> works fine. Another straightforward approach is to convert to a 32-character binary string, reverse it, and parse back — readable but a bit heavier. For many repeated calls, a byte/16-bit lookup table would speed it up.

## Refining the problem, round 2 thoughts
- Edge cases: n = 0 (all zeros) and n with trailing zeros — the loop of 32 iterations handles them uniformly.
- In languages like Java/C++ be careful: use unsigned right shift (>>> in Java) to avoid sign extension. In Python the values given are non-negative so >> is safe.
- Time complexity for the bit-by-bit method is O(32) = O(1). Space O(1).
- For the follow-up (many calls), precompute reverse for 8-bit chunks (256 entries), then reverse 4 bytes and combine; this reduces work per call to 4 table lookups and shifts, helpful if called millions of times.

## Attempted solution(s)
```python
class Solution:
    def reverseBits(self, n: int) -> int:
        """
        Reverse the bits of a 32-bit integer n and return the resulting integer.
        """
        res = 0
        for _ in range(32):
            res = (res << 1) | (n & 1)
            n >>= 1
        return res
```
- Notes:
  - Approach: Iteratively take the least-significant bit of n (n & 1) and append it to res by shifting res left and OR-ing the bit. Repeat 32 times so all bits (including leading zeros) are processed.
  - Time complexity: O(32) = O(1) per call (constant time with a small fixed number of bit operations).
  - Space complexity: O(1).
  - Implementation details:
    - Works in Python because n is non-negative per problem constraints; >> behaves as logical right shift for non-negative integers.
    - Alternative simpler (but less bit-manipulation-oriented) solution: format(n, '032b')[::-1] and int(..., 2). That is concise but uses string operations.
    - Follow-up optimization: If called many times, build a lookup table for reversing 8-bit values (256 entries). Then split the 32-bit number into four bytes, reverse each via the table, and combine them with shifts — reduces per-call work to 4 lookups and shifts.