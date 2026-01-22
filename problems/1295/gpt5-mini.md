# [Problem 1295: Find Numbers with Even Number of Digits](https://leetcode.com/problems/find-numbers-with-even-number-of-digits/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count how many integers in the array have an even number of digits. First thought: convert each integer to a string and check if len(str(num)) is even — very straightforward and easy to implement. Another idea: use math (log10) to get digit count without string conversion, e.g. int(log10(num)) + 1, but watch out for exact powers of 10 (log precision). Given constraints (nums[i] >= 1 and <= 10^5), the maximum number of digits is small (up to 6), so converting to string is cheap. Could also use digit-range thresholds (10, 100, 1000, ...) to check counts in constant time per number.

## Refining the problem, round 2 thoughts
The input size is at most 500, numbers are positive and bounded, so any reasonable solution is fine. Edge cases: single-element arrays, very small numbers (1-digit), and the maximum value 100000 (6 digits). Using str() is simple and robust; using math.log10 needs to handle floating-point precision but is still workable. A threshold-based approach (if 10 <= n < 100, etc.) is also clean and uses integer comparisons only.

Time complexity should be O(n * d) where d is digits per number; with d <= 6 this is effectively O(n). Space complexity can be O(1) auxiliary (ignoring input and small temporaries). I'll implement the simple and readable string-based solution.

## Attempted solution(s)
```python
class Solution:
    def findNumbers(self, nums: list[int]) -> int:
        """
        Count how many numbers in nums have an even number of digits.
        Simple approach: convert each number to string and check length parity.
        """
        return sum(1 for x in nums if len(str(x)) % 2 == 0)
```
- Notes:
  - Approach: Convert each integer to a string and check if the length is even; count those that are.
  - Time complexity: O(n * d) where n = len(nums) and d is average number of digits. Given constraints d <= 6, this is effectively O(n).
  - Space complexity: O(1) extra space (excluding input and short temporary strings). An alternative constant-time per-number approach is to check ranges:
    - 2 digits: 10 <= n <= 99
    - 4 digits: 1000 <= n <= 9999
    - 6 digits: 100000 (if present)
    This avoids string conversion but is more verbose. The string approach is clear and efficient for the given constraints.