# [Problem 3751: Total Waviness of Numbers in Range I](https://leetcode.com/problems/total-waviness-of-numbers-in-range-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to compute the total number of peaks and valleys across every integer in [num1, num2]. A peak/valley is defined for a digit that has both neighbors (so only digits at indices 1..len-2 matter). For each number, waviness is just a count over its interior digits: check if digit[i] > both neighbors (peak) or < both neighbors (valley). The simplest approach is to iterate every number in the range, convert to digits, count interior peaks/valleys, and sum.

Constraints are small: num2 <= 1e5 so at most 100k numbers and each number has at most 6 digits. A brute-force per-number digit check (O(range_length * digits)) is perfectly fine. Could consider DP or combinatorics for much larger bounds, but unnecessary here.

Edge-case thought: numbers with fewer than 3 digits contribute zero. Need to ensure first/last digits aren't counted. Also watch leading zeros are not present (we use string of number).

## Refining the problem, round 2 thoughts
Refine: iterate n from num1 to num2 inclusive. For each n:
- If n < 100, skip (waviness 0).
- Turn n into list of ints digits = list(map(int, str(n))).
- For i from 1 to len(digits)-2 inclusive, check (digits[i] > digits[i-1] and digits[i] > digits[i+1]) or (digits[i] < digits[i-1] and digits[i] < digits[i+1]); increment count.
Sum counts.

Time complexity: O((num2 - num1 + 1) * L) where L <= 6 (log10(num2)+1). With max range ~100k and L small this is fine. Space O(L) per number (or constant extra).

Alternative: digit-DP to count peaks/valleys across entire set; more complex but not needed.

Edge cases: identical num1 and num2, numbers like 100 which have zeros in middle (digits handled fine), ensure int-to-string conversion is fine.

## Attempted solution(s)
```python
class Solution:
    def totalWaviness(self, num1: int, num2: int) -> int:
        total = 0
        for n in range(num1, num2 + 1):
            s = str(n)
            if len(s) < 3:
                continue
            # convert to digits
            digits = [ord(c) - 48 for c in s]  # slightly faster than map(int, s)
            for i in range(1, len(digits) - 1):
                if digits[i] > digits[i-1] and digits[i] > digits[i+1]:
                    total += 1
                elif digits[i] < digits[i-1] and digits[i] < digits[i+1]:
                    total += 1
        return total
```
- Notes:
  - Approach: brute-force iterate each number in the inclusive range, examine each interior digit for peak/valley.
  - Time complexity: O((num2 - num1 + 1) * L), where L is number of digits (<= 6 given constraints). With num2 - num1 <= 1e5 this is efficient.
  - Space complexity: O(L) for digit list per number (treated as constant extra space).
  - Implementation details: used ord(c)-48 to convert to int digits slightly faster than int(c)/map(int). This is optional; clarity-wise map(int, s) is fine as well.