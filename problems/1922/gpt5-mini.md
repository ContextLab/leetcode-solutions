# [Problem 1922: Count Good Numbers](https://leetcode.com/problems/count-good-numbers/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count digit strings of length n where even indices (0-based) must be even digits and odd indices must be prime digits (2,3,5,7). Leading zeros allowed, so positions are independent choices. For each even index there are 5 choices (0,2,4,6,8). For each odd index there are 4 choices (2,3,5,7). So total count should be 5^(#even_positions) * 4^(#odd_positions). n can be huge (up to 1e15), so I need fast modular exponentiation; Python's built-in pow(base, exp, mod) works. Multiply results modulo 1e9+7.

## Refining the problem, round 2 thoughts
Compute counts: even_positions = (n + 1) // 2 (indices 0,2,4,...), odd_positions = n // 2. Use mod = 10**9 + 7. Answer = (5^even_positions mod MOD) * (4^odd_positions mod MOD) mod MOD. Complexity: pow with modular exponentiation is O(log exp) time, which is fine for 1e15. Space O(1). Edge cases: n=1 -> even_positions=1, odd_positions=0 -> 5. n large handled by pow. No other corner cases since digits independent and leading zeros allowed.

## Attempted solution(s)
```python
class Solution:
    def countGoodNumbers(self, n: int) -> int:
        MOD = 10**9 + 7
        even_positions = (n + 1) // 2  # indices 0,2,4,...
        odd_positions = n // 2         # indices 1,3,5,...
        return (pow(5, even_positions, MOD) * pow(4, odd_positions, MOD)) % MOD
```
- Notes:
  - Approach: Count independent choices per position and use modular exponentiation to compute powers for large n.
  - Time complexity: O(log n) due to modular exponentiation.
  - Space complexity: O(1).