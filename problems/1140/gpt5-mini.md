# [Problem 1140: Stone Game II](https://leetcode.com/problems/stone-game-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the maximum stones Alice can get when both play optimally. The game state is determined by the index of the first remaining pile and the current M. On a turn the player can take X piles where 1 <= X <= 2M, and then M becomes max(M, X). This suggests a dynamic programming or minimax with memoization over (i, M) states.

A common trick: if we know the total stones remaining from i to end (suffix sum), and we can compute the best the opponent can obtain from (i + X, max(M, X)), then the current player's best is suffix_sum[i] - opponent_best. So dp(i, M) = max_{1<=X<=2M} (suffix[i] - dp(i+X, max(M, X))). That reduces the need to explicitly sum taken piles each time.

We need to be careful to cap X at the number of remaining piles. n up to 100, so states are O(n^2) (i up to n, M up to n), transitions up to O(n), total ~O(n^3) which is OK.

## Refining the problem, round 2 thoughts
- Precompute suffix sums so we can get remaining total quickly.
- Use recursion + memoization (lru_cache) or bottom-up DP table. Recursion with memo is simpler to write.
- Base case: if i >= n, dp = 0.
- For each state (i, M) try X from 1 to min(2*M, n-i) and compute opponent's best.
- Return dp(0, 1).
- Complexity: states ~ n * n, each state iterates up to 2M but M <= n, so worst-case transitions ~ n => O(n^3) time, O(n^2) memory for memo plus O(n) for suffix array.

Edge cases:
- Very small arrays (n=1) should return piles[0].
- Large piles values don't affect algorithm beyond sums.

## Attempted solution(s)
```python
from functools import lru_cache
from typing import List

class Solution:
    def stoneGameII(self, piles: List[int]) -> int:
        n = len(piles)
        # suffix[i] = total stones from piles[i] to end
        suffix = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            suffix[i] = suffix[i + 1] + piles[i]

        @lru_cache(None)
        def dp(i: int, m: int) -> int:
            if i >= n:
                return 0
            # If the current player can take all remaining piles, take them
            # but the general formula below also handles it.
            best = 0
            max_take = min(2 * m, n - i)
            for x in range(1, max_take + 1):
                next_i = i + x
                next_m = max(m, x)
                # opponent_best is what the opponent will get from remaining
                opponent_best = dp(next_i, next_m)
                # current gets remaining total minus what opponent gets
                current = suffix[i] - opponent_best
                if current > best:
                    best = current
            return best

        return dp(0, 1)
```
- Notes:
  - We use dp(i, m) = maximum stones current player can obtain from piles[i:] given M = m.
  - Using suffix sums allows computing the current player's gain as suffix[i] - dp(i+x, max(m, x)) because the opponent will play optimally on the remainder.
  - Time complexity: O(n^3) in the worst case (O(n^2) states, each examines up to O(n) choices).
  - Space complexity: O(n^2) for memoization plus O(n) for the suffix array and recursion stack.