# [Problem 1945: Sum of Digits of String After Convert](https://leetcode.com/problems/sum-of-digits-of-string-after-convert/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to convert each letter to its alphabet position and concatenate those numbers, then apply digit-sum k times. The naive way would be to build the concatenated string and repeatedly sum its digits, but that could be wasteful (though constraints are small). Observing that the sum of digits of the concatenation equals the sum of digits of each position number individually, I can compute the initial digit-sum by summing the digit sums of each letter's numeric value (1..26) without forming the big string. Then apply the "sum digits" operation k times (the first application is the one after conversion). Since the initial total after conversion is at most 100 * (2+6) = 800, the repeated sums are cheap.

## Refining the problem, round 2 thoughts
Refine: compute initial_sum = sum(digit_sum(ord(ch)-96) for ch in s). That is the result after the first transform. If k == 1 return initial_sum. Otherwise apply the digit-sum operation (k-1) more times on the integer value. Edge cases: letters like 'j' -> "10" include zero digits, but digit-sum handles that naturally. Complexity: O(n + k * log M) where M is the value magnitude (small here). Space O(1). No need to construct the concatenated string.

## Attempted solution(s)
```python
class Solution:
    def getLucky(self, s: str, k: int) -> int:
        # helper to sum digits of an integer
        def sum_digits(num: int) -> int:
            total = 0
            while num > 0:
                total += num % 10
                num //= 10
            return total

        # initial sum after converting letters to their positions and summing digits
        initial = 0
        for ch in s:
            val = ord(ch) - ord('a') + 1
            # add digits of val (val is between 1 and 26)
            if val >= 10:
                initial += val // 10 + val % 10
            else:
                initial += val

        # first transform has been applied (conversion -> concatenation -> sum digits)
        current = initial
        # apply remaining k-1 transforms
        for _ in range(k - 1):
            current = sum_digits(current)

        return current
```
- Notes:
  - Approach: avoid building the concatenated string; sum digits per-letter to get the same result as summing digits of the concatenation. Then iteratively apply digit-sum (k-1) more times.
  - Time complexity: O(n + k * log M) where n = len(s) and M is the (small) magnitude of current (practically O(n + k)). With constraints (n ≤ 100, k ≤ 10) this is effectively linear and very fast.
  - Space complexity: O(1) extra space (ignoring output).