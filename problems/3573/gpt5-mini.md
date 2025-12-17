# [Problem 3573: Best Time to Buy and Sell Stock V](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-v/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We can do at most k transactions. A transaction can be a normal buy-then-sell or a short-sell (sell then buy back). For any pair of days i < j the profit from a transaction between i and j is |prices[j] - prices[i]| (we would only take the positive direction). Transactions must be non-overlapping and cannot start on the same day the previous transaction ended (so if previous ended on day j, next must start at day > j).

This looks like a dynamic programming problem similar to the classic "at most k transactions" stock problems (LeetCode 188). The naive DP dp[t][i] = max(dp[t][i-1], max_{s < i} dp[t-1][s] + |p[i]-p[s]|) is O(k * n^2) which is too slow for n up to 1000 and k up to ~500. For the standard problem without short-selling we optimize by tracking a running "best" value of dp[t-1][s-1] - price[s]. Here, the absolute value splits into two linear terms depending on sign: p[i]-p[s] or p[s]-p[i], so we can similarly maintain two running maxima to get O(k*n).

Need to be careful about the "cannot start on same day previous ended" constraint: when adding a transaction that starts at s and ends at i, we must use dp[t-1][s-1] (profit up to day s-1) — not dp[t-1][s] — to avoid allowing immediate reuse of day s.

So split the absolute into two cases and maintain:
- best1 = max over s in [0..i-1] of dp_prev[s-1] - p[s]  (handles p[i] + best1)
- best2 = max over s in [0..i-1] of dp_prev[s-1] + p[s]  (handles -p[i] + best2)

Then dp_cur[i] = max(dp_cur[i-1], p[i] + best1, -p[i] + best2). Update best1/best2 after computing dp_cur[i] using dp_prev[i-1] (dp_prev[-1] = 0 for s = 0).

## Refining the problem, round 2 thoughts
- We must ensure indices are handled so that transactions don't start on the same day a previous transaction ended: use dp_prev[s-1] in the expressions (with dp_prev[-1] = 0).
- Base cases: dp[0][*] = 0; dp[*][0] = 0 (no profit with zero days or zero transactions).
- Time complexity O(k * n) and space O(n) if we keep only previous and current dp rows.
- Edge cases: small n (2), k up to n//2 per constraints; prices large but only used in additions/subtractions so Python int fine.

This yields a correct and efficient algorithm.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxProfit(self, k: int, prices: List[int]) -> int:
        n = len(prices)
        if n < 2 or k == 0:
            return 0

        # If k is large enough we could capture every adjacent absolute diff by using
        # transactions on every adjacent pair, but constraints guarantee k <= n//2.
        # We'll use O(k * n) DP.

        # dp_prev[i] = max profit using at most (t-1) transactions up to and including day i
        dp_prev = [0] * n

        for _ in range(1, k + 1):
            dp_cur = [0] * n
            # best1 = max(dp_prev[s-1] - prices[s]) for s in [0..i-1]
            # best2 = max(dp_prev[s-1] + prices[s]) for s in [0..i-1]
            # initialize as -inf so that if no s exists (i=0) we don't use them
            best1 = float("-inf")
            best2 = float("-inf")

            for i in range(n):
                # carry forward the best without using a transaction ending at i
                if i > 0:
                    dp_cur[i] = dp_cur[i - 1]
                else:
                    dp_cur[i] = 0

                # use a transaction that ends at i and starts at some s in [0..i-1]
                if best1 != float("-inf"):
                    dp_cur[i] = max(dp_cur[i], prices[i] + best1)
                if best2 != float("-inf"):
                    dp_cur[i] = max(dp_cur[i], -prices[i] + best2)

                # now allow future i' > i to consider starting at s = i:
                prev_val = dp_prev[i - 1] if i - 1 >= 0 else 0
                best1 = max(best1, prev_val - prices[i])
                best2 = max(best2, prev_val + prices[i])

            dp_prev = dp_cur

        return dp_prev[-1]
```
- Approach notes:
  - We use dp over number of transactions. For iteration t we build dp_cur from dp_prev = dp for t-1 transactions.
  - For a transaction that starts at s and ends at i (s < i), the gain is |prices[i] - prices[s]| plus dp_prev[s-1] (profit before s). Splitting abs into two linear forms yields two running maxima that let us compute the inner max in O(1) per i.
- Time complexity: O(k * n) where n = len(prices).
- Space complexity: O(n) (we keep two arrays of length n, dp_prev and dp_cur).