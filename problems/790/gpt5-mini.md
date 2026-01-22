# [Problem 790: Domino and Tromino Tiling](https://leetcode.com/problems/domino-and-tromino-tiling/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This is a tiling DP. For a 2 x n board we can place vertical dominoes, pairs of horizontal dominoes, or tromino shapes (L-shaped) that create "overhangs" or "gaps" when considered column-by-column. A straightforward 1D DP that only counts fully-tiled boards is tricky because tromino placements can leave a column partially filled; so we need to track extra states (incomplete column states) in addition to the fully-tiled count. I recall there is a standard approach with two sequences: one for fully tiled 2 x i boards and one for boards with a single-square overhang (two symmetric orientations). Derive recurrences carefully and use modulo 1e9+7.

## Refining the problem, round 2 thoughts
Define:
- dp[i] = number of ways to fully tile 2 x i.
- side[i] = number of ways to tile a 2 x i board leaving exactly one extra cell sticking out at column i (i.e., an L-shaped partial covering). side counts both top- and bottom-overhang orientations combined.

Recurrences:
- side[i] = side[i-1] + dp[i-1]
  (You can extend a previous overhang by one column with a domino, or create a new overhang by placing a tromino after a fully tiled prefix.)
- dp[i] = dp[i-1] + dp[i-2] + 2 * side[i-1]
  (dp[i-1]: add vertical dominoes at end; dp[i-2]: add two horizontal dominoes; 2*side[i-1]: close the overhangs in two orientations or place tromino pairs.)

Base cases:
- dp[0] = 1 (empty board), dp[1] = 1
- side[0] = 0, side[1] = 0

We can iterate i = 2..n building dp and side using O(1) extra space. Handle n=1 explicit. Use modulo 10^9+7. Time O(n), space O(1). Edge cases: n=1 (answer 1), small n validated by examples (n=2 => 2, n=3 => 5).

## Attempted solution(s)
```python
class Solution:
    def numTilings(self, n: int) -> int:
        MOD = 10**9 + 7
        if n == 1:
            return 1
        
        # dp_prev2 = dp[i-2], dp_prev1 = dp[i-1]
        dp_prev2 = 1  # dp[0]
        dp_prev1 = 1  # dp[1]
        side_prev = 0  # side[1] (also side[0] = 0)
        
        for i in range(2, n + 1):
            # compute side[i] = side[i-1] + dp[i-1]
            side_i = (side_prev + dp_prev1) % MOD
            # compute dp[i] = dp[i-1] + dp[i-2] + 2 * side[i-1]
            dp_i = (dp_prev1 + dp_prev2 + 2 * side_prev) % MOD
            
            # shift for next iteration
            dp_prev2, dp_prev1, side_prev = dp_prev1, dp_i, side_i
        
        return dp_prev1 % MOD
```
- Notes:
  - Approach: dynamic programming with two sequences: dp (fully tiled) and side (one-cell overhang). The recurrence is derived by considering how new tiles can extend or close existing configurations.
  - Time complexity: O(n) — single loop from 2 to n.
  - Space complexity: O(1) — constant extra space (we only store a few integers).
  - Uses modulo 10^9+7 at each step to avoid overflow.