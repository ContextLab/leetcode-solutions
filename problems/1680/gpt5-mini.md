# [Problem 1680: Concatenation of Consecutive Binary Numbers](https://leetcode.com/problems/concatenation-of-consecutive-binary-numbers/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the decimal value of the binary string produced by concatenating binary representations of 1..n, modulo 1e9+7. Naively building the big binary string and converting would be too slow and memory-heavy for large n (and the binary string grows roughly n*log n). But we can build the numeric value incrementally: when we append the binary of a number x to the current value val, that's equivalent to shifting val left by the number of bits in x and then adding x. So maintain a running integer, shift by bit-length(x), add x, and take modulo each step to avoid huge numbers. We need an efficient way to get the bit-length of x: either use x.bit_length() or increment a counter whenever x is a power of two (bit-length increases when x hits 1,2,4,8,...).

## Refining the problem, round 2 thoughts
- Edge cases: n = 1 should return 1. For larger n up to 1e5, O(n) iteration is fine.
- Use modulo at every step to keep numbers bounded and avoid Python big-int blowup.
- To compute the bit-length cheaply we can check if x is a power of two via (x & (x-1)) == 0 and increment a length counter; this avoids calling bit_length() each iteration (though bit_length is also O(1)).
- Time complexity: O(n). Space complexity: O(1).
- Correctness: shifting then adding exactly models concatenation of binary strings.

## Attempted solution(s)
```python
class Solution:
    def concatenatedBinary(self, n: int) -> int:
        MOD = 10**9 + 7
        result = 0
        bits = 0  # current bit-length for the next number to append

        for x in range(1, n + 1):
            # Increase bits when x is a power of two (1,2,4,8,...)
            if x & (x - 1) == 0:
                bits += 1
            # Shift current result left by bits and add x, take modulo to keep values small
            result = ((result << bits) | x) % MOD

        return result
```
- Approach: iterate x from 1 to n, maintain the number of bits of x (increment when x is a power of two), left-shift the accumulated result by that many bits, add x, and take modulo 1e9+7.
- Time complexity: O(n) iterations, each step constant time → O(n).
- Space complexity: O(1) extra space.
- Implementation detail: using bitwise shift and OR mimics concatenation; modulo after each step prevents large intermediate integers. Checking power-of-two with (x & (x-1)) == 0 is an efficient way to know when the bit-length increases.