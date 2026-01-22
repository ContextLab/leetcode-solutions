# [Problem 2070: Most Beautiful Item for Each Query](https://leetcode.com/problems/most-beautiful-item-for-each-query/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need, for each query value Q, the maximum beauty among items with price <= Q. This is a classic "queries about prefix of sorted data" problem. My first thought: sort items by price, then for each query, consider all items with price <= query and take the maximum beauty. Doing that naively per query would be O(n*m) which is too slow.

A typical pattern: sort items by price, sort queries (but keep original indices), then sweep through items while advancing pointer as query thresholds increase, maintaining the maximum beauty seen so far. That yields O((n + m) log n) only for the sorts — actually O(n log n + m log m) overall for sorting and O(n + m) for the sweep. There's no need for a segment tree or binary indexed tree since we only need the global max beauty for prefix by price.

Also note that prices and queries can be as large as 1e9 but we only care about relative ordering, so sorting works fine.

## Refining the problem, round 2 thoughts
Edge cases:
- No item has price <= query — should return 0.
- Multiple items can have the same price; when sweeping we should consider all of them and update the max beauty accordingly.
- Items and queries sizes up to 1e5 — sorting is acceptable.
Alternative approaches: coordinate compression + prefix max array if we wanted to query arbitrary prices with binary search; but the two-sort sweep is simpler and optimal enough.

Complexity:
- Time: O(n log n + m log m) for sorting items and queries, plus O(n + m) for the single sweep.
- Space: O(n + m) for storing sorted structures and the result array (in-place sorts aside).

This is straightforward to implement and robust.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maximumBeauty(self, items: List[List[int]], queries: List[int]) -> List[int]:
        # Sort items by price
        items.sort(key=lambda x: x[0])
        
        # Keep original indices of queries so we can restore order after sorting
        sorted_queries = sorted([(q, i) for i, q in enumerate(queries)], key=lambda x: x[0])
        
        res = [0] * len(queries)
        max_beauty = 0
        idx = 0  # pointer into items
        
        # Sweep through queries in increasing order
        for q_val, q_idx in sorted_queries:
            # Include all items with price <= q_val and update max_beauty
            while idx < len(items) and items[idx][0] <= q_val:
                max_beauty = max(max_beauty, items[idx][1])
                idx += 1
            res[q_idx] = max_beauty
        
        return res
```
- Notes:
  - Approach: sort items by price and queries by value; sweep once through the items while answering queries in increasing order, maintaining the maximum beauty seen so far.
  - Time complexity: O(n log n + m log m) due to sorting, where n = len(items), m = len(queries). The sweep itself is O(n + m).
  - Space complexity: O(n + m) for sorted structures and the output array (aside from in-place sort of items).