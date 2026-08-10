# [Problem 1510: Stone Game IV](https://leetcode.com/problems/stone-game-iv/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This is a two-player impartial game where each move removes a perfect square number of stones. With both players optimal, we can think in terms of winning/losing positions: a position (number of stones) is winning if there exists a legal move to a losing position for the opponent. A straightforward approach is dynamic programming (or recursive memoization): compute for each pile size i whether it's winning by checking all square moves j*j <= i and seeing if any move leads to a losing position i - j*j. Constraints n ≤ 1e5 make an O(n * sqrt(n)) DP feasible. No need for advanced theory (Sprague-Grundy) here because moves are simple and decision is binary.

## Refining the problem, round 2 thoughts
Refine into an iterative DP: dp[0] = False (no stones => current player loses), for i from 1..n compute dp[i] = True if exists square s where dp[i - s] is False. Precompute squares up to n to avoid repeated sqrt computations. Edge case: n = 1 should return True because removing 1 wins immediately. Time complexity: O(n * sqrt(n)) because for each i we iterate squares up to sqrt(i). Space complexity: O(n) for the dp array. Alternative: top-down recursion with memoization yields similar complexity; bitset optimizations possible but unnecessary for n ≤ 1e5.

## Attempted solution(s)
```python
class Solution:
    def winnerSquareGame(self, n: int) -> bool:
        # dp[i] = True if the player whose turn it is with i stones can force a win
        dp = [False] * (n + 1)
        # Precompute perfect squares up to n
        squares = []
        k = 1
        while k * k <= n:
            squares.append(k * k)
            k += 1

        for i in range(1, n + 1):
            # If there exists a square move that leads to a losing position for opponent,
            # then current position i is winning.
            win = False
            for s in squares:
                if s > i:
                    break
                if not dp[i - s]:
                    win = True
                    break
            dp[i] = win

        return dp[n]
```
- Notes:
  - Approach: bottom-up dynamic programming deciding winning/losing positions by checking square removals.
  - Time complexity: O(n * sqrt(n)) — for each i (1..n) test up to O(sqrt(n)) squares.
  - Space complexity: O(n) for dp plus O(sqrt(n)) for the squares list.
  - Implementation details: precomputing squares avoids repeated sqrt calls and keeps inner loop simple. dp[0] = False is the base case (no moves => lose).