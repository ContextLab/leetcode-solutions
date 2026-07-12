# [Problem 1331: Rank Transform of an Array](https://leetcode.com/problems/rank-transform-of-an-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to replace each number by its rank among the distinct values. The rank is 1 for the smallest distinct value, 2 for the next distinct, etc. The simplest idea: collect unique values, sort them, then map each unique value to its index+1 as the rank. Finally, transform the original array using that mapping. Duplicates naturally get the same rank. Sorting the unique values is the main cost. Also consider edge cases: empty array, all-equal array, negative numbers — none of these change the approach.

## Refining the problem, round 2 thoughts
- Using sorted(set(arr)) gives the distinct values in increasing order; enumerate over that to build value->rank mapping.
- Alternatively, you can sort pairs (value, original_index) and assign ranks while handling duplicates, but that is a bit more code and not necessary since sorting unique values is simpler.
- Time complexity will be dominated by sorting the unique values: O(k log k) where k is the number of distinct values (k ≤ n). Full transform is O(n) after mapping, so overall O(n log n) worst-case.
- Space: O(k) for the mapping plus O(n) for the output (or in-place overwrite if allowed).
- Edge cases: arr empty -> return []; large n up to 1e5 is fine with this approach.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def arrayRankTransform(self, arr: List[int]) -> List[int]:
        """
        Map each distinct value in arr to its rank (1-based) in sorted order of distinct values,
        then return the transformed list.
        """
        if not arr:
            return []
        # Get sorted distinct values
        sorted_unique = sorted(set(arr))
        # Build mapping value -> rank (1-based)
        rank = {val: i + 1 for i, val in enumerate(sorted_unique)}
        # Transform original array using the mapping
        return [rank[x] for x in arr]
```
- Notes:
  - Approach: coordinate compression via sorting distinct values and mapping each value to its rank.
  - Time complexity: O(n log n) in worst case (when number of distinct values k ~ n, sorting takes O(n log n)); additional O(n) to build result.  
  - Space complexity: O(k) for the value->rank mapping plus O(n) for the returned list (k ≤ n).