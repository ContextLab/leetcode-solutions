# [Problem 2843:   Count Symmetric Integers](https://leetcode.com/problems/count-symmetric-integers/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to count integers in [low, high] whose digit count is even (2*n digits) and the sum of the first n digits equals the sum of the last n digits. The constraints are small (high ≤ 10^4), so a direct check per number is fine. First idea: convert each number to string, if length is even split into two halves and compare digit sums. That is straightforward and easy to implement. There's also an alternative: generate symmetric numbers by enumerating possible halves and matching sums, but that's unnecessary given the small input size.

## Refining the problem, round 2 thoughts
Edge cases:
- Numbers with odd number of digits must be ignored.
- Leading zeros are not present in the integer representation, so we just use the usual decimal representation.
- Range boundaries are inclusive.
Given high ≤ 10^4, maximum digit length is 5, so the only even lengths possible are 2 and 4 (and 0 but irrelevant). Complexity for checking each number is negligible.

Alternative solutions:
- Brute-force check each number in the interval (O(N * d) where d ≤ 5).
- Or generate all even-length numbers up to high by choosing halves and matching sums — slightly more clever but unnecessary here.

Time complexity is dominated by iterating the interval; space complexity is O(1) aside from loop variables and digit-string conversion.

## Attempted solution(s)
```python
class Solution:
    def countSymmetricIntegers(self, low: int, high: int) -> int:
        count = 0
        for x in range(low, high + 1):
            s = str(x)
            if len(s) % 2 == 1:
                continue
            n = len(s) // 2
            if sum(map(int, s[:n])) == sum(map(int, s[n:])):
                count += 1
        return count
```
- Notes:
  - Approach: brute-force iterate every integer in [low, high], skip odd-length numbers, compare sums of the two equal-length halves for even-length numbers.
  - Time complexity: O((high - low + 1) * d) where d is number of digits (d ≤ 5 here), so effectively O(N) for N = high-low+1.
  - Space complexity: O(1) extra space (ignoring the small temporary strings/iterators used for digit processing).