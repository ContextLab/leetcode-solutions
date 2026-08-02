# [Problem 877: Stone Game](https://leetcode.com/problems/stone-game/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This is a two-player perfect-information game where each turn a player takes an entire pile from one end. The naive way to think is minimax / DP: compute the best score difference alice - bob for every interval [i..j]. That would be an O(n^2) DP (or O(n^2) memoized recursion) solution.

But I recall a standard observation for this exact problem: because the number of piles is even, Alice can always force taking either all piles at even indices or all piles at odd indices (indices with respect to the initial array). Since she moves first, she can choose which parity to target and guarantee taking all piles of that parity. Therefore she can pick the parity with the larger total and win. So Alice always wins (return True). The total being odd just rules out ties, but isn't needed for the "always true" result given even count.

## Refining the problem, round 2 thoughts
- Edge cases: n is even and at least 2, so parity strategy applies. piles values are positive.
- Formal strategy: compute sum_even = sum of piles at even indices, sum_odd = sum of piles at odd indices. Alice chooses the parity with the larger sum. On her first move she picks the appropriate end so that she takes a pile of that parity. After that, whenever Bob takes a pile from one end, Alice takes from the opposite end; this maintains that Alice always takes from the same parity positions in the original array. Because n is even, the two ends are always of opposite parity at each full-turn step, which allows Alice to maintain the parity invariant.
- Alternative: implement DP computing maximum difference dp[i][j] = max(piles[i] - dp[i+1][j], piles[j] - dp[i][j-1]) and check dp[0][n-1] > 0. That is O(n^2) time and O(n^2) space (or O(n) optimized). But not necessary here.
- Complexity: using parity observation gives O(1) time and O(1) space (or simply return True since constraint guarantees even n).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def stoneGame(self, piles: List[int]) -> bool:
        # By the parity argument for even-length piles, Alice can always win.
        return True
```
- Notes:
  - Approach: Use the well-known parity strategy: Alice can choose to take all piles on either the even indices or the odd indices of the initial array, and thus she can guarantee at least the larger of the two sums. Since the array length is even, she can force this by an appropriate first move and then always taking the opposite end of whatever Bob takes.
  - Time complexity: O(1).
  - Space complexity: O(1).
  - Alternative (more general) approach: DP minimax with dp[i][j] = maximum difference current player can achieve on interval [i..j], which runs in O(n^2) time and O(n^2) space (or O(n) space with optimization).