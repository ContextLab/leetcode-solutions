# [Problem 1331: Rank Transform of an Array](https://leetcode.com/problems/rank-transform-of-an-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to replace each element with its rank (1-based) where equal elements get the same rank and ranks are as small as possible. The simplest idea is to determine the order of distinct values (smallest -> largest) and assign increasing ranks starting from 1. Then map each original element to its rank. A sorted order of unique values would give the ranks directly. Handling duplicates is automatic if I use set() before sorting. Edge case: empty array should return empty.

## Refining the problem, round 2 thoughts
- Using sorted(set(arr)) yields the unique values in increasing order. Enumerating that gives rank = index + 1.
- Build a dictionary mapping value -> rank, then transform the original array via lookups. This is straightforward and stable.
- Time complexity: building the set and sorting unique values dominates: O(k log k) where k = number of distinct values, but k ≤ n, so O(n log n) worst-case. Building the result is O(n). Space complexity: O(n) for the mapping and result.
- Alternatives: If we truly wanted O(n) time we could use coordinate compression with counting sort only if values are small/range-limited; not needed here.
- Corner cases: arr empty, all elements equal.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def arrayRankTransform(self, arr: List[int]) -> List[int]:
        if not arr:
            return []
        # Get sorted unique values
        unique_sorted = sorted(set(arr))
        # Map each unique value to its rank (1-based)
        rank_map = {val: i+1 for i, val in enumerate(unique_sorted)}
        # Transform original array using the rank map
        return [rank_map[x] for x in arr]
```
- Notes:
  - Approach: sort the unique values and assign ranks by their index in that sorted list. Then map each original element to its rank.
  - Time complexity: O(n log n) in the worst case (when most elements are distinct) due to sorting; building the result and set is O(n).
  - Space complexity: O(n) additional space for the set/dictionary and the output list.
  - This handles edge cases like empty input and duplicate values correctly.