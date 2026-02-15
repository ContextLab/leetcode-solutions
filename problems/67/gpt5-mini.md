# [Problem 67: Add Binary](https://leetcode.com/problems/add-binary/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to add two binary strings and return their sum as a binary string. The natural way is to simulate binary addition from the least significant bit (the end of each string) toward the most significant bit, keeping a carry. Using two pointers starting at the ends of the strings and moving left while adding corresponding bits plus carry seems straightforward. Converting the whole strings to integers and adding (then converting back with bin()) would work in Python because of arbitrary-precision ints, but it's less instructive and might be less efficient in terms of intermediate memory for very long strings. I'll implement manual bit-by-bit addition with O(max(n, m)) time and space.

## Refining the problem, round 2 thoughts
Make sure to handle different lengths (one string can be longer than the other), and the final carry after processing all digits. Edge cases: "0" + "0", one empty? (constraints say length >= 1), leading zeros aren't present except for "0" itself but that doesn't affect the algorithm. The algorithm should:
- Use i, j pointers at the end of a and b;
- Maintain carry (0 or 1);
- Build result digits in reverse order (append characters to a list) then reverse/join at the end.
Time complexity: O(max(len(a), len(b))). Space complexity: O(max(len(a), len(b))) for the output (plus small constant extra).

## Attempted solution(s)
```python
class Solution:
    def addBinary(self, a: str, b: str) -> str:
        i, j = len(a) - 1, len(b) - 1
        carry = 0
        res = []
        
        while i >= 0 or j >= 0 or carry:
            total = carry
            if i >= 0:
                total += ord(a[i]) - ord('0')
                i -= 1
            if j >= 0:
                total += ord(b[j]) - ord('0')
                j -= 1
            
            # current bit is total % 2, new carry is total // 2
            res.append('1' if total % 2 else '0')
            carry = total // 2
        
        # res currently has LSB->MSB order, reverse to get proper string
        return ''.join(reversed(res))
```
- Notes:
  - Approach: two-pointer addition from right to left with a carry; build digits in reverse and reverse at the end.
  - Time complexity: O(max(len(a), len(b))) — each digit processed once.
  - Space complexity: O(max(len(a), len(b))) for the result (plus O(1) extra).
  - Implementation details: using ord(...) - ord('0') is slightly faster than int(...) per character; loop continues while there is any remaining digit or carry.