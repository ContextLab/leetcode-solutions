# [Problem 1009: Complement of Base 10 Integer](https://leetcode.com/problems/complement-of-base-10-integer/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to flip every bit in the binary representation of n and return the resulting integer. The main detail is that only the meaningful bits (up to the highest 1) should be flipped — leading zeros are not part of the representation and shouldn't be flipped. A straightforward way: get the bit-length of n, build a mask that has 1s in every position up to that length, then XOR n with the mask. Edge case: n = 0 (binary "0") — its complement should be 1. Alternatives: convert to binary string and replace characters, or iterate bit-by-bit to construct the complement. Bit operations should be simplest and most efficient.

## Refining the problem, round 2 thoughts
Refine: use n.bit_length() to find number of meaningful bits. If bit_length is L, then mask = (1 << L) - 1 has L ones (e.g., L=3 -> mask=0b111). Then answer = n ^ mask. For n = 0, bit_length() is 0, so mask becomes 0; but complement should be 1, so handle n == 0 explicitly (return 1). Alternatively, we could set mask = 1 if L == 0. Time complexity: computing bit_length and doing shifts / xor is O(1) with respect to fixed-size integers, or O(log n) in the number of bits; space O(1). Also mention string-based approach (bin -> flip chars -> int) which is fine but less direct.

## Attempted solution(s)
```python
class Solution:
    def bitwiseComplement(self, n: int) -> int:
        # Edge case: the complement of 0 (binary "0") is 1 (binary "1")
        if n == 0:
            return 1
        # Number of bits in n (excluding leading zeros)
        bits = n.bit_length()
        # Mask with 'bits' ones, e.g., bits=3 -> mask=0b111
        mask = (1 << bits) - 1
        # XOR n with mask flips all bits within the bit-length
        return n ^ mask
```
- Notes:
  - Approach: Use bit_length to find meaningful bits, build a mask of that many 1s, and XOR to flip bits.
  - Time complexity: O(1) in typical machine model (or O(log n) related to number of bits). Space complexity: O(1).
  - Handles edge case n = 0 explicitly (returns 1). Alternative implementations could use string manipulation (bin/replace) or iteratively building the mask by shifting until it covers n.