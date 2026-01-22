# [Problem 2429: Minimize XOR](https://leetcode.com/problems/minimize-xor/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need an integer x that has the same number of 1-bits as num2 and minimizes x XOR num1. Minimizing XOR means making x as "close" to num1 as possible in binary. If x could equal num1 (i.e., num1 has the same popcount as num2), that's optimal. Otherwise we should change bits of num1 minimally to match the required number of set bits.

Intuitively, flipping lower-significance bits changes the numeric value less than flipping higher bits. So to change the number of set bits of num1 to match num2, it's optimal to add or remove 1s starting from the least significant bits (LSB) upward.

So:
- If num1 has fewer 1s than num2, set zero bits of num1 starting from LSB until counts match.
- If num1 has more 1s, clear one bits of num1 starting from LSB until counts match.

This should minimize the absolute difference and thus XOR.

## Refining the problem, round 2 thoughts
Edge cases:
- num1 == num2 (trivial).
- Need to set bits beyond current highest bit of num1: that's fine — we'll iterate enough bit positions.
- The constraints (<= 1e9) mean ~30 bits, so iterating 32 bits is safe and constant-time.

Alternative approaches:
- Build x directly by counting bits to place: try to match high bits of num1 first to minimize XOR (but that reduces to the same LSB-first trick when adjusting counts).
- Using sorting of bit positions by significance; but a simple loop from LSB up is simpler and O(1).

Complexity:
- We loop over a constant number of bit positions (<= 32), so O(1) time and O(1) space. More generally, O(B) where B is number of bits considered.

## Attempted solution(s)
```python
class Solution:
    def minimizeXor(self, num1: int, num2: int) -> int:
        # count set bits
        c1 = bin(num1).count("1")
        c2 = bin(num2).count("1")
        if c1 == c2:
            return num1

        x = num1
        if c1 < c2:
            # Need to add (c2 - c1) ones: set zero bits starting from LSB
            need = c2 - c1
            i = 0
            while need > 0:
                if (x >> i) & 1 == 0:
                    x |= (1 << i)
                    need -= 1
                i += 1
        else:
            # Need to remove (c1 - c2) ones: clear one bits starting from LSB
            need = c1 - c2
            i = 0
            while need > 0:
                if (x >> i) & 1 == 1:
                    x &= ~(1 << i)
                    need -= 1
                i += 1

        return x
```
- Notes:
  - Approach: adjust num1's bits starting from the least significant bit to match num2's popcount. Setting/clearing lower bits first minimizes change to num1 and thus minimizes XOR.
  - Time complexity: O(B) where B is number of bits inspected (constant ~32 for given constraints) → effectively O(1).
  - Space complexity: O(1).
  - Implementation detail: use bit shifts and masks to check/set/clear bits. The while loops may go beyond current highest bit if needed, but given constraints this remains bounded.