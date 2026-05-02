# [Problem 788: Rotated Digits](https://leetcode.com/problems/rotated-digits/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count numbers in [1, n] that become a valid different number after rotating every digit 180 degrees. Valid digits after rotation: 0->0,1->1,8->8,2<->5,6<->9. Digits 3,4,7 are invalid. A number is "good" if (1) it contains no invalid digits and (2) at least one digit is in {2,5,6,9} so the rotated result differs from the original. The simplest approach that comes to mind is to iterate from 1 to n, check each number's digits for invalid digits and check if it contains any "changing" digit. n <= 10^4 so iterating is cheap. There's also a digit-DP / combinatorial counting approach for much larger n, but not necessary here.

## Refining the problem, round 2 thoughts
Refinements / edge cases:
- Single-digit numbers: 2,5,6,9 are good; 1,8,0 (0 not in range unless n>=0) are not good because they stay the same; 3,4,7 invalid.
- Leading zeros are not allowed in the original number, so we just inspect the decimal representation.
- Complexity: checking digits by converting to string is fine; each number has at most 5 digits for n<=10^4, so total work is small.
- Alternative methods: pre-generate valid numbers using BFS over allowed digits or do combinatorics (count all numbers with only {0,1,8,2,5,6,9} minus those with only {0,1,8}), but the simple loop is straightforward and clear.

## Attempted solution(s)
```python
class Solution:
    def rotatedDigits(self, n: int) -> int:
        invalid = {'3', '4', '7'}
        changing = {'2', '5', '6', '9'}
        count = 0
        for num in range(1, n + 1):
            s = str(num)
            # If any digit is invalid, skip
            if any(ch in invalid for ch in s):
                continue
            # If at least one digit changes, it's a good number
            if any(ch in changing for ch in s):
                count += 1
        return count
```
- Notes:
  - Approach: brute-force iterate over 1..n, skip numbers with invalid digits (3,4,7). Count numbers that contain at least one digit from {2,5,6,9} (so the rotated number differs).
  - Time complexity: O(n * d) where d is the number of digits (d = O(log10 n)). For the problem constraints (n <= 10^4), this is effectively O(n).
  - Space complexity: O(1) extra space (ignoring input/output and string conversion).
  - Implementation detail: using sets for quick membership checks makes the digit checks concise and efficient.