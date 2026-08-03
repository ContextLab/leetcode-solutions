# [Problem 1406: Stone Game III](https://leetcode.com/problems/stone-game-iii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This is a two-player turn-based game where each player takes 1-3 stones from the front, and each stone has a (possibly negative) value. Both play optimally. This screams dynamic programming / minimax. A common trick for zero-sum games with optimal play is to think in terms of score difference: from a given position, what is the maximum difference (current_player_score - opponent_score) the current player can force?

If we know for every suffix starting at index i the best difference the current player can force, dp[i], then when the player takes k stones (k in {1,2,3}), the immediate gain is sum(stoneValue[i:i+k]) and the opponent will then be able to force dp[i+k] (which is their advantage from that suffix). So the net advantage for taking k stones is immediate_sum - dp[i+k]. We take the maximum over k.

Base: dp[n] = 0 (no stones left). Iterate backwards to compute dp[0]. Compare dp[0] to 0 to decide Alice/Tie/Bob.

Need to be careful with boundaries and negative stone values.

## Refining the problem, round 2 thoughts
- Implementation details: compute dp array of length n+1 initialized to very small values except dp[n]=0. For each i from n-1 down to 0, accumulate take sum for up to three stones and compute candidate = take_sum - dp[i + k]. Keep max.
- Complexity: O(n) time (each index does up to 3 operations), O(n) space for dp. We can reduce space to O(1) or O(3) using rolling storage but O(n) is simple and fine for n up to 5e4.
- Edge cases: n < 3 handled naturally by bounds checks; negative values handled because we use sums that can be negative. Make sure to access dp[i+k] safely (i+k may equal n).
- Alternative: top-down memoization or using suffix sums then dp[i] = max(total_suffix_i - dp[i+k]?) — but the immediate-sum - dp[i+k] approach is simpler.
- After computing dp[0], if dp[0] > 0 => "Alice", dp[0] == 0 => "Tie", else => "Bob".

## Attempted solution(s)
```python
from typing import List

class Solution:
    def stoneGameIII(self, stoneValue: List[int]) -> str:
        n = len(stoneValue)
        # dp[i] = max score difference (current player - opponent) starting from index i
        dp = [float('-inf')] * (n + 1)
        dp[n] = 0
        
        for i in range(n - 1, -1, -1):
            take_sum = 0
            # try taking 1, 2 or 3 stones
            for k in range(1, 4):
                if i + k - 1 >= n:
                    break
                take_sum += stoneValue[i + k - 1]
                # opponent's advantage after taking k stones is dp[i + k]
                candidate = take_sum - dp[i + k]
                if candidate > dp[i]:
                    dp[i] = candidate
        
        if dp[0] > 0:
            return "Alice"
        elif dp[0] == 0:
            return "Tie"
        else:
            return "Bob"
```
- Approach: Bottom-up dynamic programming computing the maximum score difference the current player can force from each index. For each i we consider taking 1..3 stones, compute immediate sum and subtract opponent's best response dp[i+k].
- Time complexity: O(n) — each i considers up to 3 options.
- Space complexity: O(n) for the dp array (can be reduced to O(1)/O(3) with rolling variables if desired).
- Important detail: dp[i] represents (current player score - opponent score) from suffix i; dp[n] = 0 as base. Comparing dp[0] to zero yields the final result "Alice"/"Bob"/"Tie".