# [Problem 1523: Count Odd Numbers in an Interval Range](https://leetcode.com/problems/count-odd-numbers-in-an-interval-range/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count how many odd integers lie between low and high inclusive. Brute force would check each number's parity but that's unnecessary for potentially large ranges (up to 1e9). There should be a constant-time arithmetic formula using parity/count properties. Observations: number of odd numbers up to n is something like roughly half of n, adjusted by whether n is odd. Use that to get count in [low, high] by subtracting counts up to boundaries.

## Refining the problem, round 2 thoughts
Define odds_up_to(n) = count of odd numbers in [0, n]. For n >= 0, odds_up_to(n) = (n + 1) // 2. Then count in [low, high] = odds_up_to(high) - odds_up_to(low - 1). Simplify algebraically to (high + 1)//2 - low//2 (since odds_up_to(low-1) = low//2). Edge cases: low == high, low or high = 0 — formula still holds. This is O(1) time and O(1) space and avoids loops.

## Attempted solution(s)
```python
class Solution:
    def countOdds(self, low: int, high: int) -> int:
        # Count of odd numbers from 0..n is (n+1)//2
        # So count in [low, high] = odds_up_to(high) - odds_up_to(low-1)
        # odds_up_to(high) = (high+1)//2
        # odds_up_to(low-1) = low//2
        return (high + 1) // 2 - (low // 2)
```
- Approach: Use arithmetic parity/count formula. Derivation: odds_up_to(n) = floor((n+1)/2). Subtract counts to get inclusive interval count.
- Time complexity: O(1).
- Space complexity: O(1).
- Notes: Works for all given constraints (0 <= low <= high <= 1e9).