# [Problem 1317: Convert Integer to the Sum of Two No-Zero Integers](https://leetcode.com/problems/convert-integer-to-the-sum-of-two-no-zero-integers/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need two positive integers a and b such that a + b = n and neither contains the digit '0'. The constraints are small (n up to 10^4), so a simple search over possible splits is feasible. For each candidate a from 1 to n-1, check if both a and n-a have any zero digit. If not, return them. A helper to test "no zero digit" is straightforward (string check or arithmetic digit check). There's guaranteed to be at least one solution, so the search will succeed.

## Refining the problem, round 2 thoughts
Brute force is simple and efficient enough here: at worst we check ~10^4 values and for each we examine at most 5 digits (since 10^4 has 5 digits), so it's trivial time. Edge cases: n small like 2 (1+1) should work. Implementation detail: avoid converting to string if prefer digit arithmetic, but string check '0' not in str(x) is concise and fast enough. Complexity: O(n * d) where d is number of digits (~log10 n). Space O(1) besides output.

## Attempted solution(s)
```python
class Solution:
    def getNoZeroIntegers(self, n: int) -> [int, int]:
        def no_zero(x: int) -> bool:
            # Check digits without converting to string
            while x > 0:
                if x % 10 == 0:
                    return False
                x //= 10
            return True

        for a in range(1, n):
            b = n - a
            if no_zero(a) and no_zero(b):
                return [a, b]
        # Problem guarantees a solution exists, but return a default to satisfy function signature
        return [1, n-1]
```
- Notes:
  - Approach: brute-force check each split a + b = n and test both numbers for presence of digit 0 using digit arithmetic.
  - Time complexity: O(n * d) where d = number of digits in n (d = O(log10 n)). With n <= 10^4 this is effectively O(n).
  - Space complexity: O(1) extra space (output not counted).
  - This is simple, readable, and efficient enough for given constraints.