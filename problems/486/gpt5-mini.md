# [Problem 486: Predict the Winner](https://leetcode.com/problems/predict-the-winner/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I see a two-player turn-based game where each player picks either the leftmost or rightmost element. Both play optimally. This screams minimax / dynamic programming. One approach is to simulate choices and minimize the opponent's future advantage. Because n <= 20, exponential recursion with memoization is possible, but there's a classic DP that computes the maximum score difference a current player can obtain over the other from any subarray [i..j]. If the difference for the whole array is >= 0, player 1 can ensure a win or tie.

A typical relation: if you pick nums[i], your net advantage becomes nums[i] - (best advantage the opponent can get on [i+1..j]). Similarly for nums[j]. So dp[i][j] = max(nums[i] - dp[i+1][j], nums[j] - dp[i][j-1]). Base case dp[i][i] = nums[i]. Finally check dp[0][n-1] >= 0.

Edge cases: single element (true), ties count as win (>= 0). Time complexity should be O(n^2).

## Refining the problem, round 2 thoughts
- Confirming tie counts as a win: use >= 0 condition.
- Consider memory: n <= 20, so O(n^2) dp is trivial. Could also optimize to O(n) space using rolling 1D dp, but 2D is clear and easy to reason about.
- Alternative: direct minimax with memoization that returns (best score current player can achieve) but computing difference is simpler and avoids carrying two scores.
- Complexity: compute dp for all i<=j, that's about n(n+1)/2 entries so O(n^2) time and O(n^2) space. If needed, reduce to O(n) space by processing lengths and updating a 1D dp array from right to left.
- Implementation detail: use integers (nums up to 1e7, but differences fit in Python int).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def PredictTheWinner(self, nums: List[int]) -> bool:
        n = len(nums)
        if n == 1:
            return True

        # dp[i][j] = maximum net score current player can achieve over opponent for subarray nums[i..j]
        dp = [[0] * n for _ in range(n)]

        # base case: single element
        for i in range(n):
            dp[i][i] = nums[i]

        # consider all lengths from 2 to n
        for length in range(2, n + 1):
            for i in range(0, n - length + 1):
                j = i + length - 1
                pick_left = nums[i] - dp[i + 1][j]   # if pick nums[i], opponent's best on [i+1..j] is dp[i+1][j]
                pick_right = nums[j] - dp[i][j - 1]  # if pick nums[j], opponent's best on [i..j-1] is dp[i][j-1]
                dp[i][j] = max(pick_left, pick_right)

        # If net advantage for player 1 on whole array is >= 0, player 1 can win (or tie)
        return dp[0][n - 1] >= 0
```
- Notes:
  - Approach: dynamic programming on intervals computing the maximum net advantage (score difference) current player can force for any subarray.
  - Correctness: dp relation derives from optimal play—when you pick an end, the opponent then becomes the "current player" on the remaining subarray, and dp for that subarray is their net advantage; subtracting that gives your net advantage for this choice.
  - Time complexity: O(n^2) because we fill about n(n+1)/2 dp states and each state is computed in O(1).
  - Space complexity: O(n^2) for the dp table. This can be reduced to O(n) using a 1D dp optimization by iterating appropriately, but O(n^2) is fine for n <= 20.
  - Edge cases: n == 1 handled directly; ties count as win, so return dp[0][n-1] >= 0.