# [Problem 3652: Best Time to Buy and Sell Stock using Strategy](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-using-strategy/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We are given prices and a strategy array where strategy[i] ∈ {-1,0,1} and profit = sum(strategy[i] * prices[i]). We may modify exactly one contiguous k-length subarray by setting its first k/2 entries to 0 and last k/2 entries to 1. We want the maximum profit after at most one such modification.

Brute force would try every possible window and compute the new profit by replacing values — that's O(n*k) which is too slow (n up to 1e5). Need an O(n) or O(n log n) approach.

For a window [l, l+k-1], the profit change (delta) equals sum over first half (new - old) + sum over second half (new - old). For first half new is 0 so contribution is -strategy[i]*price[i]. For second half new is 1 so contribution is (1 - strategy[i])*price[i]. So delta = sum_first(-s*p) + sum_second((1-s)*p). That looks like two separate sums per window, but there may be a simplification.

## Refining the problem, round 2 thoughts
Compute arrays:
- A[i] = -strategy[i] * prices[i] (contribution when i falls in the first half of the modified window)
- B[i] = (1 - strategy[i]) * prices[i] (contribution when i falls in the second half)

Observe B[i] - A[i] = (1 - s)p - (-s p) = p, i.e., B = A + p. So for a window:
delta = sum_{i=l}^{l+k-1} A[i] + sum_{i=l+m}^{l+k-1} p[i], where m = k/2.
Thus delta = sumA(window) + sumP(second_half_of_window).

We can compute prefix sums for A and for prices p. Then for each l we compute:
S_A = prefA[l+k] - prefA[l]
S_P_second = prefP[l+k] - prefP[l+m]
delta = S_A + S_P_second

Compute baseProfit = sum(strategy[i]*prices[i]). The best profit is baseProfit + max(0, max_delta_over_windows). Complexity O(n) time and O(n) extra for prefix arrays (or O(1) extra if we compute sliding sums on the fly).

Edge cases:
- No modification may be beneficial (we take max with 0).
- k can be equal to n; sliding still works.
- All integers fit in Python ints.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxProfit(self, prices: List[int], strategy: List[int], k: int) -> int:
        n = len(prices)
        m = k // 2

        # base profit without any modification
        base_profit = 0
        for s, p in zip(strategy, prices):
            base_profit += s * p

        # prefix sums for A[i] = -strategy[i] * prices[i] and for prices
        prefA = [0] * (n + 1)
        prefP = [0] * (n + 1)
        for i in range(n):
            prefA[i+1] = prefA[i] + (-strategy[i]) * prices[i]
            prefP[i+1] = prefP[i] + prices[i]

        max_delta = 0  # we can choose not to modify, so delta >= 0

        # iterate over all windows of length k
        for l in range(0, n - k + 1):
            r = l + k
            sumA = prefA[r] - prefA[l]
            sumP_second = prefP[r] - prefP[l + m]
            delta = sumA + sumP_second
            if delta > max_delta:
                max_delta = delta

        return base_profit + max_delta
```
- Notes:
  - We derived a simplification B = A + p which led to delta = sumA(window) + sumP(second_half). This allows O(1) computation per window using prefix sums.
  - Time complexity: O(n) to build prefix sums and O(n) to sweep all windows => O(n) overall.
  - Space complexity: O(n) for two prefix arrays (can be reduced to O(1) by maintaining running window sums, but O(n) is simple and well within limits for n ≤ 1e5).
  - We return base_profit + max(0, best_delta) — in the code max_delta initialized to 0 ensures we never decrease profit by applying the modification.