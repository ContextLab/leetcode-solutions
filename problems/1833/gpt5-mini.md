# [Problem 1833: Maximum Ice Cream Bars](https://leetcode.com/problems/maximum-ice-cream-bars/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We want to maximize the number of bars bought given a budget. Buying cheaper bars first is optimal (greedy). Sorting costs and buying from smallest up would work. Because the problem specifically asks to use counting sort, we should build a frequency array of costs (costs[i] are integers in a bounded range) and then iterate prices from smallest to largest, buying as many as affordable at each price.

## Refining the problem, round 2 thoughts
- Use a frequency/count array indexed by price (1..max_cost). This is effectively counting sort.
- For each price p in increasing order:
  - If coins < p, we cannot buy any further (since next prices are >= p).
  - Otherwise, buy up to min(count[p], coins // p) bars at price p.
  - Subtract spent coins and add to the total count.
- Edge cases: if all costs exceed coins initially, return 0. If coins are large enough, we may buy all bars.
- Time complexity: O(n + max_cost) where max_cost = max(costs) (max_cost ≤ 1e5). Space complexity: O(max_cost) for the counts array.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxIceCream(self, costs: List[int], coins: int) -> int:
        if not costs:
            return 0

        max_cost = max(costs)
        # frequency array for counting sort
        counts = [0] * (max_cost + 1)
        for c in costs:
            counts[c] += 1

        bought = 0
        # iterate prices from smallest to largest
        for price in range(1, max_cost + 1):
            if coins < price:
                break
            if counts[price] == 0:
                continue
            # maximum number of bars at this price we can afford
            can_buy = min(counts[price], coins // price)
            if can_buy > 0:
                bought += can_buy
                coins -= can_buy * price
                # if after buying we don't have enough for this price, future prices won't be affordable
                if coins < price:
                    break

        return bought
```
- Notes:
  - Approach: Counting-sort-style frequency array and greedy purchase of cheapest bars first.
  - Time complexity: O(n + max_cost) where n = len(costs) and max_cost = max(costs) (max_cost ≤ 1e5). Building counts takes O(n) and iterating prices takes O(max_cost).
  - Space complexity: O(max_cost) for the counts array.
  - This meets the requirement to use counting sort and is efficient for the given constraints.