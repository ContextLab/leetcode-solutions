# [Problem 2561: Rearranging Fruits](https://leetcode.com/problems/rearranging-fruits/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to make the multisets of values in the two baskets identical by cross-swapping items; each swap cost is min(basket1[i], basket2[j]). Think in terms of counts of each value rather than positions. If the total count of any value across both baskets is odd, it's impossible because final equal multisets require each value to appear an even total number (half in each). For values with an imbalance (more in basket1 than basket2), we must move some occurrences from basket1 to basket2, and vice versa.

We can collect the surplus items in each basket (values that must be moved). Each swap fixes two surplus items (one from basket1 and one from basket2). To minimize cost, pair cheap items with expensive ones carefully. A known trick: either swap the pair directly costing min(a,b) or perform two swaps via the overall smallest value in both arrays (cost 2 * global_min). For a pair (a,b), the minimum cost to fix them is min(min(a, b), 2 * global_min).

So produce lists of surplus items (each repeated by half the difference), sort them, and pair smallest surpluses in basket1 with largest in basket2 (or equivalently pair sorted ascending with sorted descending) and sum the per-pair minimal costs.

## Refining the problem, round 2 thoughts
- Use Counter to count frequencies in both arrays.
- For each value v, if (cnt1[v] + cnt2[v]) % 2 == 1 -> impossible, return -1.
- Let diff = cnt1[v] - cnt2[v]. If diff > 0 then we need diff//2 copies of v to move from basket1 to basket2 (add to list A). If diff < 0, add (-diff)//2 copies to list B.
- After building A and B, lengths must match (they will, since each pair fixes two surplus occurrences).
- Sort A ascending and B ascending, then pair A[i] with B[len-1-i] (or sort B descending and pair same indices). For each pair (a,b) cost += min(min(a,b), 2*global_min).
- Complexity: counting O(n), building surplus lists O(n), sorting O(k log k) where k <= n, so overall O(n log n) time and O(n) space.
- Edge cases: already equal (cost 0), empty surplus lists, very large values handled fine.

## Attempted solution(s)
```python
from collections import Counter
from typing import List

class Solution:
    def minCost(self, basket1: List[int], basket2: List[int]) -> int:
        n = len(basket1)
        cnt1 = Counter(basket1)
        cnt2 = Counter(basket2)

        # global minimum value across both baskets
        global_min = min(min(basket1), min(basket2))

        need1 = []  # values to move out of basket1
        need2 = []  # values to move out of basket2

        # Check feasibility and build surplus lists
        all_keys = set(cnt1.keys()) | set(cnt2.keys())
        for v in all_keys:
            total = cnt1.get(v, 0) + cnt2.get(v, 0)
            if total % 2 == 1:
                return -1  # impossible
            diff = cnt1.get(v, 0) - cnt2.get(v, 0)
            if diff > 0:
                times = diff // 2
                need1.extend([v] * times)
            elif diff < 0:
                times = (-diff) // 2
                need2.extend([v] * times)

        if not need1 and not need2:
            return 0

        # They must have equal length
        if len(need1) != len(need2):
            return -1  # defensive, though it shouldn't happen

        need1.sort()
        need2.sort(reverse=True)  # pair smallest from need1 with largest from need2

        total_cost = 0
        two_min = 2 * global_min
        for a, b in zip(need1, need2):
            total_cost += min(min(a, b), two_min)

        return total_cost
```
- Notes:
  - We operate on frequencies, not positions. For each value, the number of occurrences that must be moved is half the difference between counts.
  - Pairing strategy: sorting one ascending and the other descending ensures we try to match small values with large values where direct swap cost may be low; but even if not, using the global minimum twice (2*global_min) can be cheaper than direct swap.
  - Time complexity: O(n log n) because of sorting (n = basket length). Space complexity: O(n) for counters and surplus lists.
  - The solution handles impossible cases by checking odd total counts for any value.